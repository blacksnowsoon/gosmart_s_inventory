// Copyright (c) 2025, Gharieb Khalifa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry", {
    onload(frm) {
        filter_reference_document_type(frm);
    },
    setup: function(frm) {
        // Set default values for fields
        // Initialize handlers when form loads
        frm.trigger('setup_item_handlers');
    },
	refresh(frm) {
        // Rebind handlers on refresh (e.g., after adding a row)
        frm.trigger('setup_item_handlers')
        filter_reference_document_type(frm);
        
	},
    entry_type(frm) {
        clear_table(frm, "items");
        frm.set_value("total_amount", 0);
        // Reset warehouses and reference document fields
        frm.set_value("to_warehouse", "");
        frm.set_value("from_warehouse", "");
        frm.set_value("reference_document_type", "");
        frm.set_value("reference_document_name", "");
        if (frm.doc.entry_type === "Material Receipt" || frm.doc.entry_type === "Material Issue") {
            filter_reference_document_type(frm);
        } 
    },
    reference_document_type(frm) {
        // Clear the reference document name when type changes
        frm.set_value("reference_document_name", "");
        clear_table(frm, "items");
        if (frm.doc.reference_document_type) {
            frm.set_value("to_warehouse", "");
            frm.set_value("from_warehouse", "");
            // Filter the reference document name based on the selected type
            filter_reference_document_name(frm); 
        }
    },
    get_items: async function(frm) {
        if (!frm.doc.reference_document_type || !frm.doc.reference_document_name) {
            frappe.msgprint(__("Please select a reference document type and name first."));
            return;
        }

        try {
            const response = await frappe.call({
                method: "gosmart_s_inventory.inventory_transactions.doctype.stock_entry.stock_entry.get_items_from_reference",
                args: {
                    document_type: frm.doc.reference_document_type,
                    document_name: frm.doc.reference_document_name
                },
                freeze: true,
                freeze_message: __("Fetching items from {0}...", [frm.doc.reference_document_type])
            });

            if (response.message && response.message.length) {
                // Preserve existing items if needed
                const current_items = frm.doc.items || [];
                
                // Clear and rebuild table
                frm.clear_table("items");
                
                response.message.forEach(item => {
                    frm.add_child("items", {
                        item_code: item.item_code,
                        rate: item.rate || 0,
                        item_name: item.item_name || "",
                        qty: item.qty,
                        warehouse: frm.doc.entry_type === "Material Receipt" ? item.to_warehouse : item.from_warehouse || "",
                        unit: item.unit,
                        amount: item.amount || 0,
                        // Temporary name, will be finalized on save
                        name: `TEMP-${item.item_code}-${Math.random().toString(36).substr(2, 5)}`
                    });
                });
                frm.refresh_field("items");
                set_total_amount(frm)
            }
        } catch (error) {
            frappe.msgprint(__("Error fetching items: {0}", [error.message]));
            return;
        }
    },
    to_warehouse: function(frm) {
        
    },
    from_warehouse: function(frm) {
    }
});

frappe.ui.form.on("Stock Entry Item", {
    item_code: function(frm, cdt, cdn) {
        const item = frappe.get_doc(cdt, cdn);
        
        if (!item.name || item.name.startsWith("TEMP-")) {
            // Temporary unique ID for UI only
            frappe.model.set_value(cdt, cdn, "name", 
                `TEMP-${item.item_code}-${Math.random().toString(36).substr(2, 5)}`
            );
        } else {
            
        }
        update_item_details(frm, cdt, cdn);
    },
    qty: function(frm, cdt, cdn) {
        // recalculate amount when quantity changes
        calculate_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        // recalculate amount when rate changes
        calculate_amount(frm, cdt, cdn);
    },
    items_remove: function(frm, cdt, cdn) {
        // Recalculate total amount when an item is removed
        set_total_amount(frm);
    },
    items_add: function(frm, cdt, cdn) {
        // Rebind item handlers when a new item is added
        const can_add = validate_warehouses(frm)
        if (!can_add) {
            clear_table(frm, "items");
            return;
        }
        if (frm.doc.entry_type === "Material Receipt" || frm.doc.entry_type === "Material Issue") {
            frappe.model.set_value(cdt, cdn, "warehouse",
                frm.doc.entry_type === "Material Receipt" ? frm.doc.to_warehouse :
                frm.doc.entry_type === "Material Issue" ? frm.doc.from_warehouse : ""
            );
        } else if (frm.doc.entry_type === "Stock Adjustment") {
            frappe.model.set_value(cdt, cdn, "warehouse", frm.doc.to_warehouse);
        }
        setup_item_handlers(frm);
    }
});

function setup_item_handlers(frm) {
    // Manually trigger calculation for existing rows
    frm.doc.items.forEach((item, idx) => {
        calculate_amount(frm, "Stock Entry Item", item.name);
    });
}

function filter_reference_document_type(frm) {
    if (frm.doc.entry_type === "Material Receipt") {
        frm.set_query("reference_document_type", function() {
            return {
                filters: {
                    "name": ["=", "Purchase Order"],
                }
            };
        });
    }
    else if (frm.doc.entry_type === "Material Issue") {
        frm.set_query("reference_document_type", function() {
            return {
                filters: {
                    "name": ["=", "Sales Order"],
                }
            };
        });
    }
}

function filter_reference_document_name(frm) {
    
    frm.set_query("reference_document_name", function() {
        return {
            filters: {
                "docstatus": 1,
            }
        };
    });
}

// frm.set_value("total_amount", items.reduce((sum, item) => sum + (item.amount || 0), 0));
function set_total_amount(frm) {
    let total = 0;
    frm.doc.items.forEach(item => {
        total += flt(item.amount);
    });
    frm.set_value('total_amount', total);
}

function validate_warehouses(frm) {
    if (frm.doc.entry_type === "Material Receipt" && (!frm.doc.to_warehouse && !frm.doc.reference_document_name)) {
        frappe.msgprint({message:__("Please specify the To Warehouse or Reference Document Name."), indicator: "red"});
        return false;
    } else if (frm.doc.entry_type === "Material Issue" && (!frm.doc.from_warehouse && !frm.doc.reference_document_name)) {
        frappe.msgprint({message:__("Please specify the From Warehouse or Reference Document Name."), indicator: "red"});
        return false;
    }else if (frm.doc.entry_type === "Stock Transfer" && (!frm.doc.from_warehouse || !frm.doc.to_warehouse)) {
        frappe.msgprint({message:__("Please specify both From and To Warehouses for Stock Transfer."), indicator: "red"});
        return false;
    } else if (frm.doc.entry_type === "Stock Adjustment" && !frm.doc.to_warehouse) {
        frappe.msgprint({message:__("Please specify the To Warehouse for Stock Adjustment."), indicator: "red"});
        return false;
    } else if (frm.doc.from_warehouse === frm.doc.to_warehouse) {
        frappe.msgprint({message:__("From Warehouse and To Warehouse cannot be the same."), indicator: "red"});
        return false;
    }
    return true;
}
