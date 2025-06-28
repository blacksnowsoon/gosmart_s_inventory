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
		self.validate_totals()
	
	def before_submit(self):
		self.set_status()

	def before_cancel(self):
		self.check_delivered_qty()

	def validate_dates(self):
		if self.required_by_date and self.required_by_date < self.order_date:
			frappe.throw(_("Required By Date cannot be before Order Date."))

	def validate_items(self):
		for item in self.items:
			if not item.qty or flt(item.quy) <= 0:
				frappe.throw(_("Quantity must be greater than zero for item {0}.").format(item.item_code))

	def caculate_totals(self):
		self.total_amount = sum(flt(item.amount) for item in self.items)

	def set_status(self):
		if all(flt(item.delivered_quy) >= flt(item.quy) for item in self.items):
			self.status = "Delivered"
		elif any(flt(item.delivered_quy) > 0 for item in self.items):
			self.status = "Partially Delivered"
		else:
			self.status = "To Deliver"

	def check_delivered_qty(self):
		for item in self.items:
			if flt(item.delivered_quy) > 0:
				frappe.throw(_("Cannot cancel because item {0} has already been delivered (Qty: {1})").format(item.item_code, item.delivered_quy))

	def update_delivered_qty(self, item_code, delivered_qty):
		for item in self.items:
			if item.item_code == item_code:
				item.delivered_qty = flt(item.delivered_qty) + flt(delivered_qty)
				break
		self.set_status()
		self.save()
