# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Item(Document):
	def on_update(self):
		"""
		Update current_stock from Bin when item is modified
		"""
		self.update_current_stock_from_bins()

	def update_current_stock_from_bins(self):
		""" 
		Sync item.current_stock with sum of all Bin.actual_qty 
		"""
		from frappe.utils import flt
		if frappe.flags.in_import or frappe.flags.in_migrate:
			# Skip during import or migration to avoid performance issues
			return

		"""
		Sums up the 'actual_qty' from all Bins for this item
		and updates the 'current_stock' field in the Item doctype.
		"""
		total_stock = frappe.db.sql("""
			SELECT COALESCE(SUM(actual_qty), 0)
			FROM `tabBin`
			WHERE item_code = %s
		""", (self.name))[0][0]

		if flt(self.current_stock) != flt(total_stock):
			frappe.db.set_value(
				"Item", 
				self.name, 
				"current_stock", 
				total_stock, 
				update_modified=False
			)
		frappe.publish_realtime(
			"item_stock_updated",
			{"item_code": self.name, "current_stock": total_stock},
			doctype="Item",
			docname=self.name
		)
		
