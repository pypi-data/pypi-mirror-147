# IMBIBED: IMpeccable BIBliographiEs with Dblp

A simple tool for generating and cleaning `.bib` (and related `.tex`) files for
bibliographies mainly based on DBLP.

## Install

```shell
$ pip install imbibed
```

## Usage

```shell
$ imbibed -h
usage: imbibed [-h] [-s] [--condense] [--normal] [--crossref] [--no-cache]
               [--update-files UPDATE_FILES] [--filter-files FILTER_FILES]
               input output

IMBIBED: IMpeccable BIBliographiEs with Dblp Convert your bib file to use DBLP data and citation keys.
Conversion is based on DOIs (or DBLP keys if exist) in the input database.

positional arguments:
  input                 Input bib file
  output                File where the output bib is written (may be the same as input).

optional arguments:
  -h, --help            show this help message and exit
  -s, --sort            Sort the output bib by key.
  --condense            Use DBLP condensed format (default).
  --normal              Use DBLP normal format.
  --crossref            Use DBLP crossref format.
  --no-cache            No not cache DBLP requests in local file.
  --update-files UPDATE_FILES
                        Update tex (or other format) files for the new keys. Accepts glob patterns.
                        WARNING: this does simple search-and-replace of the keys, hence might break
                        your files. MAKE A BACKUP FIRST.
  --filter-files FILTER_FILES
                        Look for cited keys in these files and delted non-cited keys.Accepts glob
                        patterns. WARNING: this does simple search of the keys, in the files.
```
