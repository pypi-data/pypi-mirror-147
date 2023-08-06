#!/usr/env python3
# Copyright 2022 Gaëtan Cassiers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
IMBIBED: IMpeccable BIBliographiEs with Dblp

Convert your bib file to use DBLP data and citation keys.
Conversion is based on DOIs (or DBLP keys if exist) in the input database.
"""

import sys
import argparse
import glob
import urllib.parse
import traceback

import bibtexparser
import requests
import requests_cache
import tqdm

SEARCH_BY_DOI = "https://dblp.org/search/publ/api?eid=DOI%3A{doi}&format=json&h=1"
# param: 0 for condensed, 1 for normal, 2 for crossref
BIB_BY_KEY = "https://dblp.org/rec/{key}.bib?param={param}"

class NotInDBLP(Exception):
    "DOI not found by DBLP serch."
    pass

class NoDOI(Exception):
    "No DOI provided in the input database."
    pass

def doi2dblpkey(doi):
    "Convert a DOI to a DBLP key using DBLP's search API."
    search_url = SEARCH_BY_DOI.format(doi=urllib.parse.quote(doi.upper(), safe=''))
    search = requests.get(search_url).json()
    hits = search["result"]["hits"]
    if hits['@total'] != '1':
        raise NotInDBLP()
    return hits["hit"][0]["info"]["key"]

def dblpkey2bib(key, param=0):
    """"Fetch bib representation from DBLP. Return bibtex entry/entries (if
    crossref).

    :key:
        DBLP key
    :param:
        0: Condensed
        1: Standard
        2: Crossref
    """
    return requests.get(BIB_BY_KEY.format(key=key, param=param)).content.decode()

def dblp_key_extract(entry):
    """Return dblp key if the bibtex key is already a DBLP one, otherwise
    return none."""
    if entry["ID"].startswith("DBLP:"):
        return entry["ID"][5:]
    else:
        return None

def entry2dblp_bib(entry, condense):
    """Convert a bibtexparser entry to a list DBLP entries and the new key."""
    key = dblp_key_extract(entry)
    if key is None:
        if "doi" in entry:
            key = doi2dblpkey(entry["doi"])
        else:
            raise NoDOI()
    return (key, bibtexparser.loads(dblpkey2bib(key)).entries)

WARNING_NO_DOI = (
        "Warning: entry {key} has no DOI and is not a DBLP key." +
        "\n\tThe entry will be kept as-is."
        )
WARNING_NOT_DBLP = (
        "Warning: entry {key} DOI's {doi} has not been found in DBLP." +
        "\n\tThe entry will be kept as-is."
        )
ERROR_MISC = (
        "Error: unknown error when converting entry {key}."
        "\n\tThe entry will be kept as-is."
        "\n\tError: {exc}."
        )

def map_bibtex(entries, condense):
    """Map bibtexparser entries to DBLP entries if possible.

    Otherwise keep the entry as-is and and report an error.
    Output also the new keys.
    """
    errors = list()
    new_entries = list()
    key_map = dict()
    for entry in tqdm.tqdm(entries, desc="Converting items"):
        try:
            new_key, new_e = entry2dblp_bib(entry, condense)
        except Exception as e:
            if isinstance(e, NoDOI):
                errors.append(WARNING_NO_DOI.format(key=entry["ID"]))
            elif isinstance(e, NotInDBLP):
                errors.append(WARNING_NOT_DBLP.format(key=entry["ID"], doi=entry["doi"]))
            else:
                errors.append(ERROR_MISC.format(key=entry["ID"], exc=e) + traceback.format_exc())
            new_entries.append(entry)
        else:
            new_entries.extend(new_e)
            key_map[entry["ID"]] = "DBLP:"+new_key
    # Preserve order as much as possible, but deduplicate
    new_entries_dict = dict()
    for entry in new_entries:
        key = entry["ID"]
        if key not in new_entries_dict:
            new_entries_dict[key] = entry
    new_entries = list(new_entries_dict.values())
    return new_entries, key_map, errors

def filter_keys(file_patterns, keys):
    """For each file matching any of the patterns, search for the keys.
    If a key is not found in any file, delete it."""
    files = sum(map(glob.glob, file_patterns), start=list())
    keys_found = {key: False for key in keys}
    for file in tqdm.tqdm(files, desc="Searching keys in files."):
        # operate on binary as we don't know the encoding and bibtex is
        # ASCII-only for the keys
        with open(file, 'rb') as f:
            s = f.read()
        # stupid algo, should be optimized to avoid quadratic behavior (regex
        # might do it)
        for key in (key for key, found in keys_found.items() if not found):
            if key in s:
                keys_found[key] = True
    return keys_found


def update_keys(file_patterns, key_map):
    """For each file matching any of the patterns, replace every old key
    occurence with the new key."""
    files = sum(map(glob.glob, file_patterns), start=list())
    for file in tqdm.tqdm(files, desc="Updating keys in files."):
        # operate on binary as we don't know the encoding and bibtex is
        # ASCII-only for the keys
        with open(file, 'rb') as f:
            s = f.read()
        # stupid algo, should be optimized to avoid quadratic behavior (regex
        # might do it)
        for old, new in key_map.items():
            s = s.replace(old.encode(), new.encode())
        with open(file, 'wb') as f:
            f.write(s)

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
            'input',
            type=str,
            help='Input bib file',
            )
    parser.add_argument(
            'output',
            type=str,
            help='File where the output bib is written (may be the same as input).',
            )
    parser.add_argument(
            '-s', '--sort',
            action='store_true',
            help='Sort the output bib by key.',
            )
    parser.add_argument(
            '--condense',
            dest='condense',
            action='store_const',
            const=0,
            default=0,
            help='Use DBLP condensed format (default).',
            )
    parser.add_argument(
            '--normal',
            dest='condense',
            action='store_const',
            const=1,
            help='Use DBLP normal format.',
            )
    parser.add_argument(
            '--crossref',
            dest='condense',
            action='store_const',
            const=2,
            help='Use DBLP crossref format.',
            )
    parser.add_argument(
            '--no-cache',
            action='store_true',
            help='No not cache DBLP requests in local file.',
            )
    parser.add_argument(
            '--update-files',
            action='append',
            type=str,
            help=(
                'Update tex (or other format) files for the new keys. ' +
                'Accepts glob patterns. ' +
                'WARNING: this does simple search-and-replace of the keys, '+
                'hence might break your files. MAKE A BACKUP FIRST.'
                ),
            )
    parser.add_argument(
            '--filter-files',
            action='append',
            type=str,
            help=(
                'Look for cited keys in these files and delete non-cited keys.' +
                'Accepts glob patterns. ' +
                'WARNING: this does simple search of the keys, in the files.'
                ),
            )
    return parser.parse_args()

def main():
    args = parse_args()
    if not args.no_cache:
        requests_cache.install_cache('imbibed_cache.sqlite', backend='sqlite')
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    with open(args.input) as f:
        bibtex = bibtexparser.load(f, parser)
    if args.filter_files:
        key_filter = filter_keys(args.filter_files, bibtex.entries.keys())
        filtered_entries = {key: bibtex.entries[key] for key, found in key_filter if found}
    else:
        filtered_entries = bibtex.entries
    bibtex.entries, key_map, errors = map_bibtex(filtered_entries, args.condense)
    if args.filter_files:
        print("Removed items:")
        for key, found in key_filter:
            if not found:
                print(f"\t{key}")
    if key_map:
        print("Converted items:")
        for old, new in key_map.items():
            if old != new:
                print(f"\t{old} -> {new}")
    for error in errors:
        print(error, file=sys.stderr)
    writer = bibtexparser.bwriter.BibTexWriter()
    if not args.sort:
        writer.order_entries_by = None # no sorting
    with open(args.output, "w") as f:
        bibtexparser.dump(bibtex, f, writer)
    if args.update_files:
        update_keys(args.update_files, key_map)

if __name__ == '__main__':
    main()

