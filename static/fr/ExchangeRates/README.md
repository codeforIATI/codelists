# Taux d'Échange

Les données historiques sur les taux de change sont essentielles pour pouvoir interpréter les données financières historiques publiées dans des devises différentes.

Il existe un certain nombre de sources accessibles au public pour les données de taux de change. Vous pouvez télécharger un extrait complet des données sur les taux de change de l'OCDE et de la Réserve fédérale auprès d'[un seul jeu de données publié sur Morph.io](https://morph.io/markbrough/exchangerates-scraper), un site gratuit permettant d'exécuter des &laquo; scrapers &raquo; pour récupérer ce genre de données. Les données sont disponibles au format CSV, sous forme de base de données complète ou via une API interrogeable au format JSON, CSV ou ATOM. Le scraper enregistre également la première fois que des données particulières ont été récupérées, afin que vous puissiez régulièrement demander une mise à jour par rapport à la dernière fois que vous avez récupéré des données.

Pour télécharger les données, ou bien utiliser l'API:
1. Visitez le scraper: [https://morph.io/markbrough/exchangerates-scraper](https://morph.io/markbrough/exchangerates-scraper)
2. Connectez-vous avec Github (si vous n'avez pas de compte, vous pouvez en créer un gratuitement)
3. Téléchargez les données ou [y accéder via l'API](https://morph.io/documentation/api?scraper=markbrough%2Fexchangerates-scraper)

### Colonnes

| Colonne | Description |
| ------ | ----------- |
| Date | La date du taux de change (équivalente à la `value-date` dans les transactions et les budgets de l'IATI) |
| Rate | Le taux de change de cette devise en USD |
| Currency | Le code de cette devise (selon «ISO 4217» - par exemple, `EUR` ou `GBP`) |
| Frequency | Que ce taux de change soit sur une date exacte/quotidienne (`D`) ou une mensuel moyen (`M`) | |
| Source | La source de ces données, soit l'OCDE (`OECD`) ou la [Banque fédérale de réserve de Saint-Louis](https://fred.stlouisfed.org) (`FRED`) |
| RateFirstSeen | La date / heure de la première récupération de ce taux de change par l'API |

### Sélection de la meilleure date

Étant donné que plusieurs sources sont incluses dans le jeu de données, vous voudriez peut-être utiliser une formule pour accorder une préférence plus grande à certains sources. Par exemple, vous pourriez préférer les taux quotidiens de FRED aux taux mensuels de l’OCDE, tout en conservant les taux de l’OCDE comme option de rechange s’il n’ya rien d’autre disponible (par exemple, pour des taux de change très anciens).
