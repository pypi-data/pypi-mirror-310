import locale
from datetime import datetime

# Global variables to store localization information
system_locale = None
locale_encoding = None
friendly_language = None
locale_country = None
language_code = None
country_code = None
formatted_language_code = None
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

def detect_system_friendly_language():
    """
    Detect and format system localization information.

    This function initializes global variables with the system's locale information,
    including the locale, encoding, language, country, formatted language code,
    currency symbol, decimal point, thousands separator, date format, time format,
    radix character, thousands separator, yes/no expressions, currency string, era,
    era-based date/time formats, and alternative digits.
    """
    global system_locale, locale_encoding, friendly_language, locale_country, language_code, country_code, formatted_language_code
    global currency_symbol, decimal_point, thousands_separator, date_format, time_format
    global radix_char, thousands_sep, yes_expr, no_expr, currency_str, era, era_d_t_fmt, era_d_fmt, era_t_fmt, alt_digits

    # Set the locale for all categories to the user's default setting
    locale.setlocale(locale.LC_ALL, '')

    # Get the system locale
    system_locale = locale.getlocale()
    if system_locale[0] and system_locale[1]:
        locale_value = system_locale[0]
        locale_encoding = system_locale[1]
        friendly_language = locale_value.split("_")[0]
        locale_country = locale_value.split("_")[1]
        language_code = friendly_language[:2].lower()
        country_code = locale_country[:2].upper()
        formatted_language_code = f"{language_code}_{country_code}"

        # Get currency symbol
        currency_symbol = locale.localeconv()['currency_symbol']

        # Get decimal point and thousands separator
        decimal_point = locale.localeconv()['decimal_point']
        thousands_separator = locale.localeconv()['thousands_sep']

        # Get date and time format using datetime module
        date_format = datetime.now().strftime('%x')
        time_format = datetime.now().strftime('%X')

        # Get additional locale-specific information using localeconv()
        radix_char = locale.localeconv()['decimal_point']
        thousands_sep = locale.localeconv()['thousands_sep']
        yes_expr = "^[yY]"  # Example regex for yes expression
        no_expr = "^[nN]"   # Example regex for no expression
        currency_str = locale.localeconv()['currency_symbol']
        era = "N/A"  # Placeholder as era information is not available
        era_d_t_fmt = "N/A"  # Placeholder as era date/time format is not available
        era_d_fmt = "N/A"  # Placeholder as era date format is not available
        era_t_fmt = "N/A"  # Placeholder as era time format is not available
        alt_digits = "N/A"  # Placeholder as alternative digits are not available
    else:
        system_locale = None
        locale_encoding = None
        friendly_language = None
        locale_country = None
        language_code = None
        country_code = None
        formatted_language_code = None
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
detect_system_friendly_language()

def main():
    """
    Main function to demonstrate the usage of the localization information.

    This function prints the system's locale information, including the locale, encoding,
    language, country, formatted language code, currency symbol, decimal point,
    thousands separator, date format, time format, radix character, thousands separator,
    yes/no expressions, currency string, era, era-based date/time formats, and alternative digits.
    """
    print()
    print(f"System Locale: {system_locale}")
    print(f"Locale Encoding: {locale_encoding}")
    print(f"Friendly Language: {friendly_language}")
    print(f"Locale Country: {locale_country}")
    print(f"Short Language Code: {language_code}")
    print(f"Short Country Code: {country_code}")
    print(f"Formatted Language Code: {formatted_language_code}")
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
