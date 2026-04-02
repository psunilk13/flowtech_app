import frappe
from my_flowtech_app.events.committed_qty import validate_committed_qty
from my_flowtech_app.events.technical_specs_backend import validate_technical_specs


def validate(doc, method=None):

    # ✅ ONLY validate when needed
    if doc.delivery_date_apply_to == "Selected Items":
        try:
            validate_committed_qty(doc)
        except Exception as e:
            frappe.msgprint(f"Committed Qty Error: {str(e)}")
            raise

    # ✅ Always run this (if required)
    try:
        validate_technical_specs(doc)
    except Exception as e:
        frappe.msgprint(f"Technical Specs Error: {str(e)}")
        raise
def sort_committed_delivery_rows(doc, method=None):

    def safe_int(val):
        try:
            return int(val)
        except:
            return 0

    rows = doc.get("committed_delivery_schedule") or []

    sorted_rows = sorted(rows, key=lambda d: safe_int(d.item_number))

    for i, row in enumerate(sorted_rows, start=1):
        row.idx = i

    doc.set("committed_delivery_schedule", sorted_rows)
