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

