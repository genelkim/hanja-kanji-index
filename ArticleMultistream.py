"""
Class to interface with the article multistream bzip2 file.
"""

import bz2
import xml.etree.ElementTree as ET

class ArticleMultistream:

  def __init__(self, multistream_file):
    self.__rawstream = open(multistream_file, 'rb')

  def get_block(self, block_offset):
    dc = bz2.BZ2Decompressor()
    self.__rawstream.seek(block_offset)
    rawstr = self.__rawstream.read()
    return dc.decompress(rawstr).decode("utf-8")

  def get_page_ET(self, block_offset, pageid):
    blockstr = self.get_block(block_offset)
    # Parse the block with a false root added.
    root = ET.fromstring("<froot>" + blockstr + "</froot>")
    for page in root:
      if int(page.find("id").text) == pageid:
        return page
    raise LookupError

  def get_page_markdown(self, block_offset, pageid):
    page_et = self.get_page_ET(block_offset, pageid)
    return page_et.find("revision").find("text").text

