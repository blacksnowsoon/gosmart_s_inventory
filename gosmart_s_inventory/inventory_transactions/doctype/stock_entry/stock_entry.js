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
	refresh(frm) {

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
    item_code(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (row.item_code) {
            frappe.db.get_value("Item", row.item_code, ["item_name", "uom"], (data) => {
                frappe.model.set_value(cdt, cdn, "item_name", data.item_name);
                frappe.model.set_value(cdt, cdn, "uom", data.uom);
            });
        }
    }
});