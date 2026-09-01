import frappe


def execute(filters=None):
    filters = filters or {}

    validate_filters(filters)

    report_type = filters.get("report_type")

    columns = get_columns(report_type)
    data = get_data(filters, report_type)

    return columns, data


def validate_filters(filters):

    if not filters.get("start_date"):
        frappe.throw("Please select From Date")

    if not filters.get("end_date"):
        frappe.throw("Please select To Date")

    if not filters.get("report_type"):
        frappe.throw("Please select Report Type")


def get_columns(report_type):

    columns = [
        {
            "label": "EMP ID",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": "Working Days",
            "fieldname": "working_days",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": "Payment Days",
            "fieldname": "payment_days",
            "fieldtype": "Float",
            "width": 120
        }
    ]

    # =========================================================
    # MONTHLY SALARY
    # =========================================================

    if report_type == "Monthly Salary":

        columns.extend([
            {
                "label": "Basic",
                "fieldname": "basic",
                "fieldtype": "Currency",
                "width": 120
            },
            {
                "label": "HRA",
                "fieldname": "hra",
                "fieldtype": "Currency",
                "width": 120
            },
            {
                "label": "Conveyance",
                "fieldname": "conveyance",
                "fieldtype": "Currency",
                "width": 120
            },
            {
                "label": "Other Allowance",
                "fieldname": "other_allowance",
                "fieldtype": "Currency",
                "width": 140
            },
            {
                "label": "Director Remuneration",
                "fieldname": "director_remuneration",
                "fieldtype": "Currency",
                "width": 180
            },
            {
                "label": "ARREARS",
                "fieldname": "arrears",
                "fieldtype": "Currency",
                "width": 120
            }
        ])

    # =========================================================
    # PERFORMANCE LINKED INCENTIVE
    # =========================================================

    elif report_type == "Performance Linked Incentive":

        columns.append({
            "label": "Performance Linked Incentive",
            "fieldname": "performance_linked_incentive",
            "fieldtype": "Currency",
            "width": 200
        })

    # =========================================================
    # STATUTORY BONUS
    # =========================================================

    elif report_type == "Statutory Bonus":

        columns.append({
            "label": "Statutory Bonus",
            "fieldname": "statutory_bonus",
            "fieldtype": "Currency",
            "width": 160
        })

    # =========================================================
    # INC + VM + MED
    # =========================================================

    elif report_type == "Inc+VM+Med":

        columns.extend([
            {
                "label": "Incentive",
                "fieldname": "incentive",
                "fieldtype": "Currency",
                "width": 120
            },
            {
                "label": "Vehicle Maintenance",
                "fieldname": "vehicle_maintenance",
                "fieldtype": "Currency",
                "width": 180
            },
            {
                "label": "Medical Allowance",
                "fieldname": "medical_allowance",
                "fieldtype": "Currency",
                "width": 160
            }
        ])

    # =========================================================
    # GROSS PAY
    # =========================================================

    columns.append({
        "label": "Gross Pay",
        "fieldname": "gross_pay",
        "fieldtype": "Currency",
        "width": 130
    })

    # =========================================================
    # DEDUCTIONS
    # =========================================================

    if report_type == "Monthly Salary":

        columns.extend([
            {
                "label": "Income Tax",
                "fieldname": "income_tax",
                "fieldtype": "Currency",
                "width": 130
            },
            {
                "label": "Professional Tax",
                "fieldname": "professional_tax",
                "fieldtype": "Currency",
                "width": 150
            },
            {
                "label": "Monthly Loan Deduction",
                "fieldname": "monthly_loan_deduction",
                "fieldtype": "Currency",
                "width": 180
            },
            {
                "label": "EPF",
                "fieldname": "epf",
                "fieldtype": "Currency",
                "width": 150
            }
        ])

    # =========================================================
    # TOTAL DEDUCTION
    # =========================================================

    columns.append({
        "label": "Total Deduction",
        "fieldname": "total_deduction",
        "fieldtype": "Currency",
        "width": 150
    })

    # =========================================================
    # NET PAY
    # =========================================================

    columns.append({
        "label": "Net Pay",
        "fieldname": "net_pay",
        "fieldtype": "Currency",
        "width": 130
    })

    return columns


def get_data(filters, report_type):

    salary_slips = frappe.db.sql(
        """
        SELECT
            ss.name,
            ss.employee,
            ss.employee_name,
            ss.total_working_days,
            ss.payment_days

        FROM `tabSalary Slip` ss

        WHERE
            ss.docstatus = 1
            AND ss.start_date >= %(start_date)s
            AND ss.end_date <= %(end_date)s

        ORDER BY
            ss.employee ASC
        """,
        {
            "start_date": filters.get("start_date"),
            "end_date": filters.get("end_date")
        },
        as_dict=True
    )

    data = []

    for ss in salary_slips:

        details = frappe.db.sql(
            """
            SELECT
                salary_component,
                SUM(amount) AS amount

            FROM `tabSalary Detail`

            WHERE
                parent = %(salary_slip)s
                AND parenttype = 'Salary Slip'

            GROUP BY
                salary_component
            """,
            {
                "salary_slip": ss.name
            },
            as_dict=True
        )

        components = {}

        for row in details:
            components[row.salary_component] = row.amount or 0


        # =====================================================
        # COMPONENT VALUES
        # =====================================================

        basic = components.get("Basic", 0)
        hra = components.get("HRA", 0)
        conveyance = components.get("Conveyance", 0)
        other_allowance = components.get("Other Allowance", 0)

        performance_linked_incentive = components.get(
            "Performance Linked Incentive", 0
        )

        statutory_bonus = components.get(
            "Statutory Bonus", 0
        )

        vehicle_maintenance = components.get(
            "Vehicle Maintenance", 0
        )

        incentive = components.get(
            "Incentive", 0
        )

        medical_allowance = components.get(
            "Medical Allowance", 0
        )

        director_remuneration = components.get(
            "Director Remuneration", 0
        )

        arrears = components.get(
            "ARREARS", 0
        )

        income_tax = components.get(
            "Income Tax", 0
        )

        professional_tax = components.get(
            "Professional Tax", 0
        )

        monthly_loan_deduction = components.get(
            "Monthly Loan Deduction", 0
        )

        epf = components.get(
            "EPF", 0
        )


        # =====================================================
        # CALCULATE GROSS PAY
        # =====================================================

        if report_type == "Monthly Salary":

            gross_pay = (
                basic
                + hra
                + conveyance
                + other_allowance
                + director_remuneration
                + arrears
            )

        elif report_type == "Performance Linked Incentive":

            gross_pay = performance_linked_incentive

        elif report_type == "Statutory Bonus":

            gross_pay = statutory_bonus

        elif report_type == "Inc+VM+Med":

            gross_pay = (
                incentive
                + vehicle_maintenance
                + medical_allowance
            )

        else:

            gross_pay = 0


        # =====================================================
        # TOTAL DEDUCTION
        # =====================================================

        if report_type == "Monthly Salary":

            total_deduction = (
                income_tax
                + professional_tax
                + monthly_loan_deduction
                + epf
            )

        else:

            total_deduction = 0


        # =====================================================
        # NET PAY
        # =====================================================

        net_pay = gross_pay - total_deduction


        # =====================================================
        # BUILD ROW
        # =====================================================

        row = {
            "employee": ss.employee,
            "employee_name": ss.employee_name,
            "working_days": ss.total_working_days,
            "payment_days": ss.payment_days,

            "gross_pay": gross_pay,
            "total_deduction": total_deduction,
            "net_pay": net_pay
        }


        # =====================================================
        # MONTHLY SALARY FIELDS
        # =====================================================

        if report_type == "Monthly Salary":

            row.update({
                "basic": basic,
                "hra": hra,
                "conveyance": conveyance,
                "other_allowance": other_allowance,
                "director_remuneration": director_remuneration,
                "arrears": arrears,

                "income_tax": income_tax,
                "professional_tax": professional_tax,
                "monthly_loan_deduction": monthly_loan_deduction,
                "epf": epf
            })


        # =====================================================
        # PERFORMANCE LINKED INCENTIVE
        # =====================================================

        elif report_type == "Performance Linked Incentive":

            row["performance_linked_incentive"] = (
                performance_linked_incentive
            )


        # =====================================================
        # STATUTORY BONUS
        # =====================================================

        elif report_type == "Statutory Bonus":

            row["statutory_bonus"] = statutory_bonus


        # =====================================================
        # INC + VM + MED
        # =====================================================

        elif report_type == "Inc+VM+Med":

            row.update({
                "incentive": incentive,
                "vehicle_maintenance": vehicle_maintenance,
                "medical_allowance": medical_allowance
            })


        data.append(row)


    # =========================================================
    # TOTAL ROW
    # =========================================================

    total = {
        "employee": "",
        "employee_name": "Total",
        "working_days": None,
        "payment_days": None
    }


    numeric_fields = [
        "basic",
        "hra",
        "conveyance",
        "other_allowance",
        "director_remuneration",
        "arrears",

        "performance_linked_incentive",
        "statutory_bonus",

        "incentive",
        "vehicle_maintenance",
        "medical_allowance",

        "gross_pay",

        "income_tax",
        "professional_tax",
        "monthly_loan_deduction",
        "epf",

        "total_deduction",
        "net_pay"
    ]


    for field in numeric_fields:

        total[field] = sum(
            (row.get(field) or 0)
            for row in data
        )


    data.append(total)

    return data
