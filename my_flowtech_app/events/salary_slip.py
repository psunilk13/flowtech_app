import frappe


def submit_annual_additional_payroll(doc, method=None):
    if not doc.custom_annual_additional_payroll:
        return

    annual_payroll_name = doc.custom_annual_additional_payroll

    annual_payroll = frappe.get_doc(
        "Annual Additional Payroll",
        annual_payroll_name
    )

    if annual_payroll.docstatus != 0:
        return

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={
            "custom_annual_additional_payroll": annual_payroll_name
        },
        fields=["name", "docstatus"],
        limit_page_length=0
    )

    if not salary_slips:
        return

    for salary_slip in salary_slips:
        if salary_slip.docstatus != 1:
            return

    annual_payroll.submit()
