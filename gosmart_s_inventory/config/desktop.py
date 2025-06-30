from frappe import _

def get_data():
    return [
        {
            "label": _("Inventory"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Warehouse Stock Heatmap",
                    "label": _("Stock Heatmap"),
                    "description": _("Visual warehouse stock levels")
                }
            ]
        }
    ]