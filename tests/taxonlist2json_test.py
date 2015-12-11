# -*- coding: utf-8 -*-

import unittest
#from unittest import SkipTest

import taxonlist2json


class BinomialToDictTest(unittest.TestCase):

    def test_binomial_to_dict__varietas_with_author(self):
        s = 'Abutilon amplissimum var. subpeltata Ktze.'
        result = taxonlist2json.binomial_to_dict(s)
        expect = {'object': 'taxon',
                  'rank': 'varietas',  # should decide name of rank
                  'ht-rank': 'species',
                  'epithet': 'subpeltata',
                  'ht-epithet': 'Abutilon amplissimum',  # COMMENT THIS
                  'author': "Ktze.",
                  }
        self.assertEquals(result, expect)

    def test_binomial_to_dict__with_simple_author(self):
        s = ' Abuta velutina Gleason'
        result = taxonlist2json.binomial_to_dict(s)
        expect = {'object': 'taxones',
                  'rank': 'species',
                  'epithet': 'velutina',
                  'ht-rank': 'genus',
                  'ht-epithet': 'Abuta',
                  'hybrid': False,
                  'author': 'Gleason',
                  }
        self.assertEquals(result, expect)

    def test_binomial_to_dict__with_composite_author(self):
        result = taxonlist2json.binomial_to_dict(
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

    def test_binomial_to_dict__author_with_utf8_char(self):
        s = "Abutilon nudiflorum (L'H&eacute;r.) Sweet"
        result = taxonlist2json.binomial_to_dict(s)
        expect = {'ht-epithet': 'Abutilon',
                  'rank': 'species',
                  'author': u"(L'Hér.) Sweet",
                  'hybrid': False,
                  'object': 'taxon',
                  'epithet': 'nudiflorum',
                  'ht-rank': 'genus'}
        self.assertEquals(result, expect)


class SynonymLineToObjectsPairTest(unittest.TestCase):

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


class ConvertFileToElements(unittest.TestCase):
    def test_file_to_elements(self):
        s = '''\
$


 Aa brevis Schltr.


Aa brevis Schltr. = Myrosmodes breve (Schltr.) Garay

Reference: FP 1438: 102; Garay, L. A., 1978: 168; Dodson, C. H., 1992: xx.


$


 Aa calceata (Rchb. f.) Schltr.



Aa calceata (Rchb. f.) Schltr.

Synonyms: Aa calceata Rchb. f.
Reference: Flora Peru: 1438: 94; Dodson, pers. comm..
Note: Not reconfirmed.


$


 Aa chiogena Schltr.


Aa chiogena Schltr. = Myrosmodes chiogena (Schltr.)

Reference: FP 1438: 94.


$\
'''
        result = taxonlist2json.convert(s)
        self.assertEquals(len(result), 3)


class WholeBlockToTaxonObject(unittest.TestCase):
    def test_whole_block_to_taxon_object__with_synonym(self):
        s = '''\



 Matucana calvescens (Kimnach & Hutchison) Buxb.


Matucana calvescens (Kimnach & Hutchison) Buxb. = \
Matucana aurantiaca (Vaupel) Buxb.

Reference: Ritter, F., 1981: 1489; Hunt, D., 1992: 89.


'''
        result = taxonlist2json.whole_block_to_taxon_object(s)
        expect = {'object': 'taxon',
                  'rank': 'species',
                  'epithet': 'calvescens',
                  'ht-rank': 'genus',
                  'ht-epithet': 'Matucana',
                  'author': '(Kimnach & Hutchison) Buxb.',
                  'hybrid': False,
                  'accepted': {'object': 'taxon',
                               'rank': 'species',
                               'epithet': 'aurantiaca',
                               'ht-rank': 'genus',
                               'ht-epithet': 'Matucana',
                               'author': '(Vaupel) Buxb.',
                               'hybrid': False,
                               },
                  }
        self.assertEquals(result, expect)

    def test_whole_block_to_taxon_object__without_synonym(self):
        s = '''\



 Osmorhiza mexicana Griseb.



Osmorhiza mexicana Griseb.

'''
        result = taxonlist2json.whole_block_to_taxon_object(s)
        expect = {'object': 'taxon',
                  'rank': 'species',
                  'epithet': 'mexicana',
                  'ht-rank': 'genus',
                  'ht-epithet': 'Osmorhiza',
                  'author': 'Griseb.',
                  'hybrid': False,
                  }
        self.assertEquals(result, expect)


class ImportArsGrinFamily(unittest.TestCase):
    def test_import_ars_grin_family__simple(self):
        s = '''<i>Acanthaceae</i> Juss., nom. cons.</h1>'''
        result = taxonlist2json.import_ars_grin_family(s)
        expect = {'object': 'taxon',
                  'rank': 'family',
                  'epithet': 'Acanthaceae',
                  }
        self.assertEquals(result, expect)

    def test_import_ars_grin_family__with_synonym(self):
        s = '''<i>Abietaceae</i> Gray, nom. cons.</h1>
    <h2>Synonym of <a href='879'><i>Pinaceae</i> Spreng. ex F. Rudolphi, nom. cons.</a></h2>'''
        result = taxonlist2json.import_ars_grin_family(s)
        expect = {'object': 'taxon',
                  'rank': 'family',
                  'epithet': 'Abietaceae',
                  'accepted': {'object': 'taxon',
                               'rank': 'family',
                               'epithet': 'Pinaceae',
                               }
                  }
        self.assertEquals(result, expect)

    def test_import_ars_grin_family__illegitimus(self):
        s = '''<i>Abaminaceae</i> J. Agardh, nom. illeg.</h1>
    <h2>Synonym of <a href='756'><i>Nartheciaceae</i> Fr. ex Bjurzon</a></h2>'''
        result = taxonlist2json.import_ars_grin_family(s)
        expect = None
        self.assertEquals(result, expect)

    def test_import_ars_grin_family__nudus(self):
        s = '''<i>Achratinitaceae</i> F. A. Barkley, nom. nud.</h1>
    <h2>Synonym of <a href='296'><i>Corsiaceae</i> Becc., nom. cons.</a></h2>'''
        result = taxonlist2json.import_ars_grin_family(s)
        expect = None
        self.assertEquals(result, expect)


class ArsGrinGenusToDict(unittest.TestCase):
    def test_ars_grin_genus_to_dict__simple(self):
        s = '''\
	<table class="detail" cellspacing="0" border="0" id="ctl00_cphBody_dvGenus">
		<tr>
			<td colspan="2">
        <h1 style="font-size: 150%"><a href='taxon/abouttaxonomy.aspx?chapter=scient' target='_blank'>Genus:</a>
         <i>Abarema</i>  Pittier</h1>
					<th>Family:</th>
					<td><i><a href="taxonomyfamily.aspx?id=440">Fabaceae</a></i></td>
'''
        result = taxonlist2json.ars_grin_genus_to_dict(s)
        expect = {'object': 'taxon',
                  'rank': 'genus',
                  'epithet': 'Abarema',
                  'ht-rank': 'family',
                  'ht-epithet': 'Fabaceae',
                  'author': 'Pittier',
                  }
        self.assertEquals(result, expect)

    def test_ars_grin_genus_to_dict__illegitimate(self):
        s = '''\
        <h1 style="font-size: 150%"><a href='taxon/abouttaxonomy.aspx?chapter=scient' target='_blank'>Genus:</a>
         <i>Petalanthera</i>  Raf.</h1>
        <h2>Synonym of <a href='taxonomygenus.aspx?id=6233'>Justicia L.</a></h2>
					<th>Family:</th>
					<td><i><a href="taxonomyfamily.aspx?id=6">Acanthaceae</a></i></td>
					<th>Comments:</th>
					<td>an illegitimate later homonym (Melbourne ICN Art. 53) of <I>Petalanthera</I> Nees & Mart. (1833) that is unavailable for use </td>
'''
        result = taxonlist2json.ars_grin_genus_to_dict(s)
        expect = None
        self.assertEquals(result, expect)

    def test_ars_grin_genus_to_dict__rejected(self):
        s = '''\
        <h1 style="font-size: 150%"><a href='taxon/abouttaxonomy.aspx?chapter=scient' target='_blank'>Genus:</a>
         <i>Anomatheca</i>  Ker Gawl.</h1>
        <h2>Synonym of <a href='taxonomygenus.aspx?id=4754'>Freesia Eckl. ex Klatt</a></h2>
					<th>Family:</th>
					<td><i><a href="taxonomyfamily.aspx?id=584">Iridaceae</a></i></td>
					<th>Comments:</th>
					<td>a rejected (nom. rej.), heterotypic synonym (Melbourne ICN Art. 14.4 & App. III) of <I>Freesia</I> Klatt, nom. cons. </td>
'''
        result = taxonlist2json.ars_grin_genus_to_dict(s)
        expect = None
        self.assertEquals(result, expect)

    def test_ars_grin_genus_to_dict__synonym(self):
        s = '''\
        <h1 style="font-size: 150%"><a href='taxon/abouttaxonomy.aspx?chapter=scient' target='_blank'>Genus:</a>
         <i>Dactylanthes</i>  Haw.</h1>
        <h2>Synonym of <a href='taxonomygenus.aspx?id=4515'>Euphorbia L.</a></h2>
					<th>Family:</th>
					<td><i><a href="taxonomyfamily.aspx?id=433">Euphorbiaceae</a></i></td>
'''
        result = taxonlist2json.ars_grin_genus_to_dict(s)
        expect = {'object': 'taxon',
                  'rank': 'genus',
                  'epithet': 'Dactylanthes',
                  'ht-rank': 'family',
                  'ht-epithet': 'Euphorbiaceae',
                  'author': 'Haw.',
                  'accepted': {'author': 'L.',
                               'epithet': 'Euphorbia',
                               'object': 'taxon',
                               'rank': 'genus'},
                  }
        self.assertEquals(result, expect)
