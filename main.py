from gifts import gift_calculations
from investments import total_return, find_how_much_to_invest
from mortgage import mortgage


def main():
    choices_dictionary = {
        "1": total_return,
        "2": find_how_much_to_invest,
        "3": gift_calculations,
        "4": mortgage
    }

    while True:
        print("*** Menu ***")
        print("1. Calculate return given annual principal, annual yield and number of years")
        print(
            "2. Calculate the required monthly invested to reach your desired amount, given the annual yield and number of years")
        print("3. Gift calculations")
        print("4. Mortgage calculations")

        user_input = input("\nYour choice: ")
        if user_input in choices_dictionary:
            choices_dictionary[user_input]()  # Call the function
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
