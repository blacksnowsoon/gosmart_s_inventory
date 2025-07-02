// Copyright (c) 2025, Gharieb Khalifa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase Order", {
	setup: function(frm) {
        // Set default values for fields
        // Initialize handlers when form loads
        frm.trigger('setup_item_handlers');
    },
	refresh(frm) {
        frm.trigger('setup_item_handlers');
        // Rebind handlers on refresh (e.g., after adding a row)
	},
});

frappe.ui.form.on("Purchase Order Item", {
    item_code: function(frm, cdt, cdn) {
        update_item_details(frm, cdt, cdn);
    },
    qty: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    }
});

function setup_item_handlers(frm) {
    // Remove previous handlers to avoid duplicates
    frm.fields_dict.items.grid.get_docfield('qty').df.onchange = null;
    frm.fields_dict.items.grid.get_docfield('rate').df.onchange = null;
    
    // Manually trigger calculation for existing rows
    frm.doc.items.forEach((item, idx) => {
        calculate_amount(frm, "Purchase Order Item", item.name);
    });
}

