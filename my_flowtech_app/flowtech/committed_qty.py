import frappe


def validate_delivery(doc, method=None):
    """
    Main validate hook
    - ONLY performs validation
    """

    import json
    if isinstance(doc, str):
        doc = json.loads(doc)
        doc = frappe.get_doc(doc)

    if doc.delivery_date_apply_to == "Selected Items":
        validate_committed_qty(doc)

# =====================================================
# VALIDATION
# =====================================================

def validate_committed_qty(doc):

    ordered_map = {}

    # 🔹 Build ordered map using stable key
    for row in doc.items_details:
      #  if not row.custom_serial_no:
      #      continue
        serial = row.custom_serial_no or ""

    # ❌ skip split rows
        if "-" in str(serial):
            continue

        ordered_map[row.custom_serial_no] = {
            "qty": row.quantity or 0,
            "item_code": row.item,
            "item_name": row.item_name
        }

    committed_map = {}

    # 🔹 Sum committed qty
    for row in doc.committed_delivery_schedule:

        if not row.item_row_id:
            frappe.throw(f"Row #{row.idx}: Missing Item reference")

        committed_map[row.item_row_id] = (
            committed_map.get(row.item_row_id, 0)
            + (row.committed_qty or 0)
        )

    exceeded_items = []

    # 🔹 Validate totals
    for item_key, total in committed_map.items():

        if item_key not in ordered_map:
            frappe.throw(
                f"Invalid mapping: Serial No {item_key} not found in Items table"
            )

        ordered_data = ordered_map[item_key]
        ordered_qty = ordered_data.get("qty", 0)

        if total > ordered_qty:
            exceeded_items.append(
                f"{ordered_data.get('item_code')} ({ordered_data.get('item_name')})"
            )

    # 🔹 Final error
    if exceeded_items:
        frappe.throw(
            "Committed quantity exceeded for:<br><b>" +
            "<br>".join(exceeded_items) +
            "</b>"
        )

def sort_committed_delivery_rows(doc, method=None):

    def safe_int(val):
        try:
            return int(val)
        except:
            return 0

    rows = doc.get("committed_delivery_schedule") or []

    # ✅ sort by item_number
    sorted_rows = sorted(rows, key=lambda d: safe_int(d.item_number))

    # ✅ reassign idx (VERY IMPORTANT)
    for i, row in enumerate(sorted_rows, start=1):
        row.idx = i

    # ✅ overwrite table properly
    doc.set("committed_delivery_schedule", sorted_rows)
