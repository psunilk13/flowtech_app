# import frappe

# @frappe.whitelist()
# def cancel_oa_items(oa_name, items):

#     import json
#     items = json.loads(items)

#     # =========================
#     # 🔹 GET DOCUMENTS
#     # =========================
#     oa = frappe.get_doc("OA Register", oa_name)

#     ri_name = frappe.db.get_value("Reserved Inventory", {"oa_register": oa_name})
#     ri = frappe.get_doc("Reserved Inventory", ri_name) if ri_name else None

#     # FLAGS
#     oa.flags.ignore_validate_update_after_submit = True
#     oa.flags.ignore_validate = True

#     if ri:
#         ri.flags.ignore_validate_update_after_submit = True
#         ri.flags.ignore_validate = True

#     oa_rows = oa.get("items_details") or []
#     ri_rows = ri.get("items") if ri else []

#     # =========================
#     # 🔹 PROCESS CANCEL
#     # =========================
#     for item in items:

#         serial = str(item.get("serial_no")).strip()
#         cancel_qty = float(item.get("cancel_qty") or 0)

#         parent_old_qty = 0

#         # 🔹 GET PARENT QTY
#         for row in oa_rows:
#             if str(row.custom_serial_no).strip() == serial:
#                 parent_old_qty = row.quantity or 0
#                 break

#         # =========================
#         # 🔹 OA UPDATE
#         # =========================
#         for row in oa_rows:

#             row_serial = str(row.custom_serial_no).strip()

#             # 🔹 PARENT
#             if row_serial == serial:

#                 if cancel_qty > parent_old_qty:
#                     frappe.throw(f"Cancel qty exceeds available qty for {serial}")

#                 new_qty = parent_old_qty - cancel_qty
#                 row.set("quantity", new_qty)

#                 # 🔍 CHECK CHILD
#                 has_child = any(
#                     str(r.custom_serial_no).strip().startswith(serial + "-")
#                     for r in oa_rows
#                 )

#                 if has_child:
#                     row.set("reserved_qty", 0)
#                     row.already_reserved = 0
#                     row.db_set("already_reserved", 0)
#                 else:
#                     row.set("reserved_qty", new_qty)
#                     row.already_reserved = new_qty
#                     row.db_set("already_reserved", new_qty)

#             # 🔹 CHILD
#             elif row_serial.startswith(serial + "-"):

#                 old_child_qty = row.quantity or 0
#                 old_reserved = row.reserved_qty or 0
#                 old_remaining = row.remaining_quantity or 0

#                 if parent_old_qty > 0:
#                     reduce_qty = (old_child_qty / parent_old_qty) * cancel_qty
#                 else:
#                     reduce_qty = 0

#                 new_child_qty = old_child_qty - reduce_qty
#                 new_reserved = max(old_reserved - reduce_qty, 0)
#                 new_remaining = old_remaining + reduce_qty

#                 row.set("quantity", new_child_qty)
#                 row.set("reserved_qty", new_reserved)

#                 # 🔥 IMPORTANT FIELD
#                 row.already_reserved = new_reserved
#                 row.db_set("already_reserved", new_reserved)

#                 row.set("remaining_quantity", new_remaining)

#         # =========================
#         # 🔹 RESERVED INVENTORY UPDATE
#         # =========================
#         if ri:

#             for row in ri_rows:

#                 row_serial = str(row.custom_serial_no).strip()

#                 if row_serial == serial:

#                     new_qty = (row.quantity or 0) - cancel_qty
#                     row.set("quantity", new_qty)

#                     has_child = any(
#                         str(r.custom_serial_no).strip().startswith(serial + "-")
#                         for r in ri_rows
#                     )

#                     if has_child:
#                         row.set("reserved_qty", 0)
#                     else:
#                         row.set("reserved_qty", new_qty)

#                 elif row_serial.startswith(serial + "-"):

#                     old_child_qty = row.quantity or 0

#                     if parent_old_qty > 0:
#                         reduce_qty = (old_child_qty / parent_old_qty) * cancel_qty
#                     else:
#                         reduce_qty = 0

#                     new_child_qty = old_child_qty - reduce_qty
#                     new_reserved = (row.reserved_qty or 0) - reduce_qty

#                     row.set("quantity", new_child_qty)
#                     row.set("reserved_qty", new_reserved)

#     # =========================
#     # 🔥 DELETE ZERO QTY ROWS
#     # =========================
#     oa.set("items_details", [d for d in oa.get("items_details") if (d.quantity or 0) > 0])

#     if ri:
#         ri.set("items", [d for d in ri.get("items") if (d.quantity or 0) > 0])

#     # =========================
#     # 🔥 DELETE DOCUMENT IF EMPTY
#     # =========================
#     if not oa.get("items_details"):

#         # 🔥 CANCEL + DELETE OA
#         if oa.docstatus == 1:
#             oa.cancel()

#         frappe.delete_doc("OA Register", oa.name, force=1)

#         # 🔥 CANCEL + DELETE RI
#         if ri:
#             if ri.docstatus == 1:
#                 ri.cancel()

#             frappe.delete_doc("Reserved Inventory", ri.name, force=1)

#         return "All items cancelled. Documents deleted"
        
#     # =========================
#     # 🔹 SAVE
#     # =========================
#     oa.save()

#     if ri:
#         ri.save()

#     return "Items Cancelled Successfully"

# code 2

import frappe

@frappe.whitelist()
def cancel_oa_items(oa_name, items):

    import json
    items = json.loads(items)

    # =========================
    # 🔹 GET DOCUMENTS
    # =========================
    oa = frappe.get_doc("OA Register", oa_name)

    ri_name = frappe.db.get_value("Reserved Inventory", {"oa_register": oa_name})
    ri = frappe.get_doc("Reserved Inventory", ri_name) if ri_name else None

    # FLAGS
    oa.flags.ignore_validate_update_after_submit = True
    oa.flags.ignore_validate = True

    if ri:
        ri.flags.ignore_validate_update_after_submit = True
        ri.flags.ignore_validate = True

    oa_rows = oa.get("items_details") or []
    ri_rows = ri.get("items") if ri else []

    # =========================
    # 🔹 PROCESS CANCEL
    # =========================
    for item in items:

        serial = str(item.get("serial_no")).strip()
        cancel_qty = float(item.get("cancel_qty") or 0)

        parent_old_qty = 0

        # 🔹 GET PARENT QTY
        for row in oa_rows:
            if str(row.custom_serial_no).strip() == serial:
                parent_old_qty = row.quantity or 0
                break

        # =========================
        # 🔹 OA UPDATE
        # =========================
        for row in oa_rows:

            row_serial = str(row.custom_serial_no).strip()

            # 🔹 PARENT
            if row_serial == serial:

                if cancel_qty > parent_old_qty:
                    frappe.throw(f"Cancel qty exceeds available qty for {serial}")

                new_qty = parent_old_qty - cancel_qty
                row.set("quantity", new_qty)

                # 🔍 CHECK CHILD
                has_child = any(
                    str(r.custom_serial_no).strip().startswith(serial + "-")
                    for r in oa_rows
                )

                if has_child:
                    row.set("reserved_qty", 0)
                    row.already_reserved = 0
                    row.db_set("already_reserved", 0)
                else:
                    row.set("reserved_qty", new_qty)
                    row.already_reserved = new_qty
                    row.db_set("already_reserved", new_qty)

            # 🔹 CHILD
            elif row_serial.startswith(serial + "-"):

                old_child_qty = row.quantity or 0
                old_reserved = row.reserved_qty or 0
                old_remaining = row.remaining_quantity or 0

                if parent_old_qty > 0:
                    reduce_qty = (old_child_qty / parent_old_qty) * cancel_qty
                else:
                    reduce_qty = 0

                new_child_qty = old_child_qty - reduce_qty
                new_reserved = max(old_reserved - reduce_qty, 0)
                new_remaining = old_remaining + reduce_qty

                row.set("quantity", new_child_qty)
                row.set("reserved_qty", new_reserved)

                # 🔥 IMPORTANT FIELD
                row.already_reserved = new_reserved
                row.db_set("already_reserved", new_reserved)

                row.set("remaining_quantity", new_remaining)

        # =========================
        # 🔹 RESERVED INVENTORY UPDATE
        # =========================
        if ri:

            for row in ri_rows:

                row_serial = str(row.custom_serial_no).strip()

                if row_serial == serial:

                    new_qty = (row.quantity or 0) - cancel_qty
                    row.set("quantity", new_qty)

                    has_child = any(
                        str(r.custom_serial_no).strip().startswith(serial + "-")
                        for r in ri_rows
                    )

                    if has_child:
                        row.set("reserved_qty", 0)
                    else:
                        row.set("reserved_qty", new_qty)

                elif row_serial.startswith(serial + "-"):

                    old_child_qty = row.quantity or 0

                    if parent_old_qty > 0:
                        reduce_qty = (old_child_qty / parent_old_qty) * cancel_qty
                    else:
                        reduce_qty = 0

                    new_child_qty = old_child_qty - reduce_qty
                    new_reserved = (row.reserved_qty or 0) - reduce_qty

                    row.set("quantity", new_child_qty)
                    row.set("reserved_qty", new_reserved)

    # =========================
    # 🔥 DELETE ZERO QTY ROWS
    # =========================
    oa.set("items_details", [d for d in oa.get("items_details") if (d.quantity or 0) > 0])

    if ri:
        ri.set("items", [d for d in ri.get("items") if (d.quantity or 0) > 0])

    # =========================
    # 🔥 DELETE DOCUMENT IF EMPTY
    # =========================
    if not oa.get("items_details"):

        # 🔥 CANCEL + DELETE OA
        if oa.docstatus == 1:
            oa.cancel()

        frappe.delete_doc("OA Register", oa.name, force=1)

        # 🔥 CANCEL + DELETE RI
        if ri:
            if ri.docstatus == 1:
                ri.cancel()

            frappe.delete_doc("Reserved Inventory", ri.name, force=1)

        return "All items cancelled. Documents deleted"
        
    # =========================
    # 🔹 SAVE
    # =========================
    oa.save()

    if ri:
        ri.save()

    return "Items Cancelled Successfully"

# =====================================================
# GENERIC DOCUMENT IMPORT API
# =====================================================

import frappe
from frappe.model.rename_doc import rename_doc


@frappe.whitelist()
def rename_document():

    data = frappe.request.get_json()

    if not data:
        frappe.throw("No JSON received")

    doctype = data.get("doctype")
    old_name = data.get("old_name")
    new_name = data.get("new_name")

    if not frappe.db.exists(doctype, old_name):
        frappe.throw(f"{doctype} {old_name} not found")

    if frappe.db.exists(doctype, new_name):
        frappe.response["message"] = {
            "status": "exists",
            "name": new_name
        }
        return

    rename_doc(
        doctype,
        old_name,
        new_name,
        force=True,
        merge=False
    )

    frappe.db.commit()

    frappe.response["message"] = {
        "status": "success",
        "doctype": doctype,
        "name": new_name
    }
