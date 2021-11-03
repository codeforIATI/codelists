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
