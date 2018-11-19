"""
Classes for parsing Korean Wiktionary.
"""

import mwparserfromhell as mwp
from collections import namedtuple
import re

HanjaUsage = namedtuple('HanjaUsage', ['hanjas', 'hangul'])
HanjaDef = namedtuple('HanjaDef', ['hanja', 'pos', 'defentry'])

def get_hanja_usage(wcode):
  template_name = "한자활용"
  templates = [t for t in wcode.filter_templates() if t.name == template_name] 
  assert(len(templates) <= 1)
  if len(templates) == 0:
    return None
  template = templates[0]
  hangul = template.get("한글").value
  hanjas = [p.value for p in template.params if p.name != "한글"]
  return HanjaUsage(hanjas, hangul)

def raw_headings(wcode):
  return [h.title.strip() for h in s.ifilter_headings()]

def wcode_raw_heading(wcode):
  if len(wcode.nodes) == 0:
    return None
  firstnode = wcode.nodes[0]
  if firstnode is None or \
      type(firstnode) != mwp.nodes.heading.Heading:
    return None
  return firstnode.title.strip()
  

def find_title_section(wcode, title):
  tsects = [s for s in wcode.get_sections() if title == wcode_raw_heading(s)]
  print(tsects)
  assert(len(tsects) <= 1)
  if len(tsects) == 0:
    return None
  return tsects[0]

def hanja_section(wcode):
  # Find the wcode subsection whose first heading is "한자"
  return find_title_section(wcode, "한자")

def japanese_section(wcode):
  return find_title_section(wcode, "일본어")

def hangul_section(wcode):
  return find_title_section(wcode, "한글")

#          noun,  verb, adjective, adverb, coord.,   preposition, pronoun, interjection,
KO_POS = ["명사", "동사", "형용사", "부사", "접속사", "전치사", "대명사", "감탄사"] + \
  ["조동사", "관사", "한정사"]
# aux. verb, article, determiner 

def is_def_tag(tag):
  content = tag.contents
  try:
    num = int(content[:len(content) - 1])
    if content == "{}.".format(num):
      return True
    else:
      return False
  except:
    return False


# wcode to just lines to text.
def wcode_to_lines(wcode):
  return str(wcode).split("\n")


class KOWikHanjaHanja:
  def __getdefs__(hanja, wcode):
    # Get all sections grouped by POS.
    possects = [s for s in wcode.get_sections() if wcode_raw_heading(s) in KO_POS]
    defs = []
    for possect in possects:
      pos = wcode_raw_heading(possect)
      # Find definition entries.
      indef = False
      for n in possect.nodes:
        if indef and type(n) == mwp.nodes.text.Text: 
          # TODO: handle whatever type the double brackets are, e.g. [[주의]]
          defs.append(HanjaDef(hanja, pos, n.value.strip()))
        if indef:
          indef = False
        if type(n) == mwp.nodes.tag.Tag and is_def_tag(n):
          indef = True
    return defs

  def __init__(self, wcode, hanja=None):
    if "한자" != wcode_raw_heading(wcode):
      raise ValueError("wcode must have be a Hanja section, as indicated by the 한자 heading")
    if hanja:
      self.hanja = hanja
    self.hanja_usage = get_hanja_usage(wcode)
    self.hanja_list = self.hanja_usage.hanjas
    if self.hanja:
      assert(list(self.hanja) == self.hanja_list)
    if not self.hanja:
      self.hanja = "".join(self.hanja_list)
    self.hangul = self.hanja_usage.hangul
    self.defs = KOWikHanjaHanja.__getdefs__(self.hanja, wcode) 

  def get_hanja(self):
    return self.hanja

  def get_hangul(self):
    return self.hangul

  def get_defs(pos=None):
    curdefs = self.defs
    if pos:
      curdefs = [d for d in curdefs if d.pos == pos]
    return curdefs





class KOWikHanjaJapanese:

  def __getdefs__(hanja, wcode):
    # Get all sections grouped by POS.
    possects = [s for s in wcode.get_sections() if wcode_raw_heading(s) in KO_POS]
    defs = []
    for possect in possects:
      pos = wcode_raw_heading(possect)
      # Find definition entries.
      indef = False
      # TODO: filter nodes with empty text...
      # TODO: also look into langdetect? (python library)
      for n in possect.nodes:
        if indef and type(n) == mwp.nodes.text.Text: 
          # TODO: handle whatever type the double brackets are, e.g. [[주의]]
          defs.append(HanjaDef(hanja, pos, n.value.strip()))
        if indef:
          indef = False
        if type(n) == mwp.nodes.tag.Tag and is_def_tag(n):
          indef = True
    return defs

  def __gethira__(wcode):
    kohira = "히라가나"
    hiralines = [l for l in wcode_to_lines(wcode) if kohira in l]
    if len(hiralines) == 0:
      return None
    hline = hiralines[0]
    remain = hline.split(kohira)[1]
    # Filter punctuation.
    return re.sub(r'[^\w\s]', '', remain)    

  def __getromaji__(wcode):
    koromaji = "로마자 표기"
    romajilines = [l for l in wcode_to_lines(wcode) if koromaji in l]
    if len(romajilines) == 0:
      return None
    hline = romajilines[0]
    remain = hline.split(koromaji)[1]
    # Filter punctuation.
    return re.sub(r'[^\w\s]', '', remain)    


  def __init__(self, wcode, hanja=None):
    if "일본어" != wcode_raw_heading(wcode):
      raise ValueError("wcode must have be a Japanese section, as indicated by the 일본어 heading")
    if hanja:
      self.hanja = hanja
    self.hira = KOWikHanjaJapanese.__gethira__(wcode)
    self.romaji = KOWikHanjaJapanese.__getromaji__(wcode)
    self.defs = KOWikHanjaJapanese.__getdefs__(self.hanja, wcode) 

  def get_hanja(self):
    return self.hanja

  def get_hira(self):
    return self.hira

  def get_romaji(self):
    return self.romaji

  def get_defs(pos=None):
    curdefs = self.defs
    if pos:
      curdefs = [d for d in curdefs if d.pos == pos]
    return curdefs

