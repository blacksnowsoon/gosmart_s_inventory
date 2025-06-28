# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class Bin(Document):
	def update_stock(self, qty):
		if not self.item_code or not self.warehouse:
			frappe.throw(_("Item Code and Warehouse are required to update stock."))

		if not self.actual_qty:
			self.actual_qty = 0
		
		self.actual_qty += qty
		if self.actual_qty < 0:
			frappe.throw(_("Insufficient stock for item {0} in warehouse {1}.").format(self.item_code, self.warehouse))
		self.save()

		# Update the item stock
		self.update_item_stock()

	def update_item_stock(self):

		item = frappe.get_doc("Item", self.item_code)
		item.current_stock = self.get_total_stock()
		item.save()

	def get_total_stock(self):
		total_stock = frappe.db.sql("""
			SELECT SUM(actual_qty) FROM `tabBin`
			WHERE item_code = %s AND warehouse = %s
		""", (self.item_code, self.warehouse))
		return total_stock[0][0] if total_stock else 0
