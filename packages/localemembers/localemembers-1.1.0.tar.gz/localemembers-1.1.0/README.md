### `localemembers` Module Documentation

Welcome to the documentation for the `localemembers` module. This Python module is designed to detect and format system localization information using the `locale` module. It also provides an elegant and sleek graphical interface to display this information to the user.

#### Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Graphical Interface](#graphical-interface)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [License](#license)

### Installation

#### Automatic Installation via PyPI

You can install the `localemembers` module using pip:

```bash
pip install localemembers
```

#### Manual Installation via GitHub

For a local installation, you can clone the GitHub repository and install the module in development mode:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/localemembers.git
   ```

2. Navigate to the project directory:
   ```bash
   cd localemembers
   ```

3. Install the module in development mode:
   ```bash
   pip install -e .
   ```

### Usage

Here is an example of how to use the `localemembers` module to obtain and display system localization information:

#### Running the Main Function

The main function prints the system's locale information to the console.

```python
import localemembers

# To run the main function
localemembers.main()
```

#### Running the Graphical Interface

The graphical interface displays the system's locale information in a user-friendly window.

```python
import localemembers

# To run the graphical interface
localemembers.gui_main()
```

### Features

The `localemembers` module provides the following features:

- **Detection and formatting of localization information**:
  - `locale`: System locale.
  - `encoding`: Locale encoding.
  - `language`: Locale language.
  - `country`: Locale country.
  - `language_code`: Language code.
  - `country_code`: Country code.
  - `language_country_code`: Formatted language code.
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

#### Detailed Description of Features

- **System Locale**: The locale setting of the system, which includes language and country information.
- **Locale Encoding**: The character encoding used by the locale.
- **Locale Language**: The language part of the locale.
- **Locale Country**: The country part of the locale.
- **Language Code**: A short code representing the language (e.g., 'en' for English).
- **Country Code**: A short code representing the country (e.g., 'US' for the United States).
- **Formatted Language Code**: A combination of the language and country codes (e.g., 'en_US').
- **Currency Symbol**: The symbol used for currency in the locale (e.g., '$' for USD).
- **Decimal Point**: The character used as a decimal point in the locale.
- **Thousands Separator**: The character used to separate thousands in numbers.
- **Date Format**: The format used for dates in the locale.
- **Time Format**: The format used for times in the locale.
- **Radix Character**: The character used as a radix point (decimal point).
- **Regular Expressions for Yes/No**: Regular expressions used to recognize positive and negative responses.
- **Currency String**: A string representing the currency, including its position relative to the value.
- **Era Information**: Information about eras used in the locale (if applicable).
- **Era-Based Date/Time Formats**: Formats for dates and times based on eras.
- **Alternative Digits**: Symbols used to represent digits in the locale.

### Graphical Interface

The `localemembers` module includes an elegant and sleek graphical interface, created with PyQt5, to display localization information to the user. The graphical interface is maximized at startup and the components are dynamic.

#### Example of the Graphical Interface

```python
import localemembers

# To run the graphical interface
localemembers.gui_main()
```

#### Graphical Interface Features

- **Maximized Window**: The window is maximized at startup for better visibility.
- **Dynamic Components**: The components in the interface are dynamic and update based on the system's locale information.
- **User-Friendly Layout**: The layout is designed to be user-friendly and easy to navigate.

### Project Structure

The `localemembers` project has the following structure:

```
localemembers/
├── localemembers/
│   ├── __init__.py
│   ├── locale_members.py
│   ├── gui.py
├── tests/
│   ├── __init__.py
│   └── test_locale_members.py
├── .gitignore
├── LICENSE
├── localemembers.tr
├── main.py
├── README.md
├── requirements.txt
└── setup.py
```

#### Description of Files

- **`localemembers/__init__.py`**: Initializes the `localemembers` module.
- **`localemembers/locale_members.py`**: Contains the main functionality for detecting and formatting localization information.
- **`localemembers/gui.py`**: Contains the code for the graphical interface.
- **`tests/__init__.py`**: Initializes the test module.
- **`tests/test_locale_members.py`**: Contains unit tests for the `localemembers` module.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.
- **`LICENSE`**: Contains the license information for the project.
- **`localemembers.tr`**: Translation file (if applicable).
- **`main.py`**: Main script to run the module.
- **`README.md`**: Contains the documentation for the project.
- **`requirements.txt`**: Lists the dependencies required for the project.
- **`setup.py`**: Contains the setup configuration for the project.

### Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Open a pull request on the main repository.

Please ensure that your code adheres to the project's coding standards and passes all tests.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.