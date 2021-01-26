# Exchange Rates

Historical exchange rates data is essential for being able to interpret historical financial data published in different currencies.

There are a number of publicly available sources for exchange rates data. You can retrieve a full extract of exchange rates data from the OECD and the Federal Reserve from a single dataset which is automatically generated each night. The below badge shows the current status of this nightly update process:

[![Generation Status](https://github.com/codeforIATI/exchangerates-scraper/workflows/Get%20exchange%20rates%20data/badge.svg?branch=main)](https://github.com/codeforIATI/exchangerates-scraper/actions?query=workflow%3A%22Get+exchange+rates+data%22)

[Download the data here.](https://codeforiati.org/exchangerates-scraper/consolidated.csv)

### Columns

| Column | Description |
| ------ | ----------- |
| Date | The date of the exchange rate (equivalent to `value-date` in IATI transactions and budgets) |
| Rate | The rate of this currency to USD |
| Currency | The currency code for this currency (according to `ISO 4217`) |
| Frequency | Whether this currency is a daily date (`D`) or a monthly average (`M`) |
| Source | The source of this data, currently OECD (`OECD`) or the [Federal Reserve Bank of St Louis](https://fred.stlouisfed.org) (`FRED`) |

### Selecting the best date

Because multiple sources are used, you may wish to use a formula to prefer certain sources over others. For example, you may significantly prefer the daily rates from FRED to the monthly rates from the OECD, but still have the OECD rates as a fallback option if there's nothing else available (e.g. for very old rates).
