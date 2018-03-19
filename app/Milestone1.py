from bs4 import BeautifulSoup
import re
from collections import defaultdict
import nltk
from Readjson import json_dict
from nltk.corpus import stopwords
import nltk.data
import os
import time
import unicodedata
import math
from ReadEnglishDictionary import read_en_dict
import json

class RunProgram:

    def __init__(self):
        self.inverted_index = defaultdict(lambda: defaultdict(int))
        self.json_dict = json_dict()
        self.regex = re.compile("[\W_]+")
        # Below are new additions for part 2
        self.document_count = 1
        self.unigram_dict = defaultdict(lambda: defaultdict(int))
        self.bigram_dict = defaultdict(lambda: defaultdict(int))
        self.term_count_dict = defaultdict(int)
        # END
        self.parser = Parser(self.regex, self.inverted_index, self.json_dict, self.term_count_dict, self.unigram_dict, self.bigram_dict)
        self.program_duration = 0

    def walking(self, dirpath):
        try:
            # self.program_duration = time.time()
            for root, dirs, files in os.walk(dirpath):
                for file in files:
                    if (file == '.DS_Store'): continue # comment out for windows
                    print ("Processing file: {}".format(os.path.join(root, file)))
                    self.document_count += 1
                    start_time = time.time()
                    self.parser.construct(os.path.join(root, file))
                    print ("Time: {} ".format(time.time() - start_time))
            # self.program_duration = time.time() - self.program_duration
            return self.inverted_index
        except:
            print("Failed to walk through directory: " + dirpath)
            pass

    def size_of_index(self):
        return len(self.inverted_index)

    def tf(self, word, docid):
        # term freq per document
        # format : {"term" : { docid: count, docid: count ... } }
        return self.unigram_dict[word][docid]

    def idf(self, word):
        try:
            return math.log(self.document_count / float(1 + self.term_count_dict[word]))
        except Exception as e:
            print ("Error while computing idf: " + e.message)
            return 1.0

    def tf_idf(self, word, docid):
        return self.tf(word, docid) * self.idf(word)




class Parser:

    def __init__(self, regex, inverted_index, json, term_count_dict, unigram_dict, bigram_dict):
        self.regex = regex
        self.json = json
        self.inverted_index = inverted_index
        self.stopwords = set(stopwords.words('english'))
        self.term_count_dict = term_count_dict
        self.unigram_dict = unigram_dict
        self.bigram_dict = bigram_dict
        self.eng_dict = read_en_dict()


    def construct(self, filepath):
        #Windows
        # temp_f = filepath.split('WEBPAGES_RAW\\')[-1]
        #OSX
        temp_f = filepath.split('WEBPAGES_RAW/')[-1]
        # self.docid = "/".join(temp_f.split("\\"))
        self.docid = "/".join(temp_f.split("\\"))
        self.soup = self.create_soup(filepath)
        self.tokenized_dict = self.word_freq_dict()

    def create_soup(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return BeautifulSoup(f, 'html.parser')
        except IOError as e:
            print ("Error in Parser.createSoup() : " + e.message)

    def word_freq_dict(self):
        try:
            for string in self.soup.stripped_strings:
                token_line = [word for word in nltk.regexp_tokenize(string.lower(),
                              pattern=self.regex, gaps=True, discard_empty=True)
                              if word not in self.stopwords and not self.is_number_u(word) and word in self.eng_dict]
                if token_line:
                    for unigram in nltk.ngrams(token_line, 1):
                        self.term_count_dict[unigram[0]] += 1
                        self.unigram_dict[unigram[0]][self.docid] += 1
                    # for bigram in nltk.ngrams(token_line, 2):
                    #     self.bigram_dict[" ".join(sorted(bigram))][self.docid] += 1
                    # for trigram in nltk.ngrams(token_line, 3):
                    #     self.inverted_index[" ".join(sorted(trigram))][self.docid] += 1
            return self.inverted_index
        except Exception as e:
            print("Error while tokenizing: " + e.message)

    def is_number_u(self, string):
        try:
            float(string)
            return True
        except ValueError:
            pass
        try:
            unicodedata.numeric(string)
            return True
        except (TypeError, ValueError):
            pass
        return False


class ProcessFile:

    def __init__(self):
        self.f = None

    def process_analytics(self, indexsize):
        try:
            if self.f is None:
                raise IOError("File is not opened")
            self.f.write('Inverted Index Size: {}\n'.format(indexsize))
            self.f.write("\n")
        except IOError, msg:
            print ("Error in process_analytics(): " + str(msg))

    def add_query(self, query):
        try:
            if self.f is None:
                raise IOError("File is not opened")
            self.f.write('Query: {}\n'.format(query))
            self.f.write('Results: \n')
            self.f.write("\n")
        except IOError, msg:
            print ("Error in add_query(): " + str(msg))

    def add_url(self, docid, tf, url):
        try:
            if self.f is None:
                raise IOError("File is not opened")
            self.f.write("Docid: {}\n".format(docid))
            self.f.write("Term Freq: {}\n".format(tf))
            self.f.write("URL: {}\n".format(url.encode("utf-8")))
            self.f.write("\n")
        except IOError as e:
            print ("Error while adding to file : {}".format(e.message))

    def open_file(self):
        try:
            self.f = open("Analytics.txt", 'a+')
        except IOError:
            print ("Error opening Analytics.txt")

    def close_file(self):
        try:
            if self.f is None:
                raise IOError("File is not opened")
            self.f.write("\n")
            self.f.close()
        except IOError:
            print ("File failed to close!")
