frappe.query_reports["Salary Slip Report"] = {

    filters: [

        {
            fieldname: "start_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1
        },

        {
            fieldname: "end_date",
            label: "To Date",
            fieldtype: "Date",
            reqd: 1
        },

        {
            fieldname: "report_type",
            label: "Report Type",
            fieldtype: "Select",
            options: [
                "Monthly Salary",
                "Performance Linked Incentive",
                "Statutory Bonus",
                "Inc+VM+Med"
            ].join("\n"),
            default: "Monthly Salary",
            reqd: 1
        }

    ]

};
