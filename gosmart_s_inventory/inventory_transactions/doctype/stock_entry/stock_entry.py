# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class StockEntry(Document):
  def validate(self):
    self.validate_items()
    self.validate_mandatory_fields()
	
  def validate_items(self):
    if not self.items:
      frappe.throw(_("Please add at least one item to the stock entry."))

    for item in self.items:
      if not item.item_code:
        frappe.throw(_("Item Code is required for all items in the stock entry."))
      if not item.qty or item.qty <= 0:
        frappe.throw(_("Quantity must be greater than zero for item {0}.").format(item.item_code))
      if not item.uom:
        frappe.throw(_("UOM is required for item {0}.").format(item.item_code))
  
  def validate_mandatory_fields(self):
    if self.entry_type not in ["Material Issue", "Stock Transfer"] and not self.from_warehouse:
      frappe.throw(_("From Warehouse is mandatory for {0}.").format(self.entry_type))
    if self.entry_type not in ["Material Receipt", "Stock Transfer", "Stock Adjustment"] and not self.to_warehouse:
      frappe.throw(_("To Warehouse is mandatory for {0}.").format(self.entry_type))
  
  def before_submit(self):
    if self.docstatus == 1:
      self.update_stock_ledger()
      self.update_reference_documents()
  
  def update_stock_ledger(self):
    for item in self.items:
      if self.entry_type == "Material Issue":
        self.update_stock(item.item_code, self.from_warehouse, -item.qty)
      elif self.entry_type == "Material Receipt":
        self.update_stock(item.item_code, self.to_warehouse, item.qty)
      elif self.entry_type == "Stock Transfer":
        self.update_stock(item.item_code, self.from_warehouse, -item.qty)
        self.update_stock(item.item_code, self.to_warehouse, item.qty)
      elif self.entry_type == "Stock Adjustment":
        self.update_stock(item.item_code, self.to_warehouse, item.qty)

  def update_stock(self, item_code, warehouse, qty):
    if not item_code or not warehouse or qty <= 0:
      return
    bin = self.get_bin(item_code, warehouse)
    # bin.update_stock(qty)

    item = frappe.get_doc("Item", item_code)
    if not item.current_stock:
      item.current_stock = 0
    item.current_stock  = self.get_total_stock(item_code)
    item.save()

  def get_bin(self, item_code, warehouse):
    bin_name = frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": warehouse})
    if not bin_name:
      bin = frappe.new_doc("Bin")
      bin.item_code = item_code
      bin.warehouse = warehouse
      bin.insert()
      return bin
    else:
      return frappe.get_doc("Bin", bin_name)

  def get_total_stock(self, item_code):
    total_stock = frappe.db.sql("""
      SELECT SUM(actual_quy) FROM `tabBin`
      WHERE item_code = %s
    """, (item_code,), as_dict=True)
    return total[0][0] or 0

  def update_reference_documents(self):
    if not self.reference_document_type or not self.reference_document_name:
      return
    if self.reference_document_type == "Purchase Order":
      self.update_purchase_order()
    elif self.reference_document_type == "Sales Order":
      self.update_sales_order()

  def update_purchase_order(self):
    po = frappe.get_doc("Purchase Order", self.reference_document_name)
    for item in self.items:
      if item.item_code in [d.item_code for d in po.items]:
        po_item = next(d for d in po.items if d.item_code == item.item_code)
        po_item.received_qty += item.qty
    # po.update_status()
    po.save()

  def update_sales_order(self):
    so = frappe.get_doc("Sales Order", self.reference_document_name)
    for item in self.items:
      if item.item_code in [d.item_code for d in so.items]:
        so_item = next(d for d in so.items if d.item_code == item.item_code)
        so_item.delivered_qty += item.qty
    # so.update_status()
    so.save()