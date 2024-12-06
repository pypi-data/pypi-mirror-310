from locale import getlocale, setlocale, LC_ALL, localeconv
from datetime import datetime

# Global variables to store localization information
locale = None
encoding = None
language = None
country = None
language_code = None
country_code = None
language_country_code = None
currency_symbol = None
decimal_point = None
thousands_separator = None
date_format = None
time_format = None
radix_char = None
thousands_sep = None
yes_expr = None
no_expr = None
currency_str = None
era = None
era_d_t_fmt = None
era_d_fmt = None
era_t_fmt = None
alt_digits = None

def detect_system_language():
    """
    Detect and format system localization information.

    This function initializes global variables with the system's locale information,
    including the locale, encoding, language, country, formatted language code,
    currency symbol, decimal point, thousands separator, date format, time format,
    radix character, thousands separator, yes/no expressions, currency string, era,
    era-based date/time formats, and alternative digits.
    """
    global locale, encoding, language, country, language_code, country_code, language_country_code
    global currency_symbol, decimal_point, thousands_separator, date_format, time_format
    global radix_char, thousands_sep, yes_expr, no_expr, currency_str, era, era_d_t_fmt, era_d_fmt, era_t_fmt, alt_digits

    # Set the locale for all categories to the user's default setting
    setlocale(LC_ALL, '')

    # Get the system locale
    locale = getlocale()
    if locale[0] and locale[1]:
        locale_value = locale[0]
        encoding = locale[1]
        language = locale_value.split("_")[0]
        country = locale_value.split("_")[1]
        language_code = language[:2].lower()
        country_code = country[:2].upper()
        language_country_code = f"{language_code}_{country_code}"

        # Get currency symbol
        currency_symbol = localeconv()['currency_symbol']

        # Get decimal point and thousands separator
        decimal_point = localeconv()['decimal_point']
        thousands_separator = localeconv()['thousands_sep']

        # Get date and time format using datetime module
        date_format = datetime.now().strftime('%x')
        time_format = datetime.now().strftime('%X')

        # Get additional locale-specific information using localeconv()
        radix_char = localeconv()['decimal_point']
        thousands_sep = localeconv()['thousands_sep']
        yes_expr = "^[yY]"  # Example regex for yes expression
        no_expr = "^[nN]"   # Example regex for no expression
        currency_str = localeconv()['currency_symbol']
        era = "N/A"  # Placeholder as era information is not available
        era_d_t_fmt = "N/A"  # Placeholder as era date/time format is not available
        era_d_fmt = "N/A"  # Placeholder as era date format is not available
        era_t_fmt = "N/A"  # Placeholder as era time format is not available
        alt_digits = "N/A"  # Placeholder as alternative digits are not available
    else:
        locale = None
        encoding = None
        language = None
        country = None
        language_code = None
        country_code = None
        language_country_code = None
        currency_symbol = None
        decimal_point = None
        thousands_separator = None
        date_format = None
        time_format = None
        radix_char = None
        thousands_sep = None
        yes_expr = None
        no_expr = None
        currency_str = None
        era = None
        era_d_t_fmt = None
        era_d_fmt = None
        era_t_fmt = None
        alt_digits = None

# Call the function to initialize the variables
detect_system_language()

def main():
    """
    Main function to demonstrate the usage of the localization information.

    This function prints the system's locale information, including the locale, encoding,
    language, country, formatted language code, currency symbol, decimal point,
    thousands separator, date format, time format, radix character, thousands separator,
    yes/no expressions, currency string, era, era-based date/time formats, and alternative digits.
    """
    print()
    print(f"System Locale: {locale}")
    print(f"Locale Encoding: {encoding}")
    print(f"Friendly Language: {language}")
    print(f"Locale Country: {country}")
    print(f"Short Language Code: {language_code}")
    print(f"Short Country Code: {country_code}")
    print(f"Formatted Language Code: {language_country_code}")
    print(f"Currency Symbol: {currency_symbol}")
    print(f"Decimal Point: {decimal_point}")
    print(f"Thousands Separator: {thousands_separator}")
    print(f"Date Format: {date_format}")
    print(f"Time Format: {time_format}")
    print(f"Radix Character: {radix_char}")
    print(f"Thousands Separator: {thousands_sep}")
    print(f"Yes Expression: {yes_expr}")
    print(f"No Expression: {no_expr}")
    print(f"Currency String: {currency_str}")
    print(f"Era: {era}")
    print(f"Era Date/Time Format: {era_d_t_fmt}")
    print(f"Era Date Format: {era_d_fmt}")
    print(f"Era Time Format: {era_t_fmt}")
    print(f"Alternative Digits: {alt_digits}")
    print()

if __name__ == '__main__':
    main()
