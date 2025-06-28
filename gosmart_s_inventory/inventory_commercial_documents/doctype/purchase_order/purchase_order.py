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
		self.validate_totals()

	def before_submit(self):
		self.set_status()

	def before_cancel(self):
		self.check_received_qty()

	def validate_dates(self):
		if self.required_by_date and self.required_by_date < self.order_date:
			frappe.throw(_("Required By Date cannot be before Order Date."))

	def validate_items(self):
		if not self.items:
			frappe.throw(_("Please add at least one item to the purchase order."))

		for item in self.items:
			if not item.quy or flt(item.quy) <= 0:
				frappe.throw(_("Quantity must be greater than zero for item {0}.").format(item.item_code))

	def set_status(self):
		if all(flt(item.received_quy) >= flt(item.quy) for item in self.items):
			self.status = "Received"
		elif any(flt(item.received_quy) > 0 for item in self.items):
			self.status = "Partially Received"
		else:
			self.status = "To Receive"
	
	def check_received_qty(self):
		for item in self.items:
			if flt(item.received_quy) > 0:
				frappe.throw(_("Cannot cancel because item {0} has already been received (Qty: {1})").format(item.item_code, item.received_quy))
	
	def update_received_qty(self, item_code, received_qty):
		for item in self.items:
			if item.item_code == item_code:
				item.received_qty = flt(item.received_qty) + flt(received_qty)
				break
		self.set_status()
		self.save()
