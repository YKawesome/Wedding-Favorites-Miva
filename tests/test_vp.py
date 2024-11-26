import unittest
from volume_pricing import HIGHEST_BREAKPOINT, convert_to_miva, _cleanse_data, _fill_row, _fil_rows

class TestVolumePricing(unittest.TestCase):

    def test_convert_to_miva_basic(self):
        input_data = '1234#1|5|10^6|10|20\n5678#1|5|10^6|10|20'
        header, rows = convert_to_miva(input_data)

        self.assertEqual(header, ['PRICE_GROUP', 'PRODUCT_CODE'] + [str(i) for i in range(1, 301)])
        self.assertEqual(rows[0][:9], ['VolumePricing', '1234', '10', '10', '10', '10', '10', '20', '20'])
        self.assertEqual(rows[1][:9], ['VolumePricing', '5678', '10', '10', '10', '10', '10', '20', '20'])

    def test_convert_to_miva_large_range(self):
        input_data = '2345#1|100|5.00^101|200|4.00\n3456#50|150|3.50^151|300|2.50'
        header, rows = convert_to_miva(input_data)
        self.assertEqual(header, ['PRICE_GROUP', 'PRODUCT_CODE'] + [str(i) for i in range(1, 301)])
        expected_row_1 = ['VolumePricing', '2345'] + ['5.00'] * 100 + ['4.00'] * 100 + [''] * 100
        expected_row_2 = ['VolumePricing', '3456'] + [''] * 49 + ['3.50'] * 101 + ['2.50'] * 150
        self.assertEqual(rows, [expected_row_1, expected_row_2])

    def test_convert_to_miva_no_pricing_data(self):
        input_data = '4567#'
        header, rows = convert_to_miva(input_data)
        self.assertEqual(header, ['PRICE_GROUP', 'PRODUCT_CODE'] + [str(i) for i in range(1, 301)])
        self.assertEqual(rows, [['VolumePricing', '4567'] + [''] * 300])

    def test_cleanse_data_removes_carriage_returns(self):
        input_data = '1234#1|5|10^6|10|20\r\n5678#1|5|10^6|10|20'
        cleansed_data = _cleanse_data(input_data)
        self.assertEqual(cleansed_data, '1234#1|5|10^6|10|205678#1|5|10^6|10|20')

    def test_cleanse_data_handles_empty_string(self):
        input_data = ''
        cleansed_data = _cleanse_data(input_data)
        self.assertEqual(cleansed_data, '')

    def test_cleanse_data_preserves_valid_data(self):
        input_data = '1234#1|5|10^6|10|20'
        cleansed_data = _cleanse_data(input_data)
        self.assertEqual(cleansed_data, '1234#1|5|10^6|10|20')

    def test_fill_row_basic(self):
        row = _fill_row('1234', ['1|5|10', '6|10|20'])
        self.assertEqual(row, ['VolumePricing', '1234', '10', '10', '10', '10', '10', '20', '20', '20', '20', '20'] + [''] * (HIGHEST_BREAKPOINT - 10))

    def test_fill_row_edge_case_full_range(self):
        row = _fill_row('2345', ['1|300|15.00'])
        self.assertEqual(row, ['VolumePricing', '2345'] + ['15.00'] * HIGHEST_BREAKPOINT)

    def test_fill_row_edge_case_empty_pricing_data(self):
        row = _fill_row('4567', [])
        self.assertEqual(row, ['VolumePricing', '4567'] + ['']*HIGHEST_BREAKPOINT)

    def test_fill_rows_basic(self):
        input_data = '1234#1|5|10^6|10|20\n5678#1|5|10^6|10|20'
        rows = _fill_rows(input_data)
        expected_rows = [
            ['VolumePricing', '1234', '10', '10', '10', '10', '10', '20', '20', '20', '20', '20'] + [''] * (HIGHEST_BREAKPOINT - 10),
            ['VolumePricing', '5678', '10', '10', '10', '10', '10', '20', '20', '20', '20', '20'] + [''] * (HIGHEST_BREAKPOINT - 10),
        ]
        self.assertEqual(rows, expected_rows)

    def test_fill_rows_multiple_breakpoints(self):
        input_data = '2345#1|100|5.00^101|200|4.00\n3456#50|150|3.50^151|300|2.50'
        rows = _fill_rows(input_data)
        expected_row_1 = ['VolumePricing', '2345'] + ['5.00'] * 100 + ['4.00'] * 100 + [''] * 100
        expected_row_2 = ['VolumePricing', '3456'] + [''] * 49 + ['3.50'] * 101 + ['2.50'] * 150
        self.assertEqual(rows, [expected_row_1, expected_row_2])

    def test_fill_rows_empty_input(self):
        input_data = ''
        rows = _fill_rows(input_data)
        self.assertEqual(rows, [])


if __name__ == '__main__':
    unittest.main()
