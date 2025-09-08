from collections import OrderedDict
import json
import os
from os.path import join
import sys


BASE_URL = os.environ.get('CODELISTS_BASE_URL', '')

PATH = sys.argv[1]
OUTPUTDIR = sys.argv[2]

languages = ['en', 'fr']

with open(join(OUTPUTDIR, 'codelists.json')) as handler:
    codelists_list = json.load(handler)

api_data = {
    'formats': {
        'xml': OrderedDict(
            [(cl, join(
                BASE_URL, PATH, 'xml', cl + '.xml'))
             for cl in codelists_list]),
        'csv': {
            'languages': OrderedDict([
                (lang, OrderedDict([
                    (cl, join(
                        BASE_URL, PATH, 'csv', lang, cl + '.csv'))
                    for cl in codelists_list]))
                for lang in languages])
        },
        'xlsx': {
            'languages': OrderedDict([
                (lang, OrderedDict([
                    (cl, join(
                        BASE_URL, PATH, 'xlsx', lang, cl + '.xlsx'))
                    for cl in codelists_list]))
                for lang in languages])
        },
        'json': {
            'languages': OrderedDict([
                (lang, OrderedDict([
                    (cl, join(
                        BASE_URL, PATH, 'json', lang, cl + '.json'))
                    for cl in codelists_list]))
                for lang in languages])
        }
    }
}
with open(join(OUTPUTDIR, 'index.json'), 'w') as handler:
    json.dump(api_data, handler)

with open(join(OUTPUTDIR, 'index.v2.json'), 'w') as handler:
    from collections import defaultdict
    codelists_v2 = defaultdict(dict)
    for codelist in codelists_list:
        for lang in languages:
            with open(join(OUTPUTDIR, 'json', lang, codelist + '.json')) as incodelist:
                metadata = json.load(incodelist)['metadata']
                codelists_v2[codelist][lang] = {
                    'name': metadata['name'] or None,
                    'description': metadata['description'] or None
                }
                if lang == 'en':
                    codelists_v2[codelist]['code'] = codelist
                    codelists_v2[codelist]['category'] = metadata['category']
    json.dump(codelists_v2, handler)