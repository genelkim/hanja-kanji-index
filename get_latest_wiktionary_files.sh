#!/bin/bash

JA_IDX_FILE="jawiktionary-latest-pages-articles-multistream-index.txt.bz2"
JA_DAT_FILE="jawiktionary-latest-pages-articles-multistream.xml.bz2"
KO_IDX_FILE="kowiktionary-latest-pages-articles-multistream-index.txt.bz2"
KO_DAT_FILE="kowiktionary-latest-pages-articles-multistream.xml.bz2"

JA_URL_PREFIX="https://dumps.wikimedia.org/jawiktionary/latest/"
KO_URL_PREFIX="https://dumps.wikimedia.org/kowiktionary/latest/"


mkdir data
cd data
wget ${JA_URL_PREFIX}${JA_IDX_FILE}
wget ${JA_URL_PREFIX}${JA_DAT_FILE}
wget ${KO_URL_PREFIX}${KO_IDX_FILE}
wget ${KO_URL_PREFIX}${KO_DAT_FILE}

