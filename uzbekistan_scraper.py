#!/usr/bin/env python3

import logging
import os
import pandas
import re
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from time import time
from uzbekistan_settings import *


def verify_purchase_type(purchase_type):
    if purchase_type == 'tender':
        purchase_type = 'tender2'
    elif purchase_type == 'competitive':
        pass
    else:
        logging.error('Purchase type can be only tender or competitive.')
        raise ValueError('Purchase type can be only tender or competitive.')
    return purchase_type


def verify_date(start_date, end_date):
    start_date = datetime.strptime(start_date, '%d.%m.%Y')
    end_date = datetime.strptime(end_date, '%d.%m.%Y')
    if abs((end_date - start_date).days) > 90:
        logging.error("Difference between dates shouldn't be more than 90 days.")
        raise ValueError("Difference between dates shouldn't be more than 90 days.")


def get_general_table(purchase_type, start_date, end_date):
    start_time = time()
    uzbekistan_entrypoint = f'{ENTRY_POINT}/ru/ajax/filter?LotID=&PriceMin=&PriceMax=&RegionID=&TypeID=&DistrictID=&INN=&CategoryID=&EndDate={end_date}&PageSize=5000&Src=AllMarkets&PageIndex=1&Type={purchase_type}&Tnved=&StartDate={start_date}'
    response = requests.get(uzbekistan_entrypoint, headers=HEADERS, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls_list = [ENTRY_POINT + url['href'] for url in soup.select(SELECT_GENERAL_URLS)]
    general_table = list()
    general_table_dict = OrderedDict()
    general_table_dict[LOT_ID] = [soup.select(SELECT_LOT_ID)[idx].get_text().strip() for idx, _ in
                                  enumerate(soup.select(SELECT_LOT_ID))]
    general_table_dict[LOT_END_DATE] = [soup.select(SELECT_LOT_END_DATE)[idx].get_text().strip() for idx, _ in
                                        enumerate(soup.select(SELECT_LOT_END_DATE))]
    general_table_dict[LOT_REGION] = [soup.select(SELECT_LOT_REGION)[idx].get_text().strip() for idx, _ in
                                      enumerate(soup.select(SELECT_LOT_REGION))]
    general_table_dict[LOT_DISTRICT] = [soup.select(SELECT_LOT_DISTRICT)[idx].get_text().strip() for idx, _ in
                                        enumerate(soup.select(SELECT_LOT_DISTRICT))]
    general_table_dict[LOT_NAME] = [soup.select(SELECT_LOT_NAME)[idx].get_text().strip() for idx, _ in
                                    enumerate(soup.select(SELECT_LOT_NAME))]
    general_table_dict[LOT_START_PRICE] = [soup.select(SELECT_LOT_START_PRICE)[idx].get_text().strip().replace(' ', '')
                                           for idx, _ in
                                           enumerate(soup.select(SELECT_LOT_START_PRICE))]
    record_general_table(general_table_dict, purchase_type, start_date, end_date)
    general_table.append(pandas.DataFrame(general_table_dict))
    end_time = time()
    print(
        f'General table for {start_date}-{end_date} has been downloaded in {end_time - start_time:.2f} seconds.')
    logging.info(
        f'General table for {start_date}-{end_date} has been downloaded in {end_time - start_time:.2f} seconds.')
    return urls_list


def get_detailed_table(urls_list):
    detailed_table = list()
    for url in urls_list:
        try:
            start_time = time()
            response = requests.get(url, headers=HEADERS, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            detailed_table_dict = OrderedDict()
            detailed_table_dict[LOT_ID] = soup.select(SELECT_LOT_ID_DETAILED)[0].get_text().strip()
            detailed_table_dict[LOT_NAME] = [
                re.search(REGEXP_LOT_NAME_DETAILED, soup.select(SELECT_LOT_NAME_DETAILED)[idx].get_text())[0].strip()
                for idx, _ in enumerate(soup.select(SELECT_LOT_NAME_DETAILED))]
            detailed_table_dict[LOT_DESCRIPTION] = [
                re.search(REGEXP_LOT_DESCRIPTION, soup.select(SELECT_LOT_DESCRIPTION)[idx].get_text())[0].strip() for
                idx, _ in enumerate(soup.select(SELECT_LOT_DESCRIPTION))]
            detailed_table_dict[LOT_NUMBER] = [soup.select(SELECT_LOT_NUMBER)[idx].get_text().strip() for idx, _ in
                                               enumerate(soup.select(SELECT_LOT_NUMBER))]
            detailed_table_dict[LOT_MEASUREMENT] = [soup.select(SELECT_LOT_MEASUREMENT)[idx].get_text().strip() for
                                                    idx, _ in enumerate(soup.select(SELECT_LOT_MEASUREMENT))]
            detailed_table_dict[LOT_START_PRICE] = [
                soup.select(SELECT_LOT_START_PRICE_DETAILED)[idx].get_text().strip().replace(' ', '')
                for idx, _ in
                enumerate(soup.select(SELECT_LOT_START_PRICE_DETAILED))]
            detailed_table_dict[LOT_TOTAL_START_PRICE] = [
                soup.select(SELECT_LOT_TOTAL_START_PRICE)[idx].get_text().strip().replace(' ', '') for idx, _ in
                enumerate(soup.select(SELECT_LOT_TOTAL_START_PRICE))]
            detailed_table_dict[LOT_CUSTOMER_NAME] = soup.select(SELECT_LOT_CUSTOMER_NAME)[0].get_text().strip()
            detailed_table_dict[LOT_CUSTOMER_RESPONSIBLE] = soup.select(SELECT_LOT_CUSTOMER_RESPONSIBLE)[
                0].get_text().strip()
            detailed_table_dict[LOT_CUSTOMER_DOCUMENT] = soup.select(SELECT_LOT_CUSTOMER_DOCUMENT)[0].get_text().strip()
            detailed_table_dict[LOT_CUSTOMER_ADDRESS] = soup.select(SELECT_LOT_CUSTOMER_ADDRESS)[0].get_text().strip()
            detailed_table_dict[LOT_FINANCING] = soup.select(SELECT_LOT_FINANCING)[0].get_text().strip()
            detailed_table_dict[LOT_SHIPPING] = soup.select(SELECT_LOT_SHIPPING)[0].get_text().strip()
            detailed_table_dict[LOT_TERM] = soup.select(SELECT_LOT_TERM)[0].get_text().strip()
            detailed_table_dict[LOT_START_DATE] = soup.select(SELECT_LOT_START_DATE)[0].get_text().strip()
            detailed_table_dict[LOT_END_DATE] = soup.select(SELECT_LOT_END_DATE_DETAILED)[0].get_text().strip()
            detailed_table_dict[LOT_LAST_PROPOSAL_TIME] = soup.select(SELECT_LOT_LAST_PROPOSAL_TIME)[
                0].get_text().strip()
            detailed_table_dict[LOT_CUSTOMER_TELEPHONE] = soup.select(SELECT_LOT_CUSTOMER_TELEPHONE)[
                0].get_text().strip()
            lot_documents = ENTRY_POINT + soup.select(SELECT_LOT_DOCUMENTS)[0]['href']
            record_detailed_table([detailed_table_dict], detailed_table_dict[LOT_ID], lot_documents)
            detailed_table.append(pandas.DataFrame(detailed_table_dict))
            end_time = time()
            print(f'Lot {detailed_table_dict[LOT_ID]} info has been downloaded in {end_time - start_time:.2f} seconds.')
            logging.info(
                f'Lot {detailed_table_dict[LOT_ID]} info has been downloaded in {end_time - start_time:.2f} seconds.')
        except IndexError:
            print('Page is not found. Probably, it wad deleted.')
            logging.error('Page is not found. Probably, it was deleted.')
            continue
    return detailed_table


def record_general_table(general_table_dict, purchase_type, start_date, end_date):
    if not os.path.exists(PATH_TO_LOCATION):
        os.makedirs(PATH_TO_LOCATION)
    pandas.DataFrame(general_table_dict).to_csv(
        PATH_TO_LOCATION + f'{purchase_type}_purchases_{start_date}-{end_date}.csv')


def record_detailed_table(detailed_table_dict, lot_id, lot_documents_url):
    lot_location = f'{PATH_TO_LOCATION}/{lot_id}/'
    if not os.path.exists(lot_location):
        os.makedirs(lot_location)
    pandas.DataFrame(detailed_table_dict).to_csv(lot_location + lot_id + '.csv')
    response = requests.get(lot_documents_url, headers=HEADERS, verify=False)
    try:
        with open(f"{lot_location}{lot_id}.{lot_documents_url.split('.')[-1]}", 'wb') as f:
            f.write(response.content)
    except FileNotFoundError:
        logging.error("Archive with purchase documentation hasn't been found on the page.")
        return


def get_csv_with_tenders_info(tenders_info, purchase_type, start_date, end_date):
    tenders_output = pandas.concat(tenders_info, ignore_index=True)
    tenders_output.index.name = 'id'
    if not os.path.exists(PATH_TO_LOCATION):
        os.makedirs(PATH_TO_LOCATION)
    tenders_output.to_csv(PATH_TO_LOCATION + f'{purchase_type}_purchases_detailed_{start_date}-{end_date}.csv')


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s', filename='log.txt', filemode='w')
    if len(sys.argv) != 4:
        raise ValueError('Usage: python3 uzbekistan_scraper.py [tender|competitive] [start_date] [end_date]')
    purchase_type = verify_purchase_type(sys.argv[1])
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    verify_date(start_date, end_date)
    start_time = time()
    print('Start downloading')
    logging.info('Start downloading')
    urls_list = get_general_table(purchase_type, start_date, end_date)
    tenders_info = get_detailed_table(urls_list)
    get_csv_with_tenders_info(tenders_info, purchase_type, start_date, end_date)
    end_time = time()
    print(f'Download for {start_date}-{end_date} completed in {end_time - start_time:.2f} seconds.')
    logging.info(f'Download for {start_date}-{end_date} completed in {end_time - start_time:.2f} seconds.')


if __name__ == '__main__':
    main()
