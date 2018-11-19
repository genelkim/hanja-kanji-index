"""
Read and decompress the multi-stream bzip2 file.
"""

import bz2
import codecs
from IndexFile import IndexFile, IndexLine
from ArticleMultistream import ArticleMultistream
import sys

IDX_FILE = "data/kowiktionary-latest-pages-articles-multistream-index.txt.bz2"
DAT_FILE="data/kowiktionary-latest-pages-articles-multistream.xml.bz2"

print("Initializing index file..."),
idxf = IndexFile(IDX_FILE)
print("Complete")
print("Initializing article multistream..."),
am = ArticleMultistream(DAT_FILE)
print("Complete")

lookup = ""
while lookup != ":q":
  if lookup.strip() != "":
    il = idxf.name2dat(lookup)
    markdown = am.get_page_markdown(il.block_offset, il.pageid)
    print(markdown)

  lookup = input("Enter a word to lookup: ")

print("Shutting down...")

