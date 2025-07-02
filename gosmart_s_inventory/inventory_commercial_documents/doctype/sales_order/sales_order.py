# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class SalesOrder(Document):
	def validate(self):
		self.validate_dates()
		self.validate_items()
		self.caculate_totals()
	
	def validate_dates(self):
		if self.order_date and (self.delivery_date and self.order_date > self.delivery_date):
			frappe.throw(_("Order Date cannot be after Delivery Date."))

	def validate_items(self):
		for item in self.items:
			if not item.from_warehouse:
				frappe.throw(_("Warehouse is required for item {0} in Sales Order {1}.").format(item.item_code, self.name))
			if not item.qty or flt(item.qty) <= 0:
				frappe.throw(_("Quantity must be greater than zero for item {0}.").format(item.item_code))
			bin_info = frappe.get_doc("Bin", {"item_code": item.item_code, "warehouse": item.from_warehouse})
			available_qty = flt(bin_info.actual_qty) - flt(bin_info.reserved_qty)
			if available_qty < flt(item.qty):
				frappe.throw(_("Insufficient stock for item {0} in warehouse {1}. Available: {2}, Required: {3}").format(
					item.item_code, item.from_warehouse, available_qty, item.qty))

	def on_submit(self):
		"""Updates the 'reserved_qty' in the Bin when a Sales Order is submitted."""
		self.update_bin_quantities(1)
		self.set_status()
	
	def on_cancel(self):
		"""Reverses the 'reserved_qty' in the Bin when a Sales Order is cancelled."""
		self.update_bin_quantities(-1)
		self.set_status()
	
	def update_bin_quantities(self, multiplier):
		"""
		A generic function to update reserved quantities in Bins.
		
		:param multiplier: 1 for submission, -1 for cancellation.
		"""
		for item in self.items:
			
			bin_doc = frappe.get_doc("Bin", {"item_code": item.item_code, "warehouse": item.from_warehouse})
			if not bin_doc:
				bin_doc = frappe.new_doc("Bin")
				bin_doc.item_code = item.item_code
				bin_doc.warehouse = item.from_warehouse
				bin_doc.insert(ignore_permissions=True)
			
			# Check for existing reserved_qty in the Bin
			if multiplier == 1:
				bin_info = frappe.get_doc("Bin", {"item_code": item.item_code, "warehouse": item.from_warehouse})
				available_qty = flt(bin_info.actual_qty) - flt(bin_info.reserved_qty)
				if available_qty < flt(item.qty):
					frappe.throw(_("Insufficient stock for item {0} in warehouse {1}. Available: {2}, Required: {3}").format(
						item.item_code, item.from_warehouse, available_qty, item.qty))
			reserved_qty_change = flt(item.qty) * multiplier
			frappe.db.sql("""
				UPDATE `tabBin`
				SET reserved_qty = reserved_qty + %s
				WHERE item_code = %s AND warehouse = %s
			""", (reserved_qty_change, item.item_code, item.from_warehouse))

			# Recalculate projected quantity for the updated Bin
			bin_doc = frappe.get_doc("Bin", {"item_code": item.item_code, "warehouse": item.from_warehouse})
			bin_doc.save(ignore_permissions=True)

	def caculate_totals(self):
		self.total_amount = sum(flt(item.amount) for item in self.items)

	def set_status(self):
		if all(flt(item.delivered_qty) >= flt(item.qty) for item in self.items):
			self.status = "Delivered"
		elif any(flt(item.delivered_qty) > 0 for item in self.items):
			self.status = "Partially Delivered"
		elif self.docstatus == 1:
			self.status = "To Deliver"
		elif self.docstatus == 2:
			self.status = "Cancelled"
		else:
			self.status = self.docstatus == 0 and "Draft" or "Submitted"
