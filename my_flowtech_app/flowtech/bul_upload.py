# import frappe
# import csv
# import os
# import openpyxl
# from frappe.utils.file_manager import get_files_path, get_file_path


# # =====================================================
# # BULK UPLOAD ITEMS (CSV / EXCEL)
# # =====================================================
# @frappe.whitelist()
# def upload_bulk_items(parent, file_url):

#     file_doc = frappe.get_doc("File", {"file_url": file_url})
#     file_path = os.path.join(get_files_path(), os.path.basename(file_doc.file_name))

#     if not os.path.exists(file_path):
#         frappe.throw(f"File not found: {file_path}")

#     parent_doc = frappe.get_doc("Enquiry", parent)
#     count = 0

#     def get_warehouse(item_code):
#         bin_doc = frappe.get_all(
#             "Bin",
#             filters={"item_code": item_code},
#             fields=["warehouse", "actual_qty"]
#         )
#         if bin_doc:
#             return bin_doc[0]["warehouse"], bin_doc[0]["actual_qty"]
#         return "", 0

#     ext = os.path.splitext(file_path)[1].lower()

#     # ---------------- CSV ----------------
#     if ext == ".csv":
#         with open(file_path, encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 if not row.get("item"):
#                     continue

#                 warehouse, warehouse_qty = get_warehouse(row["item"])

#                 parent_doc.append("items_details", {
#                     "item": row.get("item"),
#                     "item_name": row.get("item_name"),
#                     "quantity": row.get("quantity"),
#                     "actual_price": row.get("actual_price"),
#                     "warehouse": warehouse,
#                     "warehouse_qty": warehouse_qty
#                 })
#                 count += 1

#     # ---------------- EXCEL ----------------
#     elif ext == ".xlsx":
#         wb = openpyxl.load_workbook(file_path)
#         sheet = wb.active
#         headers = [cell.value for cell in sheet[1]]

#         required = {"item", "item_name", "quantity", "actual_price"}
#         if not required.issubset(headers):
#             frappe.throw("Excel missing required columns")

#         idx = {h: headers.index(h) for h in headers}

#         for row in sheet.iter_rows(min_row=2, values_only=True):
#             if not row or not row[idx["item"]]:
#                 continue

#             warehouse, warehouse_qty = get_warehouse(row[idx["item"]])

#             parent_doc.append("items_details", {
#                 "item": row[idx["item"]],
#                 "item_name": row[idx["item_name"]],
#                 "quantity": row[idx["quantity"]],
#                 "actual_price": row[idx["actual_price"]],
#                 "warehouse": warehouse,
#                 "warehouse_qty": warehouse_qty
#             })
#             count += 1

#     else:
#         frappe.throw("Upload only CSV or XLSX")

#     parent_doc.save(ignore_permissions=True)
#     frappe.db.commit()

#     return f"Uploaded {count} items successfully"


# # =====================================================
# # PDF → IMAGE GENERATION (FRAPPE CLOUD SAFE)
# # =====================================================
# def generate_images_for_enquiry(doc, method=None, settings=None):
#     """
#     Called from before_print hook.
#     Converts PDF pages to images using PyMuPDF (fitz).
#     """

#     if not doc.get("print_technical_documents"):
#         return

#     try:
#         import fitz  # PyMuPDF
#     except ImportError:
#         frappe.log_error("PyMuPDF not installed", "before_print")
#         return

#     updated = False

#     for row in doc.get("if_any_technical_documents_upload_here", []):

#         if not row.print_this or not row.file:
#             continue

#         if row.get("generated_image"):
#             continue

#         try:
#             file_doc = frappe.get_doc("File", {"file_url": row.file})
#         except frappe.DoesNotExistError:
#             continue

#         pdf_path = get_file_path(file_doc.file_url)
#         if not pdf_path or not pdf_path.lower().endswith(".pdf"):
#             continue

#         try:
#             pdf = fitz.open(pdf_path)
#         except Exception:
#             continue

#         image_urls = []

#         for page_no in range(len(pdf)):
#             page = pdf[page_no]
#             pix = page.get_pixmap(dpi=150)

#             img_name = f"{doc.name}_{row.name}_page_{page_no + 1}.png"
#             img_path = frappe.get_site_path("private/files", img_name)
#             pix.save(img_path)

#             image_file = frappe.get_doc({
#                 "doctype": "File",
#                 "file_name": img_name,
#                 "file_url": f"/private/files/{img_name}",
#                 "is_private": 1
#             })
#             image_file.insert(ignore_permissions=True)

#             image_urls.append(image_file.file_url)

#         if image_urls:
#             row.generated_image = ",".join(image_urls)
#             updated = True

#     if updated:
#         doc.save(ignore_permissions=True)

#updated code(custom_serial_no,discount,gst)

# import frappe
# import csv
# import os
# import openpyxl
# from frappe.utils.file_manager import get_files_path

# @frappe.whitelist()
# def upload_bulk_items(parent, file_url):
#     """
#     Upload CSV or Excel (.xlsx) data into 'items_details' child table of Order Enquiry,
#     automatically fetching Warehouse and warehouse_qty from Bin based on Item.
#     """

#     # Locate uploaded file
#     file_doc = frappe.get_doc("File", {"file_url": file_url})
#     file_path = os.path.join(get_files_path(), os.path.basename(file_doc.file_name))

#     if not os.path.exists(file_path):
#         frappe.throw(f"File not found: {file_path}")

#     #parent_doc = frappe.get_doc('Order Enquiry', parent)
#     parent_doc = frappe.get_doc('Enquiry', parent)
#     count = 0

#     # Determine file type
#     file_ext = os.path.splitext(file_path)[1].lower()

#     def get_warehouse(item_code):
#         bin_doc = frappe.get_all("Bin", filters={"item_code": item_code}, fields=["warehouse", "actual_qty"])
#         if bin_doc:
#             return bin_doc[0]["warehouse"], bin_doc[0]["actual_qty"]
#         return "", 0

#     # ---------------- CSV Upload ----------------
#     if file_ext == '.csv':
#         with open(file_path, 'r', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 custom_serial_no = row.get('custom_serial_no')
#                 item = row.get('item')
#                 item_name = row.get('item_name')
#                 quantity = row.get('quantity')
#                 actual_price = row.get('actual_price')
#                 discount = row.get('discount')
#                 gst = row.get('gst')

#                 warehouse, warehouse_qty = get_warehouse(item)

#                 if item_name:
#                     parent_doc.append('items_details', {
#                         'custom_serial_no': custom_serial_no,
#                         'item': item,
#                         'item_name': item_name,
#                         'quantity': quantity,
#                         'actual_price': actual_price,
#                         'discount':discount,
#                         'gst':gst,
#                         'warehouse': warehouse,
#                         'warehouse_qty': warehouse_qty
#                     })
#                     count += 1

#     # ---------------- Excel Upload ----------------
#     elif file_ext == '.xlsx':
#         wb = openpyxl.load_workbook(file_path)
#         sheet = wb.active
#         headers = [cell.value for cell in sheet[1]]
#         expected_columns = {"custom_serial_no", "item", "item_name", "quantity", "actual_price", "discount", "gst"}

#         if not expected_columns.issubset(set(headers)):
#             frappe.throw(f"Missing columns in Excel file. Expected: {', '.join(expected_columns)}")

#         idx = {header: headers.index(header) for header in headers}

#         for row in sheet.iter_rows(min_row=2, values_only=True):
#             if not any(row):
#                 continue
#             custom_serial_no = row[idx["custom_serial_no"]]
#             item_code = row[idx["item"]]
#             item_name = row[idx["item_name"]]
#             quantity = row[idx["quantity"]]
#             actual_price = row[idx["actual_price"]]
#             discount = row[idx["discount"]]
#             gst = row[idx["gst"]]

#             warehouse, warehouse_qty = get_warehouse(item_code)

#             parent_doc.append('items_details', {
#                 'custom_serial_no': custom_serial_no,
#                 'item': item_code,
#                 'item_name': item_name,
#                 'quantity': quantity,
#                 'actual_price': actual_price,
#                 'discount': discount,
#                 'gst': gst,
#                 'warehouse': warehouse,
#                 'warehouse_qty': warehouse_qty
#             })
#             count += 1
#     else:
#         frappe.throw("Unsupported file format. Please upload a .csv or .xlsx file.")

#     parent_doc.save(ignore_permissions=True)
#     frappe.db.commit()

#     return f"✅ Successfully uploaded {count} items with Warehouse info."

# new bulkupload working code
# -----
import frappe
import csv
import os
import openpyxl
from frappe.utils.file_manager import get_files_path


@frappe.whitelist()
def upload_bulk_items(parent, file_url):
    """
    Upload CSV or Excel (.xlsx) data into 'items_details' child table of Enquiry.
    - GST strictly from file
    - Warehouse from file (if given) else from Bin
    - Warehouse Qty fetched correctly
    """

    # Get file
    file_doc = frappe.get_doc("File", {"file_url": file_url})
    file_path = os.path.join(get_files_path(), file_doc.file_name)

    if not os.path.exists(file_path):
        frappe.throw(f"File not found: {file_path}")

    parent_doc = frappe.get_doc("Enquiry", parent)
    count = 0

    # ---------------- HELPERS ---------------- #

    def normalize_gst(gst):
        if gst is None:
            return None
        gst = str(gst).strip()
        if gst.endswith("%"):
            return gst
        return f"{gst}%"

    def get_warehouse_from_bin(item_code):
        bins = frappe.get_all(
            "Bin",
            filters={"item_code": item_code, "actual_qty": (">", 0)},
            fields=["warehouse", "actual_qty"],
            order_by="actual_qty desc"
        )
        if bins:
            return bins[0]["warehouse"], bins[0]["actual_qty"]
        return "", 0

    def get_bin_qty(item_code, warehouse):
        return frappe.db.get_value(
            "Bin",
            {"item_code": item_code, "warehouse": warehouse},
            "actual_qty"
        ) or 0

    # ---------------- CSV UPLOAD ---------------- #

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".csv":
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:

                item_code = row.get("item")
                if not item_code:
                    continue

                warehouse = row.get("warehouse")
                if warehouse:
                    warehouse_qty = get_bin_qty(item_code, warehouse)
                else:
                    warehouse, warehouse_qty = get_warehouse_from_bin(item_code)

                parent_doc.append("items_details", {
                    "custom_serial_no": row.get("custom_serial_no"),
                    "item": item_code,
                    "item_name": row.get("item_name"),
                    "quantity": row.get("quantity"),
                    "actual_price": row.get("actual_price"),
                    "discount": row.get("discount"),
                    "gst": normalize_gst(row.get("gst")),
                    "warehouse": warehouse,
                    "warehouse_qty": warehouse_qty
                })
                count += 1

    # ---------------- EXCEL UPLOAD ---------------- #

    elif file_ext == ".xlsx":
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        headers = [str(cell.value).strip() for cell in sheet[1]]
        idx = {h: i for i, h in enumerate(headers)}

        required = {
            "custom_serial_no", "item", "item_name",
            "quantity", "actual_price", "discount", "gst"
        }

        if not required.issubset(idx):
            frappe.throw(f"Missing columns: {', '.join(required - set(idx))}")

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue

            item_code = row[idx["item"]]
            if not item_code:
                continue

            excel_warehouse = row[idx["warehouse"]] if "warehouse" in idx else None

            if excel_warehouse:
                warehouse = excel_warehouse
                warehouse_qty = get_bin_qty(item_code, warehouse)
            else:
                warehouse, warehouse_qty = get_warehouse_from_bin(item_code)

            parent_doc.append("items_details", {
                "custom_serial_no": row[idx["custom_serial_no"]],
                "item": item_code,
                "item_name": row[idx["item_name"]],
                "quantity": row[idx["quantity"]],
                "actual_price": row[idx["actual_price"]],
                "discount": row[idx["discount"]],
                "gst": normalize_gst(row[idx["gst"]]),
                "warehouse": warehouse,
                "warehouse_qty": warehouse_qty
            })
            count += 1

    else:
        frappe.throw("Only CSV or XLSX files are supported")

    parent_doc.save(ignore_permissions=True)
    frappe.db.commit()

    return f"✅ Successfully uploaded {count} items"

