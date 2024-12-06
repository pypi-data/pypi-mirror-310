### `localemembers` Module Documentation

Welcome to the documentation for the `localemembers` module. This Python module is designed to detect and format system localization information using the `locale` module. It also provides an elegant and sleek graphical interface to display this information to the user.

#### Table of Contents

- [`localemembers` Module Documentation](#localemembers-module-documentation)
  - [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Graphical Interface](#graphical-interface)
  - [Example of the Graphical Interface](#example-of-the-graphical-interface)
- [Contributing](#contributing)
- [License](#license)

### Installation

You can install the `localemembers` module using pip:

```bash
pip install localemembers
```

For a local installation, you can clone the GitHub repository and install the module in development mode:

```bash
git clone https://github.com/yourusername/localemembers.git
cd localemembers
pip install -e .
```

### Usage

Here is an example of how to use the `localemembers` module to obtain and display system localization information:

```python
import localemembers

# To run the main function
localemembers.main()

# To run the graphical interface
localemembers.gui_main()
```

### Features

The `localemembers` module provides the following features:

- **Detection and formatting of localization information**:
  - `system_locale`: System locale.
  - `locale_encoding`: Locale encoding.
  - `friendly_language`: Locale language.
  - `locale_country`: Locale country.
  - `language_code`: Language code.
  - `country_code`: Country code.
  - `formatted_language_code`: Formatted language code.
  - `currency_symbol`: Currency symbol.
  - `decimal_point`: Decimal point.
  - `thousands_separator`: Thousands separator.
  - `date_format`: Date format.
  - `time_format`: Time format.
  - `radix_char`: Radix character.
  - `thousands_sep`: Thousands separator.
  - `yes_expr`: Regular expression for "yes".
  - `no_expr`: Regular expression for "no".
  - `currency_str`: Currency string.
  - `era`: Era.
  - `era_d_t_fmt`: Era-based date/time format.
  - `era_d_fmt`: Era-based date format.
  - `era_t_fmt`: Era-based time format.
  - `alt_digits`: Alternative digits.

### Graphical Interface

The `localemembers` module includes an elegant and sleek graphical interface, created with PyQt5, to display localization information to the user. The graphical interface is maximized at startup and the components are dynamic.

#### Example of the Graphical Interface

```python
import localemembers

# To run the graphical interface
localemembers.gui_main()
```

### Contributing

Contributions are welcome! Please open an issue or submit a pull request on the GitHub repository.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

With this comprehensive documentation, you are ready to use and contribute to the `localemembers` module. If you need further assistance or modifications, feel free to let me know! 😊