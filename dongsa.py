#!/usr/bin/python3
# coding=utf-8

import requests
import json
import random

class DongsaError(Exception):

  pass

class Dongsa:

  def __init__(self):
    self.url = "http://dongsa.net/api/v1/conjugation"

  def conjugate(self, verb):
    r = requests.post(self.url, {'verb': verb})
    decode_1 = json.loads(r.text)
    decode_2 = json.loads(decode_1['conjugation'])
    return decode_2

  def random_form(self, verb):
    conj = self.conjugate(verb)
    conj = [x for x in conj if x['type'] == 'conjugation']
    item = random.sample(conj, 1)[0]
    return (item['conjugated'], item['infinitive'])


if __name__ == "__main__":
  d = Dongsa()
  #conj = d.conjugate("하다")
  #print(json.dumps(d.conjugate("하다"), separators=(',', ': ')))
  print(repr(d.random_form("하다")))


    

