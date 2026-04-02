import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_items_details(doc):

    import json

    if isinstance(doc, str):
        doc = json.loads(doc)

    items = doc.get("items_details", [])

    return [
        {
            "item_code": d.get("item"),
            "item_name": d.get("item_name"),
            "item_number": d.get("custom_serial_no"),
            "ordered_qty": d.get("quantity"),
            "inspected_qty": d.get("quantity")
        }
        for d in items
        if "-" not in str(d.get("custom_serial_no") or "")
    ]
