# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 15:12:32 2019

@author: Administrator
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import csv
import os
from io import open
import jieba

g_corpus_name = "xiaohuangji"
g_corpus = os.path.join("data", g_corpus_name)

g_corpus_file = os.path.join(g_corpus, "xiaohuangji50w_nofenci.conv")
g_datafile = os.path.join(g_corpus, "formatted_movie_lines.txt")


def load_conversations(corpus_file):
	conversations = []
	with open(g_corpus_file, encoding='utf8') as f:
		one_conv = []  # 存储一次完整对话
		for line in f:
			# print(line)
			line = line.strip('\n').replace('/', '')  # 去除换行符，并在字符间添加空格符，原因是用于区分 123 与1 2 3.
			if line == '':
				continue
			if line[0] == 'E':
				if one_conv:
					conversations.append(one_conv)
				one_conv = []
			elif line[0] == 'M':
				one_conv.append(line.split(' ')[1])  # 将一次完整的对话存储下来
	return conversations


def extract_sentence_pairs(conversations):
	qa_pairs = []
	for conversation in conversations:
		if len(conversation) == 1:
			continue
		if len(conversation) % 2 != 0:  # 因为默认是一问一答的，所以需要进行数据的粗裁剪，对话行数要是偶数的
			conversation = conversation[:-1]
		for i in range(len(conversation)):
			conversation[i] = " ".join(jieba.cut(conversation[i]))  # 使用jieba分词器进行分词
			if i % 2 == 0:
				ask = conversation[i]  # 因为i是从0开始的，因此偶数行为发问的语句，奇数行为回答的语句
			else:
				qa_pairs.append([ask, conversation[i]])
	return qa_pairs


def print_lines(file, n=10):
	with open(file, 'r', encoding='utf-8') as datafile:
		lines = datafile.readlines()
	for line in lines[:n]:
		print(line)


def main():
	print_lines(g_corpus_file)
	conversations = load_conversations(g_datafile)
	pairs = extract_sentence_pairs(conversations)

	delimiter = '\t'
	# Unescape the delimiter
	delimiter = str(codecs.decode(delimiter, "unicode_escape"))
	print('done')

	# Write new csv file
	print("\nWriting newly formatted file...")
	with open(g_datafile, 'w', encoding='utf-8') as outputfile:
		writer = csv.writer(outputfile, delimiter=delimiter, lineterminator='\n')
		for pair in pairs:
			writer.writerow(pair)

	# Print a sample of lines
	print("\nSample lines from file:")
	print_lines(g_datafile)


if __name__ == '__main__':
	main()
