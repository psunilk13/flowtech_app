import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote

class CustomDeliveryNote(DeliveryNote):
    def autoname(self):
        from frappe.utils import nowdate

        date = nowdate()
        year = int(date[0:4])
        month = int(date[5:7])

        if month >= 4:
            start_year = year
            end_year = str(year + 1)[-2:]
        else:
            start_year = year - 1
            end_year = str(year)[-2:]

        fy = f"{start_year}-{end_year}"

        last = frappe.db.sql("""
            SELECT name FROM `tabDelivery Note`
            WHERE name LIKE %s
            ORDER BY name DESC
            LIMIT 1
        """, (f"DC{fy}/%",))

        if last:
            last_no = int(last[0][0].split("/")[-1])
            new_no = str(last_no + 1).zfill(5)
        else:
            new_no = "00001"

        self.name = f"DC{fy}/{new_no}"
