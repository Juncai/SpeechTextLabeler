__author__ = 'juncai'

import xml.etree.ElementTree as ET
from hyphen import Hyphenator
import re
import numpy as np

filePre = 'User_HighHigh_Intro_May13_S1.bml'
filePost = '.bml'


def get_time_stamp(path):
    tree = ET.parse(path)
    root = tree.getroot()
    timestamps = []

    for child in root:
        if child.tag == 'speech':
            for ch in child:
                if ch.tag == 'text':
                    for c in ch:
                        timestamps.append(c.get('time'))
    return timestamps


def build_sentiment_dict(path):
    sentiment_dict = {}
    f = open(path)
    cline = f.readline()
    while len(cline) != 0:
        strings = cline.split()
        cline = f.readline()
        if strings[2] not in sentiment_dict:
            sentiment_value = {'positive': 1,
                               'negative': -1,
                               'neutral': 0,
                               'both': 0}[strings[0]]
            sentiment_dict[strings[2]] = sentiment_value
    return sentiment_dict


def build_sentence_info(timestamps, sentence, sent_dict):
    # for test
    # print sentence

    h_en = Hyphenator('en_US')
    info_list = []
    # words = re.split('\W+', sentence)
    words = re.split('[,.!?\r\n ]+', sentence)
    # print words
    # print len(words)
    # print len(timestamps)
    words.remove('')
    words_with_punct = sentence.split()

    for ind, word in enumerate(words):
        if word in sent_dict:
            c_sentiment = sent_dict[word]
        else:
            c_sentiment = 0
        punct = ''
        if words_with_punct[ind] != word:
            punct = words_with_punct[ind][-1]
        info_list.append((word,
                          timestamps[ind * 2],
                          timestamps[ind * 2 + 1],
                          len(h_en.syllables(unicode(word))),
                          c_sentiment,
                          punct))
    return info_list


def find_emphasis(int, pitch, info):
    '''
    Find emphasis time stamps according to the pitch information
    @param int: a tuple of two lists. First list contains timestamps, second contains intensities
    @param pitch: a tuple of two lists. First list contains timestamps, second contains pitches
    @param info: a list of tuples, each tuple contains the info for one word which are text, start time,
    end time, number of syllables, sentiment
    @return: a sentence text with emphasis and sentiment label
    (a set of integers represent the index of emphasized words in the info input.)
    '''

    pitch_array = np.array(pitch[1])
    pitch_mean = np.mean(pitch_array)
    pitch_std = np.std(pitch_array)
    word_ind_set = set()

    for ind, p in enumerate(pitch[1]):
        if pitch_is_emphasis(p, pitch_mean, pitch_std):
            for i, inf in enumerate(info):
                if float(pitch[0][ind]) >= float(inf[1]) and float(pitch[0][ind]) <= float(inf[2]):
                    word_ind_set.add(i)
    return word_ind_set


def pitch_is_emphasis(p, mean, std):
    std_coef = 1.0
    return p >= mean + std_coef * std


def read_intensities(path):
    timestamp = []
    intensities = []
    f = open(path)
    f.readline()
    c_line = f.readline()
    while len(c_line) != 0:
        strings = c_line.split()
        c_line = f.readline()
        timestamp.append(float(strings[0]))
        intensities.append(float(strings[1]))
    return timestamp, intensities


def read_pitches(path):
    timestamp = []
    pitches = []
    f = open(path)
    f.readline()
    c_line = f.readline()
    while len(c_line) != 0:
        strings = c_line.split()
        c_line = f.readline()
        if strings[1] != '--undefined--':
            timestamp.append(float(strings[0]))
            pitches.append(float(strings[1]))
    return timestamp, pitches


def label_the_sentence(info, int_path, pitch_path):
    sentence = ''
    emphasis_indices = find_emphasis(read_intensities(int_path), read_pitches(pitch_path), info)
    for ind, w_info in enumerate(info):
        sentence += w_info[0]
        if ind in emphasis_indices:
            sentence += '[e]'
        if int(w_info[4]) == 1:
            sentence += '[p]'
        if int(w_info[4]) == -1:
            sentence += '[n]'
        if len(w_info[5]) > 0:
            sentence += w_info[5]
        sentence += ' '
    return sentence

if __name__ == '__main__':
    sentiment_dict_path = '/Users/juncai/Dropbox/PlaIT Lab/TRUST/Sentiment_Analysis/reproduce/pitt_lexicon_reproduce.txt'

    bml_path = 'User_HighHigh_Intro_May13_S3.bml'

    int_path = 'User_HighHigh_Intro_May13_S3_int'

    pitch_path = 'User_HighHigh_Intro_May13_S3_pitch'

    text_path = 'User_HighHigh_Intro_May13_S3.txt'

    sent_dict = build_sentiment_dict(sentiment_dict_path)
    timestamps = get_time_stamp(bml_path)
    sen = open(text_path).readline()
    sen_info = build_sentence_info(timestamps, sen, sent_dict)

    print label_the_sentence(sen_info, int_path, pitch_path)
