const footer_content = 
`<div class="navbar fixed-bottom navbar-default border-top">
  <div class="container">
    <div>
      <small class="">Simple Inventory Management v1.0.0</small><br>
      
    </div>
    <div><small class="">© 2025 GO Smart Soultion. All rights reserved.</small></div>
  </div>
  </div>`;

  $('footer').html(footer_content);

  // spenner
function spenner(){
  const container = document.createElement('div');
  container.classList.add('d-flex');
  container.classList.add('justify-content-center');
	const spenner = document.createElement('div');
	spenner.classList.add('text-center');
	spenner.classList.add('spinner-grow');
	spenner.classList.add('text-info');
	spenner.classList.add('spinner-border-sm');
	spenner.classList.add('mb-3');
	spenner.setAttribute('role', 'status');
	spenner.setAttribute('aria-hidden', 'true');
  container.appendChild(spenner);
	return container
}


// ===== HELPER FUNCTIONS =====

function calculate_amount(frm, cdt, cdn) {
    const row = frappe.get_doc(cdt, cdn);
    const amount = flt(row.qty) * flt(row.rate) || 0;
    
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

function clear_table(frm, table_name) {
    frm.clear_table(table_name);
    frm.refresh_field(table_name);
}
function show_alert(message, title = __("Alert"), indicator = "blue") {
    frappe.show_alert({
        message: __(message),
        title: __(title),
        indicator: indicator
    });
}
