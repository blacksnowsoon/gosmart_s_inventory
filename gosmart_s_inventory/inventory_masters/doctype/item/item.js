// Copyright (c) 2025, Gharieb Khalifa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item", {
	refresh(frm) {
        frappe.realtime.on('item_stock_updated', (data) => {
            if (data.doctype === frm.doctype && data.docname === frm.docname) {
                frm.refresh();
            }
        });
	},
});
