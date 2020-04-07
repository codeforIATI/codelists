from lxml import etree as ET
import os
from os.path import join
import re
import csv
import json
from functools import partial
import sys
from collections import OrderedDict
import git
from datetime import date

import xlsx


languages = ['en', 'fr']

xml_lang = '{http://www.w3.org/XML/1998/namespace}lang'
budget_alignment_namespace = {
    'budget-alignment': 'http://iatistandard.org/activity-standard/' +
                        'overview/country-budget-alignment/'}
nsmap = {'xml': 'http://www.w3.org/XML/1998/namespace'}

repo = git.Repo('IATI-Codelists-NonEmbedded/.git')
tree = repo.tree()
repo_extra = git.Repo('Unofficial-Codelists/.git')
tree_extra = repo_extra.tree()

OUTPUTDIR = sys.argv[1]

BASE_URL = os.environ.get('CODELISTS_BASE_URL', '')


def normalize_whitespace(x):
    if x is None:
        return x
    x = x.strip()
    x = re.sub(r'\s+', ' ', x)
    return x


def get_last_updated_date(codelist_name):
    try:
        blob = tree['xml/{}.xml'.format(codelist_name)]
        commit = next(repo.iter_commits(paths=blob.path))
    except KeyError:
        blob = tree_extra['xml/{}.xml'.format(codelist_name)]
        commit = next(repo_extra.iter_commits(paths=blob.path))
    return date.fromtimestamp(commit.committed_date).isoformat()


def codelist_item_todict(codelist_item, fieldnames, default_lang='',
                         lang='en', codelist_name=None):
    out = {}
    for child in codelist_item:
        # Some tags are handled in special ways (below)
        if child.tag == 'status':
            continue
        if child.text is None:
            continue
        if child.find('narrative') is not None:
            if lang == default_lang:
                narrative = child.xpath(
                    'narrative[not(@xml:lang)]',
                    namespaces=nsmap)
                if len(narrative) == 0:
                    continue
                out[child.tag] = normalize_whitespace(narrative[0].text)
            else:
                narrative = child.find(
                    'narrative[@xml:lang="{}"]'.format(lang),
                    namespaces=nsmap)
                if narrative is None:
                    continue
                out[child.tag] = normalize_whitespace(narrative.text)
        else:
            out[child.tag] = normalize_whitespace(child.text)

    if 'public-database' in codelist_item.attrib:
        if codelist_item.attrib['public-database'] in ['1', 'true']:
            out['public-database'] = True
        else:
            out['public-database'] = False
    out['status'] = codelist_item.get('status', 'active')
    if codelist_name == 'Sector':
        budget_alignment_status = codelist_item.find(
            'budget-alignment:status',
            namespaces=budget_alignment_namespace)
        if budget_alignment_status is not None:
            out['budget_alignment_guidance'] = budget_alignment_status.text
        else:
            out['budget_alignment_guidance'] = ''
    return out


def write_json_api_root(codelists_list):
    with open(join(OUTPUTDIR, 'codelists.json'), 'w') as handler:
        json.dump(codelists_list, handler)
    api_data = {
        'formats': {
            'xml': OrderedDict(
                [(cl, join(
                    BASE_URL, 'api', 'xml', cl + '.xml'))
                 for cl in codelists_list]),
            'csv': {
                'languages': OrderedDict([
                    (lang, OrderedDict([
                        (cl, join(
                            BASE_URL, 'api', 'csv', lang, cl + '.csv'))
                        for cl in codelists_list]))
                    for lang in languages])
            },
            'xlsx': {
                'languages': OrderedDict([
                    (lang, OrderedDict([
                        (cl, join(
                            BASE_URL, 'api', 'xlsx', lang, cl + '.xlsx'))
                        for cl in codelists_list]))
                    for lang in languages])
            },
            'json': {
                'languages': OrderedDict([
                    (lang, OrderedDict([
                        (cl, join(
                            BASE_URL, 'api', 'json', lang, cl + '.json'))
                        for cl in codelists_list]))
                    for lang in languages])
            }
        }
    }
    with open(join(OUTPUTDIR, '..', 'index.json'), 'w') as handler:
        json.dump(api_data, handler)


for language in languages:
    codelists = ET.Element('codelists')
    codelists_list = []

    try:
        os.makedirs(join(OUTPUTDIR, 'json', language))
        os.makedirs(join(OUTPUTDIR, 'csv', language))
        os.makedirs(join(OUTPUTDIR, 'xlsx', language))
    except OSError:
        pass

    for xml_filename in os.listdir(join(OUTPUTDIR, 'xml')):
        fieldnames = [
            'code',
            'name',
            'description',
            'category',
            'url',
            'status'
        ]
        codelist = ET.parse(join(OUTPUTDIR, 'xml', xml_filename))
        root = codelist.getroot()
        attrib = root.attrib
        assert attrib['name'] == xml_filename.replace('.xml', '')

        default_lang = attrib.get(xml_lang)
        codelist_items = root.find('codelist-items').findall('codelist-item')
        codelist_item_els = root.xpath('codelist-items/codelist-item/*')
        fieldnames += list(OrderedDict([
            (x.tag, None)
            for x in codelist_item_els
            if x.tag not in fieldnames]).keys())
        codelist_dicts = list(
            map(partial(codelist_item_todict,
                fieldnames=fieldnames,
                default_lang=default_lang,
                lang=language,
                codelist_name=attrib['name']), codelist_items))

        if attrib['name'] == 'Sector':
            fieldnames.append('budget_alignment_guidance')

        if xml_filename == 'OrganisationRegistrationAgency.xml':
            fieldnames.append('public-database')

        csv_filename = join(
            OUTPUTDIR, 'csv', language, attrib['name'] + '.csv')
        with open(csv_filename, 'w') as handler:
            dw = csv.DictWriter(handler, fieldnames)
            dw.writeheader()
            for row in codelist_dicts:
                dw.writerow(row)

        xlsx_filename = join(
            OUTPUTDIR, 'xlsx', language, attrib['name'] + '.xlsx')
        xdw = xlsx.XLSXDictWriter(xlsx_filename, fieldnames=fieldnames)
        xdw.writeheader()
        for row in codelist_dicts:
            xdw.writerow(row)
        xdw.close()

        if language == default_lang:
            el_search = f'narrative[not(@xml:lang) or @xml:lang="{language}"]'
        else:
            el_search = f'narrative[@xml:lang="{language}"]'
        el_search = '/codelist/metadata/{}/' + el_search
        meta_name_el = root.xpath(el_search.format('name'))
        meta_desc_el = root.xpath(el_search.format('description'))
        meta_category_el = root.xpath(el_search.format('category'))
        meta_url_el = root.xpath('/codelist/metadata/url')
        meta_name = meta_name_el[0].text if meta_name_el else ''
        meta_desc = meta_desc_el[0].text if meta_desc_el else ''
        meta_category = meta_category_el[0].text if meta_category_el else ''
        meta_url = meta_url_el[0].text if meta_url_el else ''

        # JSON
        json_filename = join(
            OUTPUTDIR, 'json', language, attrib['name'] + '.json')
        with open(json_filename, 'w') as handler:
            json.dump({
                'attributes': {
                    'name': attrib['name'],
                    'complete': attrib.get('complete'),
                    'embedded': attrib.get('embedded'),
                    'category-codelist': attrib.get('category-codelist'),
                },
                'metadata': {
                    'name': meta_name,
                    'description': meta_desc,
                    'category': meta_category,
                    'url': meta_url,
                    'last-updated-date': get_last_updated_date(
                        attrib['name'])
                },
                'data': codelist_dicts
            }, handler)

        codelists_list.append(attrib['name'])

        ET.SubElement(codelists, 'codelist').attrib['ref'] = attrib['name']

tree = ET.ElementTree(codelists)
tree.write(join(OUTPUTDIR, 'codelists.xml'), pretty_print=True)
sorted_codelists_list = sorted(codelists_list)
write_json_api_root(sorted_codelists_list)
