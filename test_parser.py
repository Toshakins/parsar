import unittest
from main import background_url_declaration, declaration_list


class ParserTestCase(unittest.TestCase):
    def test_quotation_marks(self):
        parse_result = background_url_declaration.parse(
            'background-image : url("ololo")')
        self.assertEqual(parse_result, ('background-image', 'ololo'))

    def test_simple_case_works(self):
        parse_reuls = background_url_declaration.parse(
            'background-image : url(\'ololo\')')
        parse_result = parse_reuls
        self.assertEqual(parse_result, ('background-image', 'ololo'))

    def test_rule_on_background(self):
        parse_results = declaration_list.parse(
            'background-image : url(\'ololo\');'
        )
        self.assertEqual(parse_results, [('background-image', 'ololo')])

    def test_rule_on_smth(self):
        parse_results = declaration_list.parse(
            'ololo: wtf;'
        )
        self.assertEqual(parse_results, [('ololo', 'wtf')])

    def test_parse_multiple_rules_background_prepend(self):
        parse_results = declaration_list.parse(
            'background-image : url(\'ololo\'); width: 100px;'
        )
        self.assertEqual(parse_results,
                         [('background-image', 'ololo'), ('width', '100px')])

    def test_parse_multiple_rules_background_postpend(self):
        parse_results = declaration_list.parse(
            'width: 100px;background-image : url(\'ololo\');'
        )
        self.assertEqual(parse_results,
                         [('width', '100px'), ('background-image', 'ololo')])


if __name__ == '__main__':
    unittest.main()
