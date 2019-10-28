# Exchange Rates

Historical exchange rates data is essential for being able to interpret historical financial data published in different currencies.

There are a number of publicly available sources for exchange rates data. You can retrieve a full extract of exchange rates data from the OECD and the Federal Reserve from [a single dataset published on Morph.io](https://morph.io/markbrough/exchangerates-scraper), a free site for running scrapers to retrieve this kind of data. The data is available in CSV, as a full database, or via a queryable API in JSON, CSV or ATOM. The scraper also records when particular data was first seen, so that you can occasionally query for any updates since the last time you retrieved data.

To download the data, or use the API:
1. Visit the scraper: [https://morph.io/markbrough/exchangerates-scraper](https://morph.io/markbrough/exchangerates-scraper)
2. Sign in with Github (if you don't have an account, you can create one for free)
3. Download the data, or [access via the API](https://morph.io/documentation/api?scraper=markbrough%2Fexchangerates-scraper)

### Columns

| Column | Description |
| ------ | ----------- |
| Date | The date of the exchange rate (equivalent to `value-date` in IATI transactions and budgets) |
| Rate | The rate of this currency to USD |
| Currency | The currency code for this currency (according to `ISO 4217`) |
| Frequency | Whether this currency is a daily date (`D`) or a monthly average (`M`) |
| Source | The source of this data, currently OECD (`OECD`) or the [Federal Reserve Bank of St Louis](https://fred.stlouisfed.org) (`FRED`) |
| RateFirstSeen | The date/time when the rate was first seen by the scraper API |

### Selecting the best date

Because multiple sources are used, you may wish to use a formula to score rates based on their preference. For example, you may significantly prefer the daily rates from FRED to the monthly rates from the OECD, but still have the OECD rates as a fallback option if there's nothing else available (e.g. for very old rates).
