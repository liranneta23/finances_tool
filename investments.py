from helper_functions import decimal_to_percentage


def calculate_principal(x, n):
    return x * n


def calculate_growth_over_n_years(y, n):
    total_growth = 0
    for i in range(1, n + 1):
        total_growth += ((1 + y) ** i)

    return total_growth / n


def calculate_monthly_required_to_reach_z(z, n, g):
    """
    m = (z / g) / (12 * n) = z / (g * 12 * n)

    :param z: desired amount to reach
    :param n: number of years
    :param g: profit after n years given y yield return
    :return: required monthly investment to reach z given the other parameters
    """

    return z / (g * 12 * n)  # 12 because I have 12 months in a year


def total_return():
    x = int(input("Annual Principal: "))  # the annual principal
    y = int(input("Annual Yield (percentage): ")) / 100  # the annual yield in percentage (10 means 10%)
    n = int(input("Number of Years: "))  # number of years

    p = calculate_principal(x, n)
    g = calculate_growth_over_n_years(y, n)  # the growth (in decimal)
    t = int(p * g)  # for 10% yield and 10 years: x * 1.75

    print(f"The total return after {n} years: €{t}")
    print(f"The total principal after {n} years: €{p}")
    print(f"The total profit after {n} years: €{int(t - p)}")
    print(f"The total growth in percentage after {n} years: {decimal_to_percentage(g)}%")

    print("\n")


def find_how_much_to_invest():
    z = int(input(f"Desired amount: "))
    y = float(input("Annual Yield (percentage): ")) / 100  # the annual yield in percentage (10 means 10%)
    n = int(input("Number of Years: "))  # number of years
    g = calculate_growth_over_n_years(y, n)
    m = round(calculate_monthly_required_to_reach_z(z, n, g), 2)
    print(f"You need to invest €{m} every month to reach €{z} within {n} years with {round(y * 100, 2)}% yield")
    print("\n")
