#!/usr/bin/python
# coding=utf-8
import re
import binascii
import random
import sys
import getopt

class AppError(Exception):
  pass

class EnglishKoreanDict:
  def __init__(self):
    f = open("dict.txt", "r")
    self.e_to_k = {} 
    self.k_to_e = {} 
    for line in f:
      line = line.strip()
      if line == "":
        continue
      if line[0] =="#":
        continue
      m = re.search(r"^(\xef\xbb\xbf)?([\x20-\x7e]+) (.+) ([0-9,]+)\s*$", line)
      if not m:
        raise AppError("Failed to match in: %s" % line)
      tag_nums = m.group(4).split(",")
      tag_dict = {}
      for i in range(0,len(tag_nums)):
        tag_dict[int(tag_nums[i])] = 1
      self.e_to_k[m.group(2)] = (m.group(3), tag_dict);
      self.k_to_e[m.group(3)] = (m.group(2), tag_dict);
  def random_word(self, words, group):
    while True:
      w = words.keys()[random.randint(0,len(words.keys())-1)]
      if group == 0 or words[w][1].get(group):
        return w
  def random_word_game(self, words, group):
    e = self.random_word(words, group)
    print e
    sys.stdin.readline()
    print words[e][0]
    print
  def random_words_game(self, words, count, group):
    for x in range(0, count):
      print "%d)" % x
      print
      self.random_word_game(words, group)
  def random_korean_words_game(self, count, group):
    self.random_words_game(self.k_to_e, count, group);
  def random_english_words_game(self, count, group):
    self.random_words_game(self.e_to_k, count, group);
  def run(self, argv):
    try:
      opts, args = getopt.getopt(argv, "en:g:")
    except getopt.GetoptError:
      print "Args: -n [number]"
      return 2
    english = False
    group = 0
    n = 10
    for opt, arg in opts:
      if opt == "-n":
        n = int(arg)
      elif opt == "-e":
        english = True
      elif opt == "-g":
        group = int(arg)
    if english:
      self.random_english_words_game(n, group)
    else:
      self.random_korean_words_game(n, group)
    

if __name__ == "__main__":
  d = EnglishKoreanDict()
  d.run(sys.argv[1:])



