# _*_ coding: utf-8 _*_
#from nose.tools import *
import unittest
#from nose import SkipTest
import TAXONLIS2JSON

class ReadingTestCase(unittest.TestCase):

 def test_translate_species_with_author(self):
    "accept one string, return one value"

    input ="""$
         Psychotria thyrsiflora Ruiz & Pav.
         Psychotria thyrsiflora Ruiz & Pav. = Palicourea thyrsiflora (Ruiz & Pav.) DC.
         Reference: FP 1365: 226. 
         $""" #vimos ayer

    #invoke the function we did not yet write
    result = TAXONLIS2JSON.convert(input)
    #the object we expect
    expect = {
               "rank":"Species",
               "epithet":"thyrsiflora",
               "ht-rank":"Genus",
               "ht-epithet":"Psychotria",
               "hybrid": False,
               "author": "Ruiz & Pav."
               } #tambien lo vimos ayer
    self.asserEquals(result, expect)
