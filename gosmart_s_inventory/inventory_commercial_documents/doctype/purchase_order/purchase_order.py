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
			if not item.to_warehouse:
				frappe.throw(_("Warehouse is required for item {0} in Purchase Order {1}.").format(item.item_code, self.name))
			# Ensure item qty is greater than zero
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
			
			if not frappe.db.exists("Bin", {"item_code": item.item_code, "warehouse": item.to_warehouse}):
				# If Bin does not exist, create a new one
				
				bin_doc = frappe.new_doc("Bin")
				bin_doc.item_code = item.item_code
				bin_doc.warehouse = item.to_warehouse
				bin_doc.ordered_qty = flt(item.qty) * multiplier
				# Set other fields as necessary, e.g., actual_qty, reserved_qty, etc
				bin_doc.insert(ignore_permissions=True)
			else:
				bin_doc = frappe.get_doc("Bin", {"item_code": item.item_code, "warehouse": item.to_warehouse})
				
				ordered_qty_change = flt(item.qty) * multiplier
				bin_doc.ordered_qty += flt(bin_doc.ordered_qty) + ordered_qty_change
			bin_doc.save(ignore_permissions=True)

	def on_update(self):
		"""Set the status of the Purchase Order based on its items and docstatus."""
		self.set_status()	
	
	def set_status(self):

		# For draft documents, status is set to "Draft"
		if self.docstatus == 0:
			self.status = "Draft"
			return
		# For cancelled documents, status is set to "Cancelled"
		if self.docstatus == 2:
			self.status = "Cancelled"
			return

		# For submitted documents, we need to check the received quantities
		# handle the status based on received quantities
		# If all items are fully received, set status to "Received"
		if all(flt(item.received_qty) >= flt(item.qty) for item in self.items):
			self.status = "Received"
		elif any(flt(item.received_qty) > 0 for item in self.items):
			self.status = "Partially Received"
		else:
			self.status = "To Receive"
	