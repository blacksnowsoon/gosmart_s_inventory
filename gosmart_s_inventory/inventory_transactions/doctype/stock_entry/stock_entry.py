# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from gosmart_s_inventory.inventory_masters.doctype.bin.bin import update_bin_for_stock_entry


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
      if not item.unit:
        frappe.throw(_("unit is required for item {0}.").format(item.item_code))
  
  def validate_mandatory_fields(self):
    if self.entry_type in ["Material Issue", "Stock Transfer"] and not self.from_warehouse:
      frappe.throw(_("From Warehouse is mandatory for {0}.").format(self.entry_type))
    if self.entry_type in ["Material Receipt", "Stock Transfer", "Stock Adjustment"] and not self.to_warehouse:
      frappe.throw(_("To Warehouse is mandatory for {0}.").format(self.entry_type))

  def on_submit(self):
      # Update stock ledger and reference documents
      self.update_stock_ledger()
      self.update_status()
      self.update_reference_documents()

  def on_cancel(self):
    # Reverse stock effects and update status
    self.reverse_stock_effects()
    self.update_status()
    self.update_reference_documents()


  def update_stock_ledger(self):
    for item_row in self.items:
      if self.entry_type == "Material Receipt":
        self.make_stock_ledger_entry(item_row, self.to_warehouse, item_row.qty)
      elif self.entry_type == "Material Issue":
        self.make_stock_ledger_entry(item_row, self.from_warehouse, -item_row.qty)
      elif self.entry_type == "Stock Transfer":
        self.make_stock_ledger_entry(item_row, self.from_warehouse, -item_row.qty)
        self.make_stock_ledger_entry(item_row, self.to_warehouse, item_row.qty)
      elif self.entry_type == "Stock Adjustment":
        self.make_stock_ledger_entry(item_row, self.to_warehouse, item_row.qty)

  def reverse_stock_effects(self):
    for item_row in self.items:
      if self.entry_type == "Material Receipt":
        self.make_stock_ledger_entry(item_row, self.to_warehouse, -item_row.qty, is_cancellation=True)

      elif self.entry_type == "Material Issue":
        self.make_stock_ledger_entry(item_row, self.from_warehouse, item_row.qty, is_cancellation=True)

      elif self.entry_type == "Stock Transfer":
        self.make_stock_ledger_entry(item_row, self.from_warehouse, item_row.qty, is_cancellation=True)
        self.make_stock_ledger_entry(item_row, self.to_warehouse, -item_row.qty, is_cancellation=True)

      elif self.entry_type == "Stock Adjustment":
        self.make_stock_ledger_entry(item_row, self.to_warehouse, -item_row.qty, is_cancellation=True)


  def make_stock_ledger_entry(self, item_row, warehouse, qty, is_cancellation=False):
    """
    Create or update stock ledger entry for the item updates the corresponding Bin.
    :param item_row: The row from the Stock Entry items child table.
    :param qty_change: The change in quantity (can be positive or negative).
    :param warehouse: The warehouse where the stock change occurs.
    :param is_cancellation: A flag to indicate if this is a cancellation entry.
    """
    if not item_row or not warehouse:
      frappe.throw(f"A warehouse is required for item {item_row.item_code}.")

    # Create the Stock Ledger Entry
    sle = frappe.new_doc("Stock Ledger Entry")
    sle.item_code = item_row.item_code
    sle.warehouse = warehouse
    sle.posting_date = self.posting_date
    sle.posting_time = self.posting_time
    sle.qty_change = qty
    sle.valuation_rate = item_row.rate
    sle.stock_entry = self.name
    sle.stock_entry_item = item_row.name
    sle.purpose = self.entry_type
    sle.is_cancelled = 1 if is_cancellation else 0
    sle.insert(ignore_permissions=True)
    sle.save(ignore_permissions=True)

    # Update the Bin for the item and warehouse
    update_bin_for_stock_entry(item_row.item_code, warehouse)


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
    po.update_status()
    po.save()

  def update_sales_order(self):
    so = frappe.get_doc("Sales Order", self.reference_document_name)
    for item in self.items:
      if item.item_code in [d.item_code for d in so.items]:
        so_item = next(d for d in so.items if d.item_code == item.item_code)
        so_item.delivered_qty += item.qty
    so.update_status()
    so.save()
  
  def update_status(self):
    if self.docstatus == 0:
      self.status = "Draft"
    elif self.docstatus == 1:
      self.status = "Submitted"
    elif self.docstatus == 2:
      self.status = "Cancelled"

    