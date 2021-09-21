# Uzbekistan and Kazakhstan state purchases scraper
A scraper to get information about Uzbekistan and Kazakhstan state purchases.

## Requirements
### Python
A program has been written and tested on python3.8, but should work on python3.6+ versions.
Create and activate a virtual environment before you start:

`python3 -m venv venv`

`source venv/bin/activate`

Then install required modules:

`pip3 install -r requirements.txt`


## Usage
### Uzbekistan
Scraper designed to run as a command-line utility. It receives type of purchases (tender or competitive), start and end date as two parameters in format `dd.mm.YYYY`.
For example, `python3 uzbekistan_scraper.py tender 01.01.2021 31.01.2021`.

There is a limitation in 30-days search period. If you need longer time period, please, run scraper several times.
There is a limitation in 5000 results per search due to service reliability.

There are three entities you will get in result:
* *purchase_type*_*date*.csv — general information about purchases on *date*;
* *purchase_type*_detailed_*date*.csv — detailed information about each purchase on *date*;
* directory *purchase_id* with *purchase_id*.csv and *purchase_id*.zip — detailed information about purchase as in common file and archive with purchase documentation.


### Kazakhstan
Scraper designed to run as a command-line utility. It receives search query as parameter.
If your query consists of two words and more, please, take it into quotes.
For example, `python3 kazakhstan_scraper.py "доступная среда"`.

There is a result limitation in a 2000 announces due to service reliability.

There are three entities you will get in result:
* tenders_*query*.csv — general information about tenders with *query*;
* tenders_detailed_*query*.csv — detailed information about each tender with *query*;
* directory tenders/ with *announce_id*.csv — detailed information about tender as in common file.
