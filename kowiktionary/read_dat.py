"""
Read and decompress the multi-stream bzip2 file.
"""

# TODO: figure out how to get to offset without reading everything.

import bz2
import codecs


INDEX_FILE = "kowiktionary-latest-pages-articles-multistream-index."

with open("kowiktionary-latest-pages-articles-multistream.xml.bz2", "rb") as fdat:
  rawdat = fdat.read()
  
  dat_pieces = []
  curdat = rawdat
  while not curdat == "":
    dpr = bz2.BZ2Decompressor()
    piece = dpr.decompress(curdat)
    dat_pieces.append(piece)
    curdat = dpr.unused_data
    print(piece.decode("utf-8").replace("\\n", "\n"))
    #print(len(dat_pieces))
  print("Complete")

