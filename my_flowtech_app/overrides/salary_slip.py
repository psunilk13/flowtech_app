from frappe.utils import flt

from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip as HRMSSalarySlip


class SalarySlip(HRMSSalarySlip):

    def validate(self):

        # Normal Salary Slip
        if not self.custom_annual_additional_payroll:
            return super().validate()

        # --------------------------------------------
        # Annual Additional Payroll Salary Slip
        # --------------------------------------------

        self.check_salary_withholding()

        self.status = self.get_status()

        from hrms.hr.utils import validate_active_employee
        validate_active_employee(self.employee)

        self.validate_dates()
        self.check_existing()

        # Required Salary Slip fields
        self.salary_structure = "Annual Additional Payroll"

        self.total_working_days = 1
        self.payment_days = 1

        # No deductions
        self.set("deductions", [])

        # Calculate ONLY the supplied annual earnings
        self.calculate_annual_additional_net_pay()


    def calculate_annual_additional_net_pay(self):

        total_earnings = 0

        for earning in self.get("earnings"):

            earning.amount = flt(earning.amount)

            total_earnings += earning.amount


        # Absolutely no deductions
        self.set("deductions", [])


        self.gross_pay = total_earnings
        self.total_earnings = total_earnings

        self.base_gross_pay = flt(
            total_earnings * flt(self.exchange_rate or 1)
        )


        self.total_deduction = 0
        self.base_total_deduction = 0


        self.net_pay = total_earnings

        self.base_net_pay = flt(
            total_earnings * flt(self.exchange_rate or 1)
        )


        self.rounded_total = self.net_pay
        self.base_rounded_total = self.base_net_pay


        # No Income Tax
        self.current_month_income_tax = 0
        self.total_income_tax = 0
        self.tax_exemption_declaration = 0
        self.future_income_tax_deductions = 0
        self.income_tax_deducted_till_date = 0


        self.set_net_total_in_words()
