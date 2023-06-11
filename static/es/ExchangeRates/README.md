# Tipos de cambio

Historical exchange rates data is essential for being able to interpret historical financial data published in different currencies.

There are a number of publicly available sources for exchange rates data. You can retrieve a full extract of exchange rates data in 169 currencies from the IMF from a single dataset which is automatically generated each night. The below badge shows the current status of this nightly update process:

[![Generation status](https://github.com/codeforIATI/imf-exchangerates/actions/workflows/pythonapp.yml/badge.svg)](https://github.com/codeforIATI/imf-exchangerates/actions/workflows/pythonapp.yml)

[Download the data here.](https://codeforiati.org/imf-exchangerates/imf_exchangerates.csv)

### Columns

| Column | Description |
| ------ | ----------- |
| Date | The date of the exchange rate (equivalent to `value-date` in IATI transactions and budgets) |
| Rate | The rate of this currency to USD |
| Currency | The currency code for this currency (according to `ISO 4217`) |
| Frequency | Whether this currency is a daily date (`D`) or a monthly average (`M`) |
| Source | The source of this data, always `IMF` |

