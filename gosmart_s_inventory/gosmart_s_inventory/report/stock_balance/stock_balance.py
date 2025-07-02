# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    # Define the columns for the report
    columns = get_columns()

    # Get the data based on the filters
    data = get_data(filters)

    # (Optional) Add a chart to the report
    chart = get_chart(data)

    return columns, data, None, chart

def get_columns():
	"""Returns the columns for the report."""
	return [
		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 250},
		{"label": _("Item Group"), "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 150},
		{"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 200},
		{"label": _("Actual Qty"), "fieldname": "actual_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Reserved Qty"), "fieldname": "reserved_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Ordered Qty"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Projected Qty"), "fieldname": "projected_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Unit of Measure"), "fieldname": "uom", "fieldtype": "Link", "options": "Unit", "width": 120},
	]

def get_data(filters):
    """Fetches the data from the Bin doctype based on filters."""
    conditions = get_conditions(filters)
    
    # SQL query to fetch data from Bin and join with Item and Warehouse for more details
    # We use `tabBin` and `tabItem` which are the actual SQL table names for the doctypes
    data = frappe.db.sql(f"""
        SELECT
            bin.item_code,
            item.item_name,
            item_group.item_group as item_group,
            warehouse.warehouse_name as warehouse,
            bin.actual_qty,
            bin.reserved_qty,
            bin.ordered_qty,
            bin.projected_qty,
            uom.unit as uom
        FROM
            `tabBin` as bin
		INNER JOIN
    		`tabItem` as item ON bin.item_code = item.name
		LEFT JOIN
			`tabItem Group` as item_group ON item.item_group = item_group.name
		LEFT JOIN
			`tabUnit` as uom ON item.unit = uom.name
		LEFT JOIN
			`tabWarehouse` as warehouse ON bin.warehouse = warehouse.name

        WHERE
            1 = 1
            {conditions}
        ORDER BY
            bin.item_code, bin.warehouse
    """, filters, as_dict=1)
    
    return data

def get_conditions(filters):
    """Builds the WHERE clause for the SQL query from the filters."""
    conditions = ""
    if filters.get("item_code"):
        conditions += " AND bin.item_code = %(item_code)s"
    if filters.get("warehouse"):
        conditions += " AND bin.warehouse = %(warehouse)s"
    if filters.get("item_group"):
        conditions += " AND item.item_group = %(item_group)s"
    
    return conditions

def get_chart(data):
    """Creates a chart summarizing the data."""
    if not data:
        return None

    # Create a summary of total actual quantity per warehouse
    warehouse_summary = {}
    for row in data:
        warehouse = row.get("warehouse")
        qty = row.get("actual_qty")
        if warehouse in warehouse_summary:
            warehouse_summary[warehouse] += qty
        else:
            warehouse_summary[warehouse] = qty

    chart = {
        "data": {
            "labels": list(warehouse_summary.keys()),
            "datasets": [
                {
                    "name": "Stock by Warehouse",
                    "values": list(warehouse_summary.values())
                }
            ]
        },
        "type": "bar",
        "height": 280,
    }
    return chart
