# volume_pricing.py
# Author: Yousef Khan
# Description: This script takes a string of Weiland input data
# and converts it into a list of lists in the Miva format.

import csv

HIGHEST_BREAKPOINT = 300


def convert_and_write_to_csv(ifile: str, ofile: str) -> None:
    '''Converts the input data to Miva format and writes it to a CSV file'''
    with open(ifile, 'r') as input_data:
        _write_to_csv(*convert_to_miva(input_data.read()), ofile)


def convert_to_miva(input_data: str) -> tuple[list[str], list[list[str]]]:
    '''Takes a string of Weiland input data and
    returns a tuple of header and rows in the Miva format'''
    input_data = _cleanse_data(input_data)

    header = ["PRICE_GROUP", "PRODUCT_CODE"] + [str(i) for i in range(1, HIGHEST_BREAKPOINT + 1)]
    rows = _fill_rows(input_data)

    return header, rows


def _write_to_csv(header: list[str], rows: list[list[str]], filename: str) -> None:
    '''Writes the header and rows to a CSV file'''
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(rows)


def _cleanse_data(input_data: str) -> str:
    '''Cleanses the input data by removing unwanted characters'''
    return input_data.replace('\r\n', '').replace('\\r\\n', '')


def _fill_row(product_code: str, pricing_data: list[str]) -> list[str]:
    '''Fills a row with the pricing data'''
    row = ['VolumePricing', product_code] + [''] * HIGHEST_BREAKPOINT
    for data in pricing_data:
        if data:
            qty_start, qty_end, price = data.split('|')
            qty_start = int(qty_start)
            qty_end = HIGHEST_BREAKPOINT if qty_end == '+' else int(qty_end)

            for i in range(qty_start, qty_end + 1):
                row[i + 1] = price

    return row


def _fill_rows(input_data: str) -> list[list[str]]:
    '''Fills the rows with the input data'''
    rows = []

    for line in input_data.split('\n'):
        if line == '':
            continue
        parts = line.split('#')
        product_code = parts[0].strip()
        volume_pricing = parts[1].strip()

        row = _fill_row(product_code, volume_pricing.split('^'))
        rows.append(row)

    return rows


__all__ = ['convert_and_write_to_csv', 'convert_to_miva']


if __name__ == '__main__':
    # file = input('Enter the input file [test or actual]: ')
    convert_and_write_to_csv('data/test_data.txt', 'output/output.csv')
