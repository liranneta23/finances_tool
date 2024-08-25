from constants import interest_rates
from gifts import gift_tax_net

MONTHS_IN_YEAR = 12


def find_portion_key(portion):
    if portion == "NHG":
        portion_key = "NHG"
    elif 0 < portion <= 0.65:
        portion_key = "≤65%"
    elif 0.65 < portion <= 0.85:
        portion_key = "≤85%"
    elif 0.85 < portion <= 0.90:
        portion_key = "≤90%"
    elif 0.90 < portion <= 1.0:
        portion_key = ">90%"
    else:
        raise ValueError("Invalid portion input. Must be 'NHG' or a float between 0 and 1.")

    return portion_key


def find_year_key(years):
    if years <= 1:
        return "Variable"
    elif 1 < years <= 5:
        return "5"
    elif 5 < years <= 10:
        return "10"
    elif 10 < years <= 15:
        return "15"
    elif 15 < years <= 20:
        return "20"
    elif years > 20:
        return "30"
    else:
        raise ValueError("Invalid year input. Must be a non-negative number.")


def find_interest_rate(years, portion):
    # Determine the correct portion key
    portion_key = find_portion_key(portion)
    year_key = find_year_key(int(years))

    return interest_rates[year_key][portion_key]


def calculate_total_linear_interest(mortgage_amount, interest_rate, years):
    total_interest = 0
    monthly_principal = mortgage_amount / (years * MONTHS_IN_YEAR)

    remaining_capital = mortgage_amount

    for i in range(years):
        total_interest += remaining_capital * interest_rate
        remaining_capital -= monthly_principal

    return total_interest


def calculate_dutch_linear_mortgage(mortgage_amount, interest_rate, years):
    # Calculate monthly principal payment, also called as 'monthly capital'
    monthly_principal = mortgage_amount / (years * MONTHS_IN_YEAR)

    # Calculate initial monthly interest
    initial_monthly_interest = (mortgage_amount * interest_rate) / MONTHS_IN_YEAR

    # Calculate initial total monthly payment
    initial_monthly_payment = monthly_principal + initial_monthly_interest

    # Calculate final monthly interest (only on the last principal payment)
    final_monthly_interest = (monthly_principal * interest_rate) / MONTHS_IN_YEAR

    # Calculate final total monthly payment
    final_monthly_payment = monthly_principal + final_monthly_interest

    total_interest = calculate_total_linear_interest(mortgage_amount, interest_rate, years)

    return initial_monthly_payment, final_monthly_payment, mortgage_amount, total_interest


def linear_mortgage(mortgage_amount, interest_rate, years):
    initial_payment, final_payment, mortgage_amount, total_interest = calculate_dutch_linear_mortgage(mortgage_amount,
                                                                                                      interest_rate,
                                                                                                      years)

    print(f"Mortgage amount: €{mortgage_amount:.2f}")
    print(f"Initial monthly payment: €{initial_payment:.2f}")
    print(f"Final monthly payment: €{final_payment:.2f}")
    print(f"Monthly payment decrease: €{initial_payment - final_payment:.2f}")
    print(f"Total interest paid : €{total_interest:.2f}")
    print(f"Total amount paid over {years} years: €{mortgage_amount + total_interest:.2f}")


def calculate_annuity_mortgage_payment(principal, interest_rate, years):
    monthly_rate = interest_rate / 12
    num_payments = years * 12

    # Calculate monthly payment
    if monthly_rate == 0:
        return principal / num_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / (
                (1 + monthly_rate) ** num_payments - 1)
        return monthly_payment


def annuity_mortgage(mortgage_amount, interest_rate, years):
    monthly_payment = calculate_annuity_mortgage_payment(mortgage_amount, interest_rate, years)
    print(
        f"Monthly payment for a €{mortgage_amount} loan at {round(interest_rate * 100, 2)}% for {years} years: €{monthly_payment:.2f}")

    # Calculate total amount paid over the life of the loan
    total_paid = monthly_payment * years * MONTHS_IN_YEAR
    total_interest = total_paid - mortgage_amount
    print(f"Total interest paid: €{total_interest:.2f}")
    print(f"Total amount paid over {years} years: €{total_paid:.2f}")


def mortgage():
    print("*** Calculate your mortgage*** ")
    house_price = float(input("House Price: "))
    own_participation = float(input("Your Own Participation: "))
    gift = float(input("Gift Amount: "))
    years = input("Mortgage Duration in years: ")

    gift_tax, gift_net = gift_tax_net(gift)

    # Calculate the mortgage amount
    mortgage_amount = house_price - own_participation - gift_net
    interest_rate = round(find_interest_rate(years, mortgage_amount / house_price) / 100,
                          4)  # divide by 100 since its percentage

    years = int(years)

    print("\n***Linear Mortgage Calculations***")
    linear_mortgage(mortgage_amount, interest_rate, years)

    print("\n***Annuity Mortgage Calculations***")
    annuity_mortgage(mortgage_amount, interest_rate, years)
    print("")
