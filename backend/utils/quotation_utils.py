from decimal import Decimal


def recalculate_quotation_totals(quotation):

    total = Decimal("0")

    for detail in quotation.details:

        total += detail.subtotal

    quotation.subtotal = total
    quotation.total = total