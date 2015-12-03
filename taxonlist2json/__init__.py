def line_to_binomial(input):
    '''compute dictionary equivalent to input
    '''
    result = {'object': 'taxon',
              'ht-rank': 'genus',
              'hybrid': False,
              'rank': 'species'}
    values = input.strip().split(' ', 2)
    print values[2]
    result['ht-epithet'] = values[0]
    result['epithet'] = values[1]
    import HTMLParser
    var = HTMLParser.HTMLParser()
    result['author'] = var.unescape(values[2])
    print result['author']
    return result


def synonym_line_to_objects_pair(input):
    '''compute pair where first element is synonym and second accepted taxon
    '''
    first, second = input.split('=')
    synonym = line_to_binomial(first)
    accepted = line_to_binomial(second)
    return (synonym, accepted)


def whole_block_to_taxon_object(input):
    '''compute one taxon object from $-separated text

    receive one block of text, separated from previous and next by a $,
    return one dictionary.
    '''

    return None


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
