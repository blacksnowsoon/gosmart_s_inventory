// Copyright (c) 2025, Gharieb Khalifa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry", {
    onload(frm) {
        frm.set_query("reference_document_type", function() {
            return {
                filters: {
                    "name": ["in", ["Purchase Order", "Sales Order"]],
                    
                }
            };
        });
    },
    setup: function(frm) {
        // Set default values for fields
        // Initialize handlers when form loads
        frm.trigger('setup_item_handlers');
    },
	refresh(frm) {
        // Rebind handlers on refresh (e.g., after adding a row)
        frm.trigger('setup_item_handlers');
        
	},
    stock_entry() {
        if (frm.doc.stock_entry_type === "Material Receipt") {
            
        }
        else if (frm.doc.stock_entry_type === "Material Issue") {
            
        }
    },
    reference_document(frm) {
        if (frm.doc.entry_type === "Material Receipt") {
            frm.set_query("reference_document_type", function() {
                return {
                    filters: {
                        "status": ["in", ["Submitted", "Partially Delivered"]],
                    }
                };
            });
        }
    }
});

frappe.ui.form.on("Stock Entry Item", {
    item_code: function(frm, cdt, cdn) {
        update_item_details(frm, cdt, cdn);
    },
    quy: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    }
});

// ===== HELPER FUNCTIONS =====
function setup_item_handlers(frm) {
    // Remove previous handlers to avoid duplicates
    console.log("frm.fields_dict.items:", frm.fields_dict.items);
console.log("frm.fields_dict.items.grid:", frm.fields_dict.items.grid);
console.log("frm.fields_dict.items.grid.get_docfield('quy'):", frm.fields_dict.items.grid.get_docfield('quy'));
    frm.fields_dict.items.grid.get_docfield('quy').df.onchange = null;
    frm.fields_dict.items.grid.get_docfield('rate').df.onchange = null;
    
    // Manually trigger calculation for existing rows
    frm.doc.items.forEach((item, idx) => {
        calculate_amount(frm, 'Stock Entry Item', item.name);
    });
}

function calculate_amount(frm, cdt, cdn) {
    const row = frappe.get_doc(cdt, cdn);
    const amount = flt(row.quy) * flt(row.rate) || 0;
    
    frappe.model.set_value(cdt, cdn, 'amount', amount).then(() => {
        // Update grand total after all calculations
        update_grand_total(frm);
    });
}

function update_grand_total(frm) {
    let total = 0;
    frm.doc.items.forEach(item => {
        total += flt(item.amount);
    });
    frm.set_value('total_amount', total);
}

function update_item_details(frm, cdt, cdn) {
    const row = frappe.get_doc(cdt, cdn);
    if (row.item_code) {
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Item',
                filters: { name: row.item_code },
                fieldname: ['item_name', 'stander_rate']
            },
            callback: function(r) {
                if (!r.exc) {
                    frappe.model.set_value(cdt, cdn, {
                        'item_name': r.message.item_name,
                        'rate': r.message.stander_rate
                    }).then(() => {
                        calculate_amount(frm, cdt, cdn);
                    });
                }
            }
        });
    }
}

