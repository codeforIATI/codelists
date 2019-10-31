from lxml import etree as ET
import os
import re
import csv
import json
from functools import partial
import sys
from collections import OrderedDict

languages = ['en', 'fr']

xml_lang = '{http://www.w3.org/XML/1998/namespace}lang'

OUTPUTDIR = sys.argv[1]

BASE_URL = os.environ.get('CODELISTS_BASE_URL', "")


def normalize_whitespace(x):
    if x is None:
        return x
    x = x.strip()
    x = re.sub(r'\s+', ' ', x)
    return x


def codelist_item_todict(codelist_item, default_lang='', lang='en'):
    fieldnames = [
        'code',
        'name',
        'description',
        'category',
        'url',
    ]
    out = {}
    for child in codelist_item:
        if child.tag not in fieldnames:
            continue
        if child.tag in ['name', 'description'] and \
                child.attrib.get(xml_lang) != lang and \
                (child.attrib.get(xml_lang) is not None or lang != default_lang):
            continue
        out[child.tag] = normalize_whitespace(child.text)

    if 'public-database' in codelist_item.attrib:
        if codelist_item.attrib['public-database'] in ['1', 'true']:
            out['public-database'] = True
        else:
            out['public-database'] = False
    out['status'] = codelist_item.get('status', 'active')
    return out


def utf8_encode_dict(d):
    def enc(a):
        if type(a) == str:
            return a.encode('utf8')
        else:
            return None
    return dict((enc(k), enc(v)) for k, v in d.items())


def write_json_api_data(codelists_list):
    json.dump(codelists_list, open(os.path.join(OUTPUTDIR, 'codelists.json'), 'w'))
    json.dump({
        "languages": dict([
            (lang,{
                "formats":
                    {
                    "xml": OrderedDict(map(lambda cl:
                        (str(cl), "{}/api/xml/{}.xml".format(BASE_URL, cl)),
                        sorted(codelists_list))),
                    "csv": OrderedDict(map(lambda cl:
                        (str(cl), "{}/api/csv/{}/{}.csv".format(BASE_URL, lang, cl)),
                        sorted(codelists_list))),
                    "json": OrderedDict(map(lambda cl:
                        (str(cl), "{}/api/json/{}/{}.json".format(BASE_URL, lang, cl)),
                        sorted(codelists_list)))
                    }
            })
            for lang in languages
        ])
        },
        open(os.path.join(OUTPUTDIR, '..', 'index.json'), 'w'))


for language in languages:
    codelists = ET.Element('codelists')
    codelists_list = []

    try:
        os.makedirs(os.path.join(OUTPUTDIR, 'json', language))
        os.makedirs(os.path.join(OUTPUTDIR, 'csv', language))
    except OSError:
        pass

    for fname in os.listdir(os.path.join(OUTPUTDIR, 'xml')):
        codelist = ET.parse(os.path.join(OUTPUTDIR, 'xml', fname))
        attrib = codelist.getroot().attrib
        assert attrib['name'] == fname.replace('.xml', '')

        root = codelist.getroot()
        default_lang = root.attrib.get(xml_lang)
        codelist_items = root.find('codelist-items').findall('codelist-item')
        codelist_dicts = list(map(partial(codelist_item_todict, default_lang=default_lang, lang=language), codelist_items))

        fieldnames = [
            'code',
            'name',
            'description',
            'category',
            'url',
            'status'
        ]

        if fname == 'OrganisationRegistrationAgency.xml':
            fieldnames.append('public-database')

        dw = csv.DictWriter(open(os.path.join(OUTPUTDIR, 'csv', language, attrib['name'] + '.csv'), 'w'), fieldnames)
        dw.writeheader()
        for row in codelist_dicts:
            if sys.version_info.major == 2:
                row = utf8_encode_dict(row)
            dw.writerow(row)

        name_elements = codelist.getroot().xpath('/codelist/metadata/name[{}@xml:lang="{}"]'.format('not(@xml:lang) or ' if language == default_lang else '', language))
        description_elements = codelist.getroot().xpath('/codelist/metadata/description[{}@xml:lang="{}"]'.format('not(@xml:lang) or ' if language == default_lang else '', language))
        category_elements = codelist.getroot().xpath('/codelist/metadata/category[{}@xml:lang="{}"]'.format('not(@xml:lang) or ' if language == default_lang else '', language))
        url_elements = codelist.getroot().xpath('/codelist/metadata/url')

        # JSON
        json.dump(
            {
                'attributes': {
                    'name': attrib['name'],
                    'complete': attrib.get('complete'),
                    'embedded': attrib.get('embedded'),
                    'category-codelist': attrib.get('category-codelist'),
                },
                'metadata': {
                    'name': name_elements[0].text if name_elements else '',
                    'description': description_elements[0].text if description_elements else '',
                    'category': category_elements[0].text if category_elements else '',
                    'url': url_elements[0].text if url_elements else ''
                },
                'data': codelist_dicts
            },
            open(os.path.join(OUTPUTDIR, 'json', language, attrib['name'] + '.json'), 'w')
        )

        codelists_list.append(attrib['name'])

        ET.SubElement(codelists, 'codelist').attrib['ref'] = attrib['name']

tree = ET.ElementTree(codelists)
tree.write(os.path.join(OUTPUTDIR, 'codelists.xml'), pretty_print=True)
write_json_api_data(codelists_list)
