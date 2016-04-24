#!/usr/bin/python3
# coding=utf-8
import re
import binascii
import random
import sys
import getopt
import codecs

class AppError(Exception):

  pass

class EnglishKoreanDict:

  def __init__(self):
    f = codecs.open('dict.txt', encoding='utf-8-sig')
    self.e_to_k = {} 
    self.k_to_e = {} 
    for line in f:
      line = line.strip()
      if line == "":
        continue
      if line[0] =="#":
        continue
      m = re.search(r"^([ -~]+) (.+) ([0-9,]+)\s*$", line)
      if not m:
        raise AppError("Failed to match in: %s" % line)
      tag_nums = m.group(3).split(",")
      tag_dict = {}
      for i in range(0,len(tag_nums)):
        tag_dict[int(tag_nums[i])] = 1
      self.e_to_k[m.group(1)] = (m.group(2), tag_dict);
      self.k_to_e[m.group(2)] = (m.group(1), tag_dict);

  def all_words_randomized_repeats(self, words, groups):
    while True:
      w = list(words.keys())[random.randint(0,len(words.keys())-1)]
      if self.check_word(words, w, groups):
        yield w

  def all_words_randomized(self, words, groups):
    w = list(words.keys())
    random.shuffle(w)
    for ww in w:
      if self.check_word(words, ww, groups):
        yield ww

  def all_words_ordered(self, words, groups):
    w = list(words.keys())
    w.sort()
    for ww in w:
      if self.check_word(words, ww, groups):
        yield ww

  def check_word(self, words, ww, groups):
    if groups == None:
      return True
    for group in groups:
      if words[ww][1].get(group):
        return True
    return False

  def word_game(self, words, word, extra_wait):
    print(word)
    sys.stdin.readline()
    print(words[word][0])
    if (extra_wait):
      sys.stdin.readline()
    print()

  def words_game(self, words, count, groups, word_callback, extra_wait):
    x=0
    for w in word_callback(words, groups):
      x+=1
      if x>count:
        return
      print("%d)" % x)
      print()
      self.word_game(words, w, extra_wait)

  def run(self, argv):
    try:
      opts, args = getopt.getopt(argv, "en:g:row")
    except getopt.GetoptError:
      print("Invalid arguments")
      return 2
    english = False
    groups = None
    count = 10
    ordered = False
    allow_repeats = False
    extra_wait = False
    word_dict = self.k_to_e
    for opt, arg in opts:
      if opt == "-n":
        count = int(arg)
      elif opt == "-e":
        word_dict = self.e_to_k
      elif opt == "-g":
        groups = list(map(int, arg.split(",")))
      elif opt == "-o":
        ordered = True
      elif opt == "-w":
        extra_wait = True
      elif opt == "-r":
        allow_repeats = True
    if ordered:
      sorter = self.all_words_ordered
    elif allow_repeats:
      sorter = self.all_words_randomized_repeats
    else:
      sorter = self.all_words_randomized
    self.words_game(word_dict, count, groups, sorter, extra_wait);

if __name__ == "__main__":
  d = EnglishKoreanDict()
  d.run(sys.argv[1:])



