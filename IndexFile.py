"""
Class for the index file for the multistream bz2 wiktionary files.
"""

import bz2
from collections import namedtuple

IndexLine = namedtuple('IndexLine', ['block_offset', 'pageid', 'name'])

class IndexFile:
  
  def __parseline__(line):
    toks = line.split(":")
    return IndexLine(int(toks[0]), int(toks[1]), ":".join(toks[2:]))

  
  def __init__(self, indexfile):
    filedat = None
    if indexfile[len(indexfile)-3:] == "bz2":
      # If still compressed we need to deal with that.
      with open(indexfile, "rb") as fdat:
        rawdat = fdat.read()
        dc = bz2.BZ2Decompressor()
        filedat = dc.decompress(rawdat).decode("utf-8")
    else:
      # If not bz2 compressed, assume it's just a text file.
      with open(indexfile, "r") as fdat:
        filedat = fdat.read()
    # Now parse the data.
    self.__name2dat = {}
    for line in filedat.splitlines():
      iline = IndexFile.__parseline__(line)
      self.__name2dat[iline.name] = iline


  def name2dat(self, name):
    if name in self.__name2dat:
      return self.__name2dat[name]
    else:
      raise LookupError
  

  def name2block_offset(self, name):
    if name in self.__name2dat:
      return self.__name2dat[name].block_offset
    else:
      raise LookupError

  def name2pageid(self, name):
    if name in self.__name2dat:
      return self.__name2dat[name].pageid
    else:
      raise LookupError

