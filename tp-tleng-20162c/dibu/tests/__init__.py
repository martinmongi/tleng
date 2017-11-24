from unittest import TestCase

from ply import yacc
from ply.lex import lex

from dibu import lexer_rules
from dibu import parse
from dibu import parser_rules
from xml.dom.minidom import parseString as xmlParse

from dibu.exceptions import SyntacticException, SemanticException


class TestTLENG(TestCase):
    def setUp(self):
        self.lexer = lex(module=lexer_rules)
        self.parser = yacc.yacc(module=parser_rules)

    def test_correct_parsing_of_rectangle(self):
        text = 'rectangle upper_left=(0,0), size=(200, 200), fill="yellow" '
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'rectangle')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 3)
        self.assertTrue('rect' in result)
        self.assertTrue('x="0" y="0"' in result)
        self.assertTrue('height="200" width="200"' in result)

    def test_correct_parsing_of_polygon(self):
        # FIXME: Falta la parte del style. Eso es distinto a como dieron el ejemplo.
        text = 'polygon points=[(0,0), (50, 50), (0, 100)]'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'polygon')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 1)
        self.assertTrue('polygon' in result)
        self.assertTrue('points="0,0 50,50 0,100 "' in result)

    def test_correct_parsing_of_line(self):
        text = 'line to=(0, 100), from=(25, 50)'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'line')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 2)
        self.assertTrue('line' in result)
        self.assertTrue('x1="25" y1="50" x2="0" y2="100"' in result)

    def test_correct_parsing_of_circle(self):
        text = 'circle center=(100,100), radius=20'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'circle')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 2)
        self.assertTrue('circle' in result)
        self.assertTrue('radius="20" cx="100" cy="100"' in result)

    def test_correct_parsing_of_polyline(self):
        text = 'polyline points = [(200, 100), (150, 50), (200, 0)]'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'polyline')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 1)
        self.assertTrue('polyline' in result)
        self.assertTrue('points="200,100 150,50 200,0 "' in result)

    def test_correct_parsing_of_size(self):
        text = 'size height=100, width=100'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'size')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 2)
        self.assertTrue('height="100"' in result)
        self.assertTrue('width="100"' in result)

    def test_correct_parsing_of_ellipse(self):
        text = 'ellipse center=(100,100), rx=20, ry=20'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'ellipse')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 3)
        self.assertTrue('ellipse' in result)
        self.assertTrue('ry="20" rx="20" cx="100" cy="100"' in result)

    def test_correct_parsing_of_text_without_optional_parameters(self):
        text = 'text t="esto es un texto", at=(10, 20)'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'text')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 2)
        self.assertTrue('text' in result)
        self.assertTrue('>esto es un texto</text>' in result)
        self.assertTrue('x="10" y="20"' in result)

    def test_correct_parsing_of_text_with_optional_parameters(self):
        text = 'text t="esto es un texto", at=(10, 20), font-family="bakbatn", font-size="12"'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 1)
        self.assertEqual(abstract_syntax_tree.lines[0].identifier, 'text')
        self.assertEqual(len(abstract_syntax_tree.lines[0].parameters), 4)
        self.assertTrue('text' in result)
        self.assertTrue('>esto es un texto</text>' in result)
        self.assertTrue('x="10" y="20"' in result)
        self.assertTrue('style="font-size=12;font-family=bakbatn;"' in result)

    def test_correct_parsing_more_than_one_line(self):
        text = 'line to=(0, 100), from=(25, 50)' \
               'circle center=(100,100), radius=20' \
               'polyline points=[(200, 100), (150, 50), (200, 0)]' \
               'ellipse center=(100,100), rx=20, ry=20'
        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        result = abstract_syntax_tree.evaluate()

        self.assertEqual(len(abstract_syntax_tree.lines), 4)
        self.assertTrue('line' in result)
        self.assertTrue('circle' in result)
        self.assertTrue('polyline' in result)
        self.assertTrue('ellipse' in result)

    def test_invalid_token_raises_exception(self):
        text = 'line to=(0, 100), from=(25, 50)' \
               'circle center=(100,100), radius=20' \
               'polyline points=[(200, 100), (150, 50), (200, 0)], invalid_token="test" ' \
               'ellipse center=(100,100), rx=20, ry=20'

        self.assertRaises(SyntacticException, self.parser.parse, text, self.lexer)

    def test_missing_obligatory_parameter_raises_exception(self):
        # Misses "radius" from circle
        text = 'line to=(0, 100), from=(25, 50)' \
               'circle center=(100,100)' \
               'polyline points=[(200, 100), (150, 50), (200, 0)]' \
               'ellipse center=(100,100), rx=20, ry=20'

        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        self.assertRaises(SemanticException, abstract_syntax_tree.evaluate)

    def test_invalid_parameter_raises_exception(self):
        # Misses "radius" from circle
        text = 'line to=(0, 100), from=(25, 50)' \
               'circle center=(100,100), radius=20, rx=20' \
               'polyline points=[(200, 100), (150, 50), (200, 0)]' \
               'ellipse center=(100,100), rx=20, ry=20'

        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        self.assertRaises(SemanticException, abstract_syntax_tree.evaluate)

    def test_duplicated_parameters_raises_exception(self):
        text = 'line to=(0, 100), from=(25, 50)' \
               'circle center=(100,100), radius=20, radius=220' \
               'polyline points=[(200, 100), (150, 50), (200, 0)]' \
               'ellipse center=(100,100), rx=20, ry=20'

        abstract_syntax_tree = self.parser.parse(text, self.lexer)
        self.assertRaises(SemanticException, abstract_syntax_tree.evaluate)
