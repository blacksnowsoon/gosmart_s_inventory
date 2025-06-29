# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class PurchaseOrder(Document):
	def validate(self):
		self.validate_dates()
		self.validate_items()

	def validate_dates(self):
		if self.required_by_date and self.required_by_date < self.order_date:
			frappe.throw(_("Required By Date cannot be before Order Date."))

	def validate_items(self):
		for item in self.items:
			if not item.qty or flt(item.qty) <= 0:
				frappe.throw(_("Quantity must be greater than zero for item {0}.").format(item.item_code))
	
	def on_submit(self):
		"""Updates the 'ordered_qty' in the Bin when a Purchase Order is submitted."""
		self.update_bin_quantities(1)
		self.set_status()
	
	def on_cancel(self):
		"""Reverses the 'ordered_qty' in the Bin when a Purchase Order is cancelled."""
		self.update_bin_quantities(-1)
		self.set_status()

	def update_bin_quantities(self, multiplier):
		"""
		A generic function to update ordered quantities in Bins.
        
        :param multiplier: 1 for submission, -1 for cancellation.
		"""
		for item in self.items:
			if not item.warehouse:
				frappe.throw(_(f"Warehouse is required for item {item.item_code} in Purchase Order {self.name}"))
			
			bin_doc = frappe.get_doc("Bin", {"item_code": item.item_code, "warehouse": item.warehouse})
			if not bin_doc:
				bin_doc = frappe.new_doc("Bin")
				bin_doc.item_code = item.item_code
				bin_doc.warehouse = item.warehouse
				bin_doc.insert(ignore_permissions=True)
			
			ordered_qty_change = flt(item.qty) * multiplier
			frappe.db.sql("""
				UPDATE `tabBin`
				SET ordered_qty = ordered_qty + %s
				WHERE item_code = %s AND warehouse = %s
			""", (ordered_qty_change, item.item_code, item.warehouse))

			# Recalculate projected quantity for the updated Bin
			bin_doc = frappe.get_doc("Bin", {"item_code": item.item_code, "warehouse": item.warehouse})
			bin_doc.save(ignore_permissions=True)

	def set_status(self):
		if all(flt(item.received_qty) >= flt(item.qty) for item in self.items):
			self.status = "Received"
		elif any(flt(item.received_qty) > 0 for item in self.items):
			self.status = "Partially Received"
		elif self.docstatus == 1:
			self.status = "To Receive"
		elif self.docstatus == 2:
			self.status = "Cancelled"
		else:
			self.status = "Draft"
	