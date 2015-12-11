# -*- coding: utf-8 -*-

import unittest
from unittest import SkipTest

import taxonlist2json


class ConverterTest(unittest.TestCase):

    def test_file_into_elements(self):
        raise SkipTest("not tested yet")

    def test_element_into_lines(self):
        'returns only the relevant lines'
        raise SkipTest("not tested yet")

    def test_line_to_binomial_with_simple_author(self):
        s = ' Abuta velutina Gleason'
        result = taxonlist2json.line_to_binomial(s)
        expect = {'object': 'taxon',
                  'rank': 'species',
                  'epithet': 'velutina',
                  'ht-rank': 'genus',
                  'ht-epithet': 'Abuta',
                  'hybrid': False,
                  'author': 'Gleason',
                  }
        self.assertEquals(result, expect)

    def test_line_to_binomial_with_composite_author(self):
        result = taxonlist2json.line_to_binomial(
            'Abutilon mollissimum (Cav.) Sweet')
        expect = {'object': 'taxon',
                  'rank': 'species',
                  'epithet': 'mollissimum',
                  'ht-rank': 'genus',
                  'ht-epithet': 'Abutilon',
                  'hybrid': False,
                  'author': '(Cav.) Sweet',
                  }
        self.assertEquals(result, expect)

    def test_line_to_binomial_author_with_utf8_char(self):
        s = "Abutilon nudiflorum (L'H&eacute;r.) Sweet"
        result = taxonlist2json.line_to_binomial(s)
        expect = {'ht-epithet': 'Abutilon',
                  'rank': 'species',
                  'author': "(L'Hér.) Sweet",
                  'hybrid': False,
                  'object': 'taxon',
                  'epithet': 'nudiflorum',
                  'ht-rank': 'genus'}
        self.assertEquals(result, expect)

    def test_synonym_line_to_objects_pair(self):
        s = "Abutilon pulverulentum Ulbrich = "\
            "Sidasodes jamesonii (Baker f. ) Fryxell & Fuertes"

        result = taxonlist2json.synonym_line_to_objects_pair(s)

        expect = ({'ht-epithet': 'Abutilon', 'rank': 'species',
                   'author': 'Ulbrich', 'hybrid': False,
                   'object': 'taxon', 'epithet': 'pulverulentum',
                   'ht-rank': 'genus'},
                  {'ht-epithet': 'Sidasodes',
                   'rank': 'species',
                   'author': '(Baker f. ) Fryxell & Fuertes',
                   'hybrid': False,
                   'object': 'taxon',
                   'epithet': 'jamesonii',
                   'ht-rank': 'genus'})
        self.assertEquals(result, expect)

    
