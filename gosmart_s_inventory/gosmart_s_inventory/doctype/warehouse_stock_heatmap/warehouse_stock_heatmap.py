# Copyright (c) 2025, Gharieb Khalifa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cint, flt
import json


class WarehouseStockHeatmap(Document):
	pass

def get_context(context):
    context.heatmap_data = generate_heatmap_data()

def generate_heatmap_data():
    # Data fetching logic from original example
    return json.dumps(heatmap_dict)
