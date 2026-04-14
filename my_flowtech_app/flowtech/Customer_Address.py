import frappe

def get_customer_addresses(customer):
    addresses = frappe.get_all(
        "Address",
        filters={
            "link_doctype": "Customer",
            "link_name": customer
        },
        fields=["name", "address_type", "address_line1", "city"]
    )

    billing_address = None
    shipping_address = None

    for addr in addresses:
        if addr.address_type == "Billing" and not billing_address:
            billing_address = addr
        elif addr.address_type == "Shipping" and not shipping_address:
            shipping_address = addr

    return {
        "billing_address": billing_address,
        "shipping_address": shipping_address
    }
