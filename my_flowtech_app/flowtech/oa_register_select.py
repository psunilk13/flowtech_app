import frappe

@frappe.whitelist()
def get_synced_items(doc):
    doc = frappe.parse_json(doc)

    updated_rows = []

    for item in enumerate(doc.get("items_details", []), start=1):
        updated_rows.append({
            "item_number": item.get("custom_serial_no"),
            "item_code": item.get("item"),
            "item_name": item.get("item_name"),
            "ordered_qty": item.get("quantity")
        })

    return updated_rows
