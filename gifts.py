# Constants
HOME_ACQUISITION_EXEMPTION = 114318
ANNUAL_PARENTAL_EXEMPTION = 6035
FIRST_BRACKET_LIMIT = 138642
FIRST_BRACKET_RATE = 0.10
SECOND_BRACKET_RATE = 0.20


def calculate_gift_tax(gift_amount):
    # Calculate total exemptions
    total_exemptions = HOME_ACQUISITION_EXEMPTION + ANNUAL_PARENTAL_EXEMPTION

    # Calculate taxable amount
    taxable_amount = max(0, gift_amount - total_exemptions)

    # Calculate tax
    if taxable_amount <= FIRST_BRACKET_LIMIT:
        tax = taxable_amount * FIRST_BRACKET_RATE
    else:
        tax = (FIRST_BRACKET_LIMIT * FIRST_BRACKET_RATE) + (
                (taxable_amount - FIRST_BRACKET_LIMIT) * SECOND_BRACKET_RATE)

    return tax


def gift_tax_net(gift_amount):
    # Calculate tax
    tax = calculate_gift_tax(gift_amount)

    # Net amount
    net = gift_amount - tax

    return tax, net


def gift_calculations():
    gift_amount = float(input("Enter the gift amount: "))
    tax, net = gift_tax_net(gift_amount)

    print(f"\nGift Amount: €{gift_amount:.2f}")
    print(f"Estimated Gift Tax: €{tax:.2f}")
    print(f"Net Amount After Tax: €{net:.2f}")
    print("\n")




