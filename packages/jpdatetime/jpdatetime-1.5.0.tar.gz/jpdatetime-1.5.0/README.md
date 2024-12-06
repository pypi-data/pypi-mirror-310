# JapaneseDatetime
[![Test](https://github.com/new-village/cnparser/actions/workflows/test.yaml/badge.svg)](https://github.com/new-village/cnparser/actions/workflows/test.yaml)
![PyPI - Version](https://img.shields.io/pypi/v/jpdatetime)

The `jpdatetime` library extends Python's `datetime` to support Japanese eras (元号). It allows parsing and formatting dates using Japanese era names like Reiwa (令和), Heisei (平成), and more, including special support for first-year notation (元年).

## Features
- **Parsing**: Convert Japanese era date strings to Gregorian dates using the strptime method. This method supports date strings that include full-width characters and can handle years, months, and days written in kanji numerals.
- **Formatting**: Convert Gregorian dates to Japanese era formatted strings using the `strftime` method.
- **Supported Eras**: Support for conversion of eras from Reiki (霊亀), which began on October 3, 715, to Reiwa (令和).
- **First Year Notation**: Supports the first-year notation (元年) for each era.

## Installation
`jpdatetime` is available for installation via pip.
```shell
$ python -m pip install jpdatetime
```
  
### GitHub Install
Installing the latest version from GitHub:  
```shell
$ git clone https://github.com/new-village/JapaneseDatetime
$ cd JapaneseDatetime
$ python setup.py install
```
    
## Usage
```python
from jpdatetime import jpdatetime

# Parsing Japanese era date string to a datetime object
date_string = "平成三〇年十二月二四日"
format_string = "%G年%m月%d日"
date_obj = jpdatetime.strptime(date_string, format_string)
print(date_obj)  # Output: 2018-12-24 00:00:00

# Formatting a datetime object to a Japanese era date string
date = jpdatetime(2024, 10, 30)
formatted_date = date.strftime("%G年%m月%d日")
print(formatted_date)  # Output: "令和06年10月30日"

# Handling the first year of an era
date_string = "令和元年5月1日"
format_string = "%G年%m月%d日"
date_obj = jpdatetime.strptime(date_string, format_string)
print(date_obj)  # Output: 2019-05-01 00:00:00

# Formatting a datetime object for the first year of an era
date = jpdatetime(2019, 5, 1)
formatted_date = date.strftime("%G年%m月%d日")
print(formatted_date)  # Output: "令和元年5月1日"

# Using abbreviated era names
date_string = "令1年10月30日"
format_string = "%g年%m月%d日"
date_obj = jpdatetime.strptime(date_string, format_string)
print(date_obj)  # Output: 2019-10-30 00:00:00

date = jpdatetime(2019, 10, 30)
formatted_date = date.strftime("%g年%m月%d日")
print(formatted_date)  # Output: "令1年10月30日"

# Using English era names
date_string = "Heisei 30, April 1"
format_string = "%E, %B %d"
date_obj = jpdatetime.strptime(date_string, format_string)
print(date_obj)  # Output: 2018-04-01 00:00:00

date = jpdatetime(2018, 4, 1)
formatted_date = date.strftime("%E, %B %d")
print(formatted_date)  # Output: "Heisei 30, April 01"

# Using abbreviated English era names
date_string = "R1/05/01"
format_string = "%e/%m/%d"
date_obj = jpdatetime.strptime(date_string, format_string)
print(date_obj)  # Output: 2019-05-01 00:00:00

date = jpdatetime(2019, 5, 1)
formatted_date = date.strftime("%e/%m/%d")
print(formatted_date)  # Output: "R1/05/01"
```

### `strftime()` and `strptime()` Format Codes 

| Directive | Meaning | Example |
|-------------|-------------|-----------------|
| `%G` | Full Japanese era name with year. Displays "令和元" for the first year and "平成30" for other years. | 令和元, 平成30 |
| `%-G`/`%#G` | Full Japanese era name with year (without zero-padding). Displays non-zero-padded numbers for other years (e.g., "平成6"). | 令和2, 平成6 |
| `%g` | Abbreviated Japanese era name (first character) with year. Shows "令01" for the first year and zero-padded numbers for other years (e.g., "平30"). | 令01, 平30 |
| `%-g`/`%#g` | Abbreviated Japanese era name with year (without zero-padding). Shows "令1" for the first year and non-zero-padded numbers for other years (e.g., "平30"). | 令1, 平6 |
| `%E` | Full English era name with year. Displays "Reiwa 01" for the first year and "Heisei 30" for other years. | Reiwa 01, Heisei 30 |
| `%-E`/`%#E` | Full English era name with year (without zero-padding). Displays "Reiwa 1" for the first year and non-zero-padded numbers for other years (e.g., "Heisei 30"). | Reiwa 1, Heisei 30 |
| `%e` | Abbreviated English era name (first letter) with year. Shows "R01" for the first year and "H30" for other years. | R01, H30 |
| `%-e`/`%#e` | Abbreviated English era name with year (without zero-padding). Shows "R1" for the first year and non-zero-padded numbers for other years (e.g., "H30"). | R1, H30 |

`%Y`, `%m`, `%d`, `%B`, etc.: [Standard datetime format](https://docs.python.org/3/library/datetime.html#format-codes) specifiers.

## Limitation
- **Supported Eras**: The library supports Reiki (from October 3, 715) onwards. Eras prior to Reiki are not supported.
- **Future Eras**: The library does not account for hypothetical future eras not explicitly defined in the eras list.
- **Conversion rule of abbrivation Era**: When converting from abbreviated era names (such as Rei, Hei, or R, H) to a date-time format, duplicate initial letters may exist among era names. In cases of duplication, the conversion defaults to the newer era.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements.

## Reference

The era conversion in this library is based on the [List of Japanese Eras on Wikipedia](https://ja.wikipedia.org/wiki/%E5%85%83%E5%8F%B7%E4%B8%80%E8%A6%A7_(%E6%97%A5%E6%9C%AC)).

## License

This project is licensed under the Apache-2.0 license.
