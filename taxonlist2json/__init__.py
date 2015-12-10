def binomial_to_dict(input):
    '''compute dictionary equivalent to input
    '''

    input = input.strip()
    if input in ['?', '']:
        return {}
    result = {'object': 'taxon',
              'ht-rank': 'genus',
              'hybrid': False,
              'rank': 'species'}
    values = input.split(' ', 2)
    result['ht-epithet'] = values[0]
    result['epithet'] = values[1]
<<<<<<< HEAD
    import HTMLParser
    a = HTMLParser.HTMLParser() 
    result['author'] = a.unescape(values[2])


=======

    import HTMLParser
    h = HTMLParser.HTMLParser()  # rewrite with functor
    result['author'] = h.unescape(values[2])
>>>>>>> e9ff63b1ee4b203b19181b8ea7ba05625927c6f3

    return result


def synonym_line_to_objects_pair(input):
    '''compute pair where first element is synonym and second accepted taxon
    '''
    first, second = input.split('=')
    synonym = binomial_to_dict(first)
    accepted = binomial_to_dict(second)
    return (synonym, accepted)


def whole_block_to_taxon_object(input):
    '''compute one taxon object from $-separated text

    receive one block of text, separated from previous and next by a $
    and not including any $ symbols, return one dictionary.
    '''

    lines = element_to_lines(input)
    result = binomial_to_dict(lines[0])
    if len(lines) > 1:
        synonym, accepted = synonym_line_to_objects_pair(lines[1])
        if accepted:
            result['accepted'] = accepted
    return result


def element_to_lines(input):
    """filter all lines which are relevant to object definition

    input is a <cr> separated string, output is a list of strings. the
    only lines relevant to the object definition are the first one and
    the one defining the synonymy.
    """

    lines = input.split('\n')
    ## remove empty lines
    lines = [i for i in lines if i != '']
    ## we definitely use the first non-empty line
    result = [lines[0]]
    ## and the second, if it's a synonym definition
    if lines[1].find('=') != -1:
        result.append(lines[1])
    return result


def convert(input):
    return [whole_block_to_taxon_object(i)
            for i in input.split('$') if i.strip()]


def import_ars_grin_family(input):
    '''the family as of the input

    input is html code snippet.
    it starts with <i>, then the epithet, then </i>, then junk.
    second line is optional and we are again only interested in italic.

    noli resultare si nomen nudus vel illegitimus est
    '''
    if input.find("nom. nud.") != -1:
        return None
    if input.find("nom. illeg.") != -1:
        return None
    input = input.strip()
    lines = input.split('\n')
    result = ars_grin_line_to_object(lines[0])
    if len(lines) > 1 and lines[1].find("<h2>") != -1:
        result['accepted'] = ars_grin_line_to_object(lines[1])
    return result


def ars_grin_line_to_object(input):
    '''
    input is html code snippet.
    we only want the part in italic.
    part of the line holds the author and the quality of the publication.
    '''

    input = input.strip()
    if not input:
        return None

    input = input.split("<i>")[1]
    input = input.split("</i>")[0]
    return {'object': 'taxon',
            'rank': 'family',
            'epithet': input,
            }


def convert_ars_grin(input):
    """return the list of objects

    input is the file as we have saved it.
    """

    separator = '\n    <h1>'
    items = input.split(separator)[1:]
    result = [import_ars_grin_family(i) for i in items]
    return [i for i in result if i]


def dict_from_epithet_author(fields, rank):
    if rank == 'family':
        prefix = 'ht-'
    elif rank == 'genus':
        prefix = ''
    result = {'object': 'taxon',
              prefix + 'rank': rank,
              prefix + 'epithet': fields[0],
              }
    if len(fields) > 1:
        result['author'] = fields[1]
    return result


def ars_grin_genus_to_dict(input):
    '''convert the content of page to bauble dict

    the input is the content of a taxonomyfamily page
    '''

    import re
    taxon_pattern = re.compile(
        r'^<i>([A-Z][a-z]+)</i>[ ]*(.*)</h1>$')
    synonym_pattern = re.compile(
        r'^<h2>Synonym of <a [^>]*>([A-Z][^ ]+) (.*)</a></h2>$')
    family_pattern = re.compile(
        r'<td><i><a href=".*">([A-Z].*)</a></i></td>')
    reject_pattern = re.compile(
        r'<td>(a rejected|an illegitimate).*')
    lines = [i.strip() for i in input.split('\n')]
    if filter(None, map(reject_pattern.match, lines)):
        return None
    try:
        taxon_match = filter(None, map(taxon_pattern.match, lines))[0]
    except IndexError:
        return None
    synonym_match = (filter(None, map(synonym_pattern.match, lines)) +
                     [None])[0]
    family_match = filter(None, map(family_pattern.match, lines))[0]
    result = dict_from_epithet_author(family_match.groups(), 'family')
    result.update(dict_from_epithet_author(taxon_match.groups(), 'genus'))

    if synonym_match:
        result['accepted'] = dict_from_epithet_author(synonym_match.groups(),
                                                      'genus')
    return result
