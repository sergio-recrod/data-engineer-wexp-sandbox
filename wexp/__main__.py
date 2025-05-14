import argparse
from load_data import load_data
from exporters import (
    get_countries,
    get_top_types_per_country,
    get_country_by_name,
    get_top_country_per_type
)


def test(arguments):
    if len(list(get_countries())) > 0:
        print("OK: There is some test data. Let's go.")
    else:
        print("ERROR: There is no test data.")


def show_countries(*args):
    for country in get_countries():
        print(country)


def show_top_types(*args):
    def top_three(items):
        return sorted(items, key=lambda i: i.value, reverse=True)[:3] # this should not be hardcoded to top 3

    def top_n(items, n):
        return sorted(items, key=lambda i: i.value, reverse=True)[:n]

    for country in get_top_types_per_country().values():
        print(country)
        try:
            for index, export in enumerate(top_n(country.exports.values(), int(args[0][-1]))):
                print(f"\t{index + 1}: {export}")
        except:
            for index, export in enumerate(top_n(country.exports.values(), 3)):
                print(f"\t{index + 1}: {export}")


def show_top_countries(*args):
    for whiskey_type, countries in get_top_country_per_type().items():
        print(whiskey_type)
        for country in countries.keys():
            print(f"\t{country}: {countries[country]}") 



# new func to print single country by name
def show_single_country(*args):
    print (get_country_by_name(*args))


def show(commands):
    if commands == []:
        print("Incorrect syntax. \nUsage: wexp show <what>\n")
        return

    {
        "countries": show_countries,
        "top": show_top_types,
        "types": show_top_countries,
        "single": show_single_country  # for single country
    }[commands[0]](commands[1:])


def main():
    print()

    load_data()

    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="+")
    arguments = parser.parse_args()

    command_functions = {"test": test, "show": show}

    command_functions[arguments.command[0]](arguments.command[1:])

    print()


main()
