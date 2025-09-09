---
title: Taux de change
---

# Taux de change

Les données historiques sur les taux de change sont essentielles pour pouvoir interpréter les données financières historiques publiées dans des devises différentes.

Il existe un certain nombre de sources accessibles au public pour les données de taux de change. Vous pouvez télécharger un extrait complet des données sur les taux de change du FMI dans un seul jeu de données. Ce jeu de données est actualisé automatiquement chaque nuit.

Ce badge indique le statut de cette processus:

[![Generation Status](https://github.com/codeforIATI/imf-exchangerates/workflows/Generate%20IMF%20currencies%20data/badge.svg?branch=main)](https://github.com/codeforIATI/imf-exchangerates/actions?query=workflow%3A%22Generate+IMF+currencies+data%22)

[Téléchargez les données ici](https://codeforiati.org/imf-exchangerates/imf_exchangerates.csv)

### Colonnes

| Colonne | Description |
| ------ | ----------- |
| Date | La date du taux de change (équivalente à la `value-date` dans les transactions et les budgets de l'IATI) |
| Rate | Le taux de change de cette devise en USD |
| Currency | Le code de cette devise (selon «ISO 4217» - par exemple, `EUR` ou `GBP`) |
| Frequency | Indique si ce taux de change correspond à une date exacte/quotidienne (`D`) ou à une moyenne mensuelle (`M`) | |
| Source | La source de ces données, le FMI (`IMF`) |
