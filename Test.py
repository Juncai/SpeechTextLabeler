__author__ = 'juncai'

from Utilities import get_time_stamp, build_sentiment_dict, read_pitches, read_intensities, build_sentence_info
import re
from hyphen import Hyphenator
import numpy as np


for i in range(6):
    print i


# sentiment_dict_path = '/Users/juncai/Dropbox/PlaIT Lab/TRUST/Sentiment_Analysis/reproduce/pitt_lexicon_reproduce.txt'
#
# bml_path = 'User_HighHigh_Intro_May13_S2.bml'
#
# int_path = 'User_HighHigh_Intro_May13_S2_int'
#
# pitch_path = 'User_HighHigh_Intro_May13_S2_pitch'
#
# text_path = 'User_HighHigh_Intro_May13_S2.txt'
#
#
# pitch_info = read_pitches(pitch_path)
# int_info = read_intensities(int_path)
# sent_dict = build_sentiment_dict(sentiment_dict_path)
# timestamps = get_time_stamp(bml_path)
# sen = open(text_path).readline()
# sen_info = build_sentence_info(timestamps, sen, sent_dict)
#
#


# pitch_array = np.array(pitch_info[1])
# print np.mean(pitch_array)
# print np.std(pitch_array)

# sent_dict = build_sentiment_dict(sentiment_dict_path)
#
# for key in sent_dict:
#     print key
#
# ts = get_time_stamp(bml_path)
#
# for t in ts:
#     print t

# words = re.split('\W+', 'OK, well, shall we start? Welcome to Finnmore Associates!')
# words.remove('')
# for ind, word in enumerate(words):
#     print word, ind

h_en = Hyphenator('en_US')
#
print len(h_en.syllables(unicode(u'beautiful')))
#
# alist = [1, 2, 4, 2, 5, 6, 9.1]
# barray = np.array(alist)
# dev = np.std(barray)
# m = np.mean(barray)
# print m
# print dev

