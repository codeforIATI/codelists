# Taux de change

Les données historiques sur les taux de change sont essentielles pour pouvoir interpréter les données financières historiques publiées dans des devises différentes.

Il existe un certain nombre de sources accessibles au public pour les données de taux de change. Vous pouvez télécharger un extrait complet des données sur les taux de change de l'OCDE et de la Réserve fédérale dans un seul jeu de données. Ce jeu de données est actualisé automatiquement chaque nuit.

Ce badge indique le statut de cette processus:

[![Generation Status](https://github.com/codeforIATI/exchangerates-scraper/workflows/Get%20exchange%20rates%20data/badge.svg?branch=main)](https://github.com/codeforIATI/exchangerates-scraper/actions?query=workflow%3A%22Get+exchange+rates+data%22)

[Téléchargez les données ici](https://codeforiati.org/exchangerates-scraper/consolidated.csv)

### Colonnes

| Colonne | Description |
| ------ | ----------- |
| Date | La date du taux de change (équivalente à la `value-date` dans les transactions et les budgets de l'IATI) |
| Rate | Le taux de change de cette devise en USD |
| Currency | Le code de cette devise (selon «ISO 4217» - par exemple, `EUR` ou `GBP`) |
| Frequency | Indique si ce taux de change correspond à une date exacte/quotidienne (`D`) ou à une moyenne mensuelle (`M`) | |
| Source | La source de ces données, soit l'OCDE (`OECD`) ou la [Banque fédérale de réserve de Saint-Louis](https://fred.stlouisfed.org) (`FRED`) |

### Sélection de la meilleure date

Étant donné que plusieurs sources sont incluses dans le jeu de données, vous voudriez peut-être utiliser une formule pour accorder une préférence plus grande à certaines sources. Par exemple, vous pourriez préférer les taux quotidiens de FRED aux taux mensuels de l’OCDE, tout en conservant les taux de l’OCDE comme option de rechange s’il n’y a rien d’autre disponible (par exemple, pour des taux de change très anciens).
