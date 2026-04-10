# import frappe

# def validate_technical_specs(doc, method=None):
#      pass;

# # =====================================================
# # 1. SYNC ITEMS → TECHNICAL SPECS
# # =====================================================

# def sync_technical_specs_rows(doc):

#     items = doc.get("items_details") or []
#     specs = doc.get("item_technical_specs") or []

#     spec_map = {}
#     for d in specs:
#         if d.item_row_id:
#             spec_map[d.item_row_id] = d

#     new_rows = []

#     for item in items:

#         serial = item.custom_serial_no or ""

#         # ❌ skip split rows like 3-01
#         if "-" in str(serial):
#             continue

#         if not item.name:
#             continue

#         row = spec_map.get(item.name)

#         if not row:
#             row = {}

#         row_data = {
#             "item_row_id": item.name,
#             "item_code": item.item or "",
#             "item_name": item.item_name or "",
#             "item_number": serial
#         }

#         new_rows.append(row_data)

#     doc.set("item_technical_specs", [])

#     for row in new_rows:
#         doc.append("item_technical_specs", row)
# # =====================================================
# # 2. CLEANUP LOGIC
# # =====================================================

# def clean_item_parameters(doc):

#     rows = doc.get("item_technical_specs") or []

#     cleaned = []

#     for row in rows:

#         if not row.colour:
#             continue

#         if row.colour != "Others":
#             row.please_specify = ""

#         cleaned.append(row.as_dict())

#     doc.set("item_technical_specs", [])

#     for row in cleaned:
#         doc.append("item_technical_specs", row)


# # =====================================================
# # 3. SORTING
# # =====================================================

# def sort_technical_rows(doc):

#     rows = doc.get("item_technical_specs") or []

#     def safe_float(val):
#         try:
#             return float(val)
#         except:
#             return 0

#     sorted_rows = sorted(
#         rows,
#         key=lambda d: safe_float(d.item_number)
#     )

# CODE 2

import frappe

def validate_technical_specs(doc, method=None):
    clean_item_parameters(doc)
    sort_technical_rows(doc)

#    frappe.msgprint("1")
#
#    frappe.msgprint("Before function call")
#
#    sync_technical_specs_rows(doc)

#   frappe.msgprint("After function call")

#    frappe.msgprint("2")

#    clean_item_parameters(doc)

#    frappe.msgprint("3")

#    sort_technical_rows(doc)

#    frappe.msgprint("Running Technical Specs Validation")

# =====================================================
# 1. SYNC ITEMS → TECHNICAL SPECS
# =====================================================

# def sync_technical_specs_rows(doc):

#     items = doc.get("items_details") or []
#     specs = doc.get("item_technical_specs") or []

#     spec_map = {}
#     for d in specs:
#         if d.item_row_id:
#             spec_map[d.item_row_id] = d

#     new_rows = []

#     for item in items:

#         if not item.name:
#             continue

#         row = spec_map.get(item.name)

#         if not row:
#             row = {}

#         row_data = {
#             "item_row_id": item.name,
#             "item_code": item.item or "",
#             "item_name": item.item_name or "",
#             "item_number": item.custom_serial_no or ""
#         }

#         new_rows.append(row_data)

#     doc.set("item_technical_specs", [])

#     for row in new_rows:
#         doc.append("item_technical_specs", row)
# def sync_technical_specs_rows(doc):

#     items = doc.get("items_details") or []
#     specs = doc.get("item_technical_specs") or []

#     spec_map = {}
#     for d in specs:
#         if d.item_row_id:
#             spec_map[d.item_row_id] = d

#     new_rows = []

#     for item in items:

#         serial = item.custom_serial_no or ""

#         # ❌ skip split rows like 3-01
#         if "-" in str(serial):
#             continue

#         if not item.name:
#             continue

#         row = spec_map.get(item.name)

#         if not row:
#             row = {}

#         row_data = {
#             "item_row_id": item.name,
#             "item_code": item.item or "",
#             "item_name": item.item_name or "",
#             "item_number": serial
#         }

#         new_rows.append(row_data)

#     doc.set("item_technical_specs", [])

#     for row in new_rows:
#         doc.append("item_technical_specs", row)
# =====================================================
# 2. CLEANUP LOGIC
# =====================================================

def clean_item_parameters(doc):

    rows = doc.get("item_technical_specs") or []

    cleaned = []

    for row in rows:

        if not row.colour:
            continue

        if row.colour != "Others":
            row.please_specify = ""

        cleaned.append(row.as_dict())

    doc.set("item_technical_specs", [])

    for row in cleaned:
        doc.append("item_technical_specs", row)


# =====================================================
# 3. SORTING
# =====================================================

def sort_technical_rows(doc):

    rows = doc.get("item_technical_specs") or []

    def safe_float(val):
        try:
            return float(val)
        except:
            return 0

    sorted_rows = sorted(
        rows,
        key=lambda d: safe_float(d.item_number)
    )

    doc.set("item_technical_specs", [])

    for row in sorted_rows:
        doc.append("item_technical_specs", row.as_dict())
#     doc.set("item_technical_specs", [])

#     for row in sorted_rows:
#         doc.append("item_technical_specs", row.as_dict())
