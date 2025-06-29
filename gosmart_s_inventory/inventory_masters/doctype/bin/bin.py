# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt

class Bin(Document):
	def before_save(self):
		"""
		Recalculates the Projected  quantity before saving the Bin document.
		"""
		self.Projected_qty = flt(self.actaul_qty) + flt(self.ordered_qty) - flt(self.reserved_qty)
		

	
@frappe.whitelist()
def update_bin_for_stock_entry(item_code, warehouse):
	"""
	Updates the 'actual_qty' in a Bin based on all Stock Ledger Entries.
    This function should be called after a Stock Entry is submitted or cancelled.
	"""
	if not frappe.db.exists("Bin", {"item_code": item_code, "warehouse": warehouse}):
		bin_doc = frappe.new_doc("Bin")
		bin_doc.item_code = item_code
		bin_doc.warehouse = warehouse
		bin_doc.insert()
	actual_qty = frappe.db.sql("""
		SELECT SUM(qty_change) FROM `tabStock Ledger Entry`
		WHERE item_code = %s AND warehouse = %s AND is_cancelled = 0
	""", (item_code, warehouse), as_list=True)
	actual_qty_val = flt(actual_qty[0][0]) if actual_qty and actual_qty[0] else 0

	frappe.db.set_value("Bin", {"item_code": item_code, "warehouse": warehouse}, "actual_qty", actual_qty_val)

	# After updating the actaul_qty, save the bin to trigger recalculation of ordered_qty
	bin_doc = frappe.get_doc("Bin", {"item_code": item_code, "warehouse": warehouse})
	bin_doc.save(ignore_permissions=True)