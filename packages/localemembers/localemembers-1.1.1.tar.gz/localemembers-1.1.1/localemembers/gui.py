import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

# Import the function to detect system friendly language
from .locale_members import detect_system_language, locale, encoding, language, country, language_code, country_code, language_country_code, currency_symbol, decimal_point, thousands_separator, date_format, time_format, radix_char, thousands_sep, yes_expr, no_expr, currency_str, era, era_d_t_fmt, era_d_fmt, era_t_fmt, alt_digits

class LocaleInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Locale Information")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        # Initialize locale information
        detect_system_language()

        # Create labels to display locale information
        self.labels = {
            "System Locale": QLabel(f"System Locale: {locale}"),
            "Locale Encoding": QLabel(f"Locale Encoding: {encoding}"),
            "Friendly Language": QLabel(f"Friendly Language: {language}"),
            "Locale Country": QLabel(f"Locale Country: {country}"),
            "Short Language Code": QLabel(f"Short Language Code: {language_code}"),
            "Short Country Code": QLabel(f"Short Country Code: {country_code}"),
            "Formatted Language Code": QLabel(f"Formatted Language Code: {language_country_code}"),
            "Currency Symbol": QLabel(f"Currency Symbol: {currency_symbol}"),
            "Decimal Point": QLabel(f"Decimal Point: {decimal_point}"),
            "Thousands Separator": QLabel(f"Thousands Separator: {thousands_separator}"),
            "Date Format": QLabel(f"Date Format: {date_format}"),
            "Time Format": QLabel(f"Time Format: {time_format}"),
            "Radix Character": QLabel(f"Radix Character: {radix_char}"),
            "Thousands Separator": QLabel(f"Thousands Separator: {thousands_sep}"),
            "Yes Expression": QLabel(f"Yes Expression: {yes_expr}"),
            "No Expression": QLabel(f"No Expression: {no_expr}"),
            "Currency String": QLabel(f"Currency String: {currency_str}"),
            "Era": QLabel(f"Era: {era}"),
            "Era Date/Time Format": QLabel(f"Era Date/Time Format: {era_d_t_fmt}"),
            "Era Date Format": QLabel(f"Era Date Format: {era_d_fmt}"),
            "Era Time Format": QLabel(f"Era Time Format: {era_t_fmt}"),
            "Alternative Digits": QLabel(f"Alternative Digits: {alt_digits}")
        }

        # Create a layout and add labels to it
        layout = QVBoxLayout()
        for label in self.labels.values():
            layout.addWidget(label)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)
    window = LocaleInfoWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
