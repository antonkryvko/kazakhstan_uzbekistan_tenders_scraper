#!/usr/bin/env python3

import logging
import os
import pandas
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from time import time
from kazakhstan_settings import *


def get_general_table(search_word):
    start_time = time()
    kazakhstan_entrypoint = f'{ENTRY_POINT}/ru/search/lots?filter%5Bname%5D={search_word}&count_record=2000&search' \
                            f'=&filter%5Bnumber%5D' \
                            f'=&filter%5Bnumber_anno%5D=&filter%5Benstru%5D=&filter%5Bcustomer%5D=&filter' \
                            f'%5Bamount_from%5D=&filter%5Bamount_to%5D=&filter%5Btrade_type%5D=&filter%5Bmonth%5D' \
                            f'=&filter%5Bplan_number%5D=&filter%5Bend_date_from%5D=&filter%5Bend_date_to%5D=&filter' \
                            f'%5Bstart_date_to%5D=&filter%5Byear%5D=&filter%5Bitogi_date_from%5D=&filter' \
                            f'%5Bitogi_date_to%5D=&filter%5Bstart_date_from%5D=&filter%5Bmore%5D='
    response = requests.get(kazakhstan_entrypoint, headers=HEADERS, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls_list = [f"{ENTRY_POINT}{url['href']}?tab=lots" for url in soup.select(SELECT_GENERAL_URLS)]
    general_table = list()
    general_table_dict = OrderedDict()
    general_table_dict[LOT_ID] = [soup.select(SELECT_LOT_ID)[idx].get_text().strip() for idx, _ in
                                  enumerate(soup.select(SELECT_LOT_ID))]
    general_table_dict[ANNOUNCE_NAME] = [soup.select(SELECT_ANNOUNCE_NAME)[idx].get_text().strip() for idx, _ in
                                         enumerate(soup.select(SELECT_ANNOUNCE_NAME))]
    general_table_dict[LOT_CUSTOMER] = [idx.next_sibling.strip() for idx in
                                        soup.find_all(SELECT_LOT_CUSTOMER, text=SELECT_LOT_CUSTOMER_SIBLING)]
    general_table_dict[LOT_NAME] = [soup.select(SELECT_LOT_NAME)[idx].get_text().strip() for idx, _ in
                                    enumerate(soup.select(SELECT_LOT_NAME))]
    general_table_dict[LOT_NUMBER] = [soup.select(SELECT_LOT_NUMBER)[idx].get_text().strip() for idx, _ in
                                      enumerate(soup.select(SELECT_LOT_NUMBER))]
    general_table_dict[LOT_PRICE] = [soup.select(SELECT_LOT_PRICE)[idx].get_text().strip().replace(' ', '') for idx, _
                                     in
                                     enumerate(soup.select(SELECT_LOT_PRICE))]
    general_table_dict[LOT_PURCHASE_METHOD] = [soup.select(SELECT_LOT_PURCHASE_METHOD)[idx].get_text().strip() for
                                               idx, _ in
                                               enumerate(soup.select(SELECT_LOT_PURCHASE_METHOD))]
    general_table_dict[LOT_STATUS] = [soup.select(SELECT_LOT_STATUS)[idx].get_text().strip() for idx, _ in
                                      enumerate(soup.select(SELECT_LOT_STATUS))]
    record_general_table(general_table_dict, search_word)
    general_table.append(pandas.DataFrame(general_table_dict))
    end_time = time()
    print(
        f'Urls from general table for {search_word} and the table have been downloaded in {end_time - start_time:.2f} seconds.')
    logging.info(
        f'Urls from general table for {search_word} and the table have been downloaded in {end_time - start_time:.2f} seconds.')
    return urls_list


def get_detailed_table(urls_list):
    detailed_table = list()
    for url in urls_list:
        try:
            start_time = time()
            response = requests.get(url, headers=HEADERS, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            detailed_table_dict = OrderedDict()
            detailed_table_dict[ANNOUNCE_ID] = soup.find_all(SELECT_ANNOUNCE_HEADER)[0]['value']
            detailed_table_dict[ANNOUNCE_NAME] = soup.find_all(SELECT_ANNOUNCE_HEADER)[1]['value']
            detailed_table_dict[ANNOUNCE_STATUS] = soup.find_all(SELECT_ANNOUNCE_HEADER)[2]['value']
            detailed_table_dict[ANNOUNCE_PUBLICATION_DATE] = soup.find_all(SELECT_ANNOUNCE_HEADER)[3]['value']
            detailed_table_dict[ANNOUNCE_START_DATE] = soup.find_all(SELECT_ANNOUNCE_HEADER)[4]['value']
            detailed_table_dict[ANNOUNCE_END_DATE] = soup.find_all(SELECT_ANNOUNCE_HEADER)[5]['value']
            try:
                detailed_table_dict[LOT_ID] = soup.find(SELECT_LOT_HEADER,
                                                        text=SELECT_LOT_ID_DETAILED_SIBLING).next_sibling.strip()
                detailed_table_dict[LOT_NAME] = soup.find(SELECT_LOT_HEADER,
                                                          text=SELECT_LOT_NAME_DETAILED_SIBLING).next_sibling.strip()
                detailed_table_dict[LOT_DESCRIPTION] = soup.find(SELECT_LOT_HEADER,
                                                                 text=SELECT_LOT_DESCRIPTION_SIBLING).next_sibling.strip()
                detailed_table_dict[LOT_DESCRIPTION_DETAILED] = soup.find(SELECT_LOT_HEADER,
                                                                          text=SELECT_LOT_DESCRIPTION_DETAILED_SIBLING).next_sibling.strip()
            except AttributeError:
                detailed_table_dict[LOT_ID] = [soup.select(SELECT_LOT_ID_DETAILED)[idx].get_text().strip() for
                                               idx, _ in
                                               enumerate(soup.select(SELECT_LOT_ID_DETAILED))]
                detailed_table_dict[LOT_NAME] = [soup.select(SELECT_LOT_NAME_DETAILED)[idx].get_text().strip() for
                                                 idx, _ in
                                                 enumerate(soup.select(SELECT_LOT_NAME_DETAILED))]
                detailed_table_dict[LOT_DESCRIPTION] = ''
                detailed_table_dict[LOT_DESCRIPTION_DETAILED] = ''
            detailed_table_dict[LOT_CUSTOMER_NAME] = [soup.select(SELECT_LOT_CUSTOMER_NAME)[idx].get_text().strip() for
                                                      idx, _ in
                                                      enumerate(soup.select(SELECT_LOT_CUSTOMER_NAME))]
            detailed_table_dict[LOT_CHARACTERISTICS_FULL] = [
                soup.select(SELECT_LOT_CHARACTERISTICS_FULL)[idx].get_text().strip() for idx, _ in
                enumerate(soup.select(SELECT_LOT_CHARACTERISTICS_FULL))]
            detailed_table_dict[LOT_PRICE_PER_ONE] = [
                soup.select(SELECT_LOT_PRICE_PER_ONE)[idx].get_text().strip().replace(' ', '') for
                idx, _ in
                enumerate(soup.select(SELECT_LOT_PRICE_PER_ONE))]
            detailed_table_dict[LOT_NUMBER] = [soup.select(SELECT_LOT_NUMBER_DETAILED)[idx].get_text().strip() for
                                               idx, _ in
                                               enumerate(soup.select(SELECT_LOT_NUMBER_DETAILED))]
            detailed_table_dict[LOT_MEASUREMENT] = [soup.select(SELECT_LOT_MEASUREMENT)[idx].get_text().strip() for
                                                    idx, _ in
                                                    enumerate(soup.select(SELECT_LOT_MEASUREMENT))]
            detailed_table_dict[LOT_PLANNED_TOTAL] = [
                soup.select(SELECT_LOT_PLANNED_TOTAL)[idx].get_text().strip().replace(' ', '') for
                idx, _ in
                enumerate(soup.select(SELECT_LOT_PLANNED_TOTAL))]
            detailed_table_dict[LOT_TOTAL_1_YEAR] = [soup.select(SELECT_LOT_TOTAL_1_YEAR)[idx].get_text().strip() for
                                                     idx, _ in
                                                     enumerate(soup.select(SELECT_LOT_TOTAL_1_YEAR))]
            detailed_table_dict[LOT_TOTAL_2_YEAR] = [soup.select(SELECT_LOT_TOTAL_2_YEAR)[idx].get_text().strip() for
                                                     idx, _ in
                                                     enumerate(soup.select(SELECT_LOT_TOTAL_2_YEAR))]
            detailed_table_dict[LOT_TOTAL_3_YEAR] = [soup.select(SELECT_LOT_TOTAL_3_YEAR)[idx].get_text().strip() for
                                                     idx, _ in
                                                     enumerate(soup.select(SELECT_LOT_TOTAL_3_YEAR))]
            detailed_table_dict[LOT_STATUS] = [soup.select(SELECT_LOT_STATUS_DETAILED)[idx].get_text().strip() for
                                               idx, _ in
                                               enumerate(soup.select(SELECT_LOT_STATUS_DETAILED))]
            record_detailed_table(detailed_table_dict, detailed_table_dict[ANNOUNCE_ID])
            detailed_table.append(pandas.DataFrame(detailed_table_dict))
            end_time = time()
            print(f'Lot {detailed_table_dict[ANNOUNCE_ID]} info has been downloaded in {end_time - start_time:.2f} seconds.')
            logging.info(
                f'Lot {detailed_table_dict[ANNOUNCE_ID]} info has been downloaded in {end_time - start_time:.2f} seconds.')
        except IndexError:
            print('Page is not found. Probably, it wad deleted.')
            logging.error('Page is not found. Probably, it was deleted.')
            continue
    return detailed_table


def record_general_table(general_table_dict, search_word):
    if not os.path.exists(PATH_TO_LOCATION):
        os.makedirs(PATH_TO_LOCATION)
    pandas.DataFrame(general_table_dict).to_csv(PATH_TO_LOCATION + f'tenders_{search_word}.csv')


def record_detailed_table(detailed_table_dict, tender_id):
    tender_location = f'{PATH_TO_LOCATION}/tenders/'
    if not os.path.exists(tender_location):
        os.makedirs(tender_location)
    pandas.DataFrame(detailed_table_dict).to_csv(tender_location + tender_id + '.csv')


def get_csv_with_tenders_info(tenders_info, search_word):
    tenders_output = pandas.concat(tenders_info, ignore_index=True)
    tenders_output.index.name = 'id'
    if not os.path.exists(PATH_TO_LOCATION):
        os.makedirs(PATH_TO_LOCATION)
    tenders_output.to_csv(PATH_TO_LOCATION + f'tenders_detailed_{search_word}.csv')


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s', filename='log.txt', filemode='w')
    if len(sys.argv) != 2:
        raise ValueError('Usage: python3 kazakhstan_tenders.py [search_word]. If your search query consists of two '
                         'and more words, take them into quotes.')
    search_word = sys.argv[1]
    start_time = time()
    print('Start downloading')
    logging.info('Start downloading')
    url_list = get_general_table(search_word)
    tenders_info = get_detailed_table(url_list)
    get_csv_with_tenders_info(tenders_info, search_word)
    end_time = time()
    print(f'Download for {search_word} completed in {end_time - start_time:.2f} seconds.')
    logging.info(f'Download for {search_word} completed in {end_time - start_time:.2f} seconds.')


if __name__ == '__main__':
    main()
