#!/usr/bin/env python3

ENTRY_POINT = 'https://dxarid.uzex.uz'
SELECT_GENERAL_URLS = 'tr > td:nth-of-type(2) > a'
PATH_TO_LOCATION = 'uzbekistan/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'}

LOT_ID = '№ лота'
LOT_END_DATE = 'Дата окончания'
LOT_REGION = 'Регион'
LOT_DISTRICT = 'Район'
LOT_NAME = 'Наименование заказа'
LOT_START_PRICE = 'Стартовая стоимость'
LOT_DESCRIPTION = 'Подробное описание'
LOT_NUMBER = 'Количество товара'
LOT_MEASUREMENT = 'Единица измерения'
LOT_TOTAL_START_PRICE = 'Итого стартовая стоимость'
LOT_CUSTOMER_NAME = 'Наименование заказчика'
LOT_CUSTOMER_RESPONSIBLE = 'Ответственное лицо заказчика'
LOT_CUSTOMER_DOCUMENT = 'ИНН'
LOT_CUSTOMER_ADDRESS = 'Адрес'
LOT_FINANCING = 'Источники финансирования предмета'
LOT_SHIPPING = 'Место поставки'
LOT_TERM = 'Срок поставки'
LOT_START_DATE = 'Дата начала'
LOT_LAST_PROPOSAL_TIME = 'День и время последнего предложения'
LOT_CUSTOMER_TELEPHONE = 'Телефон'

SELECT_LOT_ID = 'tr > td:nth-of-type(2) > a'
SELECT_LOT_END_DATE = 'tr > td:nth-of-type(3)'
SELECT_LOT_REGION = 'tr > td:nth-of-type(4)'
SELECT_LOT_DISTRICT = 'tr > td:nth-of-type(5)'
SELECT_LOT_NAME = 'tr > td:nth-of-type(6) > a > span'
SELECT_LOT_START_PRICE = 'tr > td:nth-of-type(7)'
SELECT_LOT_ID_DETAILED = 'p.form_title > strong'
SELECT_LOT_NAME_DETAILED = 'h3.min_title'
SELECT_LOT_DESCRIPTION = 'h3 + div.full_block p'
SELECT_LOT_NUMBER = 'div.full_block p ~ table > tr td:first-of-type'
SELECT_LOT_MEASUREMENT = 'div.full_block p ~ table > tr td:nth-of-type(2)'
SELECT_LOT_START_PRICE_DETAILED = 'div.full_block p ~ table > tr td.table_text_red'
SELECT_LOT_TOTAL_START_PRICE = 'div.full_block table tr td.table_text_green'
SELECT_LOT_CUSTOMER_NAME = 'ul.product_info > li:nth-of-type(1) > div.right_element'
SELECT_LOT_CUSTOMER_RESPONSIBLE = 'ul.product_info > li:nth-of-type(2) > div.right_element'
SELECT_LOT_CUSTOMER_DOCUMENT = 'ul.product_info > li:nth-of-type(3) > div.right_element'
SELECT_LOT_CUSTOMER_ADDRESS = 'ul.product_info > li:nth-of-type(4) > div.right_element'
SELECT_LOT_FINANCING = 'ul.product_info > li:nth-of-type(5) > div.right_element'
SELECT_LOT_SHIPPING = 'ul.product_info > li:nth-of-type(6) > div.right_element'
SELECT_LOT_TERM = 'ul.product_info > li:nth-of-type(8) > div.right_element'
SELECT_LOT_START_DATE = 'ul.product_info > li:nth-of-type(10) > div.right_element'
SELECT_LOT_END_DATE_DETAILED = 'ul.product_info > li:nth-of-type(11) > div.right_element'
SELECT_LOT_LAST_PROPOSAL_TIME = 'ul.product_info > li:nth-of-type(12) > div.right_element'
SELECT_LOT_CUSTOMER_TELEPHONE = 'ul.product_info > li:nth-of-type(17) > div.right_element'
SELECT_LOT_DOCUMENTS = 'a.product_file'

REGEXP_LOT_DESCRIPTION = '(?<=Подробное описание:\\s).+'
REGEXP_LOT_NAME_DETAILED = '(?<=\\d\\s-).+'
