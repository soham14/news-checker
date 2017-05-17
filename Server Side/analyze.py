#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import nltk

paragraph = unicode(sys.argv[1], errors="replace")

sentences = tokenize.sent_tokenize(paragraph)
analyzer = SentimentIntensityAnalyzer()

result = {"pos": 0, "neu": 0, "neg": 0, "compound": 0}

if len(sentences) == 0:
        print(json.dumps(result))
        exit(0)

for sentence in sentences:
	scores = analyzer.polarity_scores(sentence)
	c = scores["compound"]
	result["compound"] += c
	if c >= .5:
		result["pos"] += 1
	elif c <= -.5:
		result["neg"] += 1
	else:
		result["neu"] += 1

for k in result.keys():
	result[k] = result[k] / (len(sentences) + 0.0)

def tree_create(sent):
	a = nltk.word_tokenize(sent)
	b = nltk.pos_tag(a)
	c = nltk.ne_chunk(b)
	return c

def tree_choose(tree):
	r = {}
	for t in tree:
		if type(t) == nltk.Tree and t.label() in ["GPE", "ORGANIZATION", "PERSON"]:
			temp = []
			for u in t:
				temp += [u[0]]
			word = " ".join(temp)
			if word in r.keys():
				r[word] += 1
			else:
				r[word] = 1
	return r

ret = {}

for s in sentences:
	d = tree_choose(tree_create(s))
	for k in d.keys():
		if k in ret.keys():
			ret[k] += d[k]
		else:
			ret[k] = d[k]

result["top_words"] = sorted(ret, key=ret.get, reverse=True)[:20]
result["num_sentences"] = len(sentences)
result["num_words"] = len(tokenize.word_tokenize(paragraph))
result["mins"] = result["num_words"] / 200
result["secs"] = int((((result["num_words"] % 200) / (200 + 0.0)) * 60))

print(json.dumps(result))
