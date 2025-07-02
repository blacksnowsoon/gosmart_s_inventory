# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import whitelist

class Bin(Document):
	pass	
		

@whitelist()
def update_bin_for_stock_entry(item_code, warehouse):
	"""
	Updates the 'actual_qty' in a Bin based on all Stock Ledger Entries.
    This function should be called after a Stock Entry is submitted or cancelled.
	"""
	bin_name = frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": warehouse}, "name")
	frappe.logger().info(f"Updating Bin for Item: {item_code}, Warehouse: {warehouse}, Bin Name: {bin_name}")
	if not bin_name:
		bin_doc = frappe.new_doc("Bin")
		bin_doc.item_code = item_code
		bin_doc.warehouse = warehouse
		bin_doc.insert()
		bin_name = bin_doc.name
	# calculate actual_qty from Stock Ledger Entries 
	actual_qty = frappe.db.sql("""
		SELECT SUM(qty_change) FROM `tabStock Ledger Entry`
		WHERE item_code = %s AND warehouse = %s AND is_cancelled = 0
	""", (item_code, warehouse))[0][0]
	bin_doc = frappe.get_doc("Bin", bin_name)
	bin_doc.actual_qty = flt(actual_qty) if actual_qty else 0
	bin_doc.projected_qty = flt(bin_doc.actual_qty) + flt(bin_doc.ordered_qty) - flt(bin_doc.reserved_qty)
	bin_doc.save(ignore_permissions=True)
	update_item_stock_level(item_code)

@whitelist()
def update_item_stock_level(item_code):
	"""
	Sums up the 'actual_qty' from all Bins for a given item
    and updates the 'current_stock' field in the Item doctype.
	"""
	total_stock = frappe.db.sql("""
        SELECT SUM(actual_qty)
        FROM `tabBin`
        WHERE item_code = %s
    """, (item_code,), as_list=True)
	total_stock_val = flt(total_stock[0][0]) if total_stock and total_stock[0] else 0
	frappe.db.set_value("Item", item_code, "current_stock", total_stock_val, update_modified=False)
