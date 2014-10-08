__author__ = 'juncai'

import xml.etree.ElementTree as ET
from hyphen import Hyphenator
import re
import numpy as np
import text2num as t2n
from data_classes import SentenceData, WordData

# constants
STD_COEF = 1.0
ATTRIB_TEXT = "text"
ATTRIB_START = "start"
ATTRIB_END = "end"
ATTRIB_EMPH = "emphasis"
ATTRIB_SENTIMENT = "sentiment"
ATTRIB_SPE = "special"
ATTRIB_SYLLABLES = "syllables"
ATTRIB_DURATION = "duration"
ATTRIB_SPEED = "speed"
ATTRIB_PUNCT = "punctuation"
POS_SENTIMENT = "positive"
NEG_SENTIMENT = "negative"

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
    """

    :rtype : dict
    """
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
    '''
    Build sentence info from timestamps, sentence text and sentiment lexicon
    :param timestamps:
    :param sentence:
    :param sent_dict:
    :return:
    '''
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
        num = t2n.text2num(word)
        info_list.append((word,
                          timestamps[ind * 2],
                          timestamps[ind * 2 + 1],
                          len(h_en.syllables(unicode(word))),
                          c_sentiment,
                          punct,
                          num))
    return info_list


def build_sentence_data(title, timestamps, sentence, sent_dict):
    '''
    Build sentence info from timestamps, sentence text and sentiment lexicon
    :param timestamps:
    :param sentence:
    :param sent_dict:
    :return: a SentenceData object contain text-based information about the sentence
    '''
    # for test
    # print sentence

    s = SentenceData(title, sentence)
    s.words = []

    h_en = Hyphenator('en_US')
    words = re.split('[,.!?\r\n ]+', sentence)

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
        num = t2n.text2num(word)
        if num == -1:
            num = ''
        else:
            num = str(num)
        w = WordData(word, float(timestamps[ind * 2]), float(timestamps[ind * 2 + 1]), c_sentiment,
                     len(h_en.syllables(unicode(word))), punct, num)
        s.words.append(w)
    return s


def find_emphasis(intensity, pitch, info):
    '''
    Find emphasis time stamps according to the pitch information
    @param int: a tuple of two lists. First list contains timestamps, second contains intensities
    @param pitch: a tuple of two lists. First list contains timestamps, second contains pitches
    @param info: a list of tuples, each tuple contains the info for one word which are text, start time,
    end time, number of syllables, sentiment
    @return: a set of integers represent the index of emphasized words in the info input.
    '''

    pitch_mean = pitch[2]
    pitch_std = pitch[3]
    word_ind_set = set()

    for ind, p in enumerate(pitch[1]):
        if pitch_is_emphasis(p, pitch_mean, pitch_std):
            for i, inf in enumerate(info):
                if float(pitch[0][ind]) >= float(inf[1]) and float(pitch[0][ind]) <= float(inf[2]):
                    word_ind_set.add(i)
    return word_ind_set


def fill_acoustic_data(intensity, pitch, sentence):
    '''
    Find emphasis time stamps according to the pitch information
    @param int: a tuple of two lists. First list contains timestamps, second contains intensities
    @param pitch: a tuple of two lists. First list contains timestamps, second contains pitches
    @param sentence: a SentenceData object containing text-base data of that sentence
    @return: the analyzed sentence.
    '''

    sentence.pitch_ts = pitch[0]
    sentence.pitch_list = pitch[1]
    sentence.pitch_mean = pitch[2]
    sentence.pitch_std = pitch[3]
    sentence.duration = pitch[4]
    sentence.intensity_ts = intensity[0]
    sentence.intensity_list = intensity[1]
    sentence.intensity_mean = intensity[2]
    sentence.intensity_std = intensity[3]

    for ind, ts in enumerate(sentence.pitch_ts):
        for w in sentence.words:
            if float(ts) >= w.start_time and float(ts) <= w.end_time:
                # w.pitch_ts.append(ts)
                w.pitch_list.append(sentence.pitch_list[ind])

    for ind, ts in enumerate(sentence.intensity_ts):
        for w in sentence.words:
            if float(ts) >= w.start_time and float(ts) <= w.end_time:
                # w.intensity_ts.append(ts)
                w.intensity_list.append(sentence.intensity_list[ind])

    for w in sentence.words:
        if len(w.pitch_list) > 0:
            w.pitch_mean = np.array(w.pitch_list).mean()
        else:
            w.pitch_mean = 0
        if len(w.intensity_list) > 0:
            w.intensity_mean = np.array(w.intensity_list).mean()
        else:
            w.intensity_mean = 0
        w.acoustic_data_filled = True

    sentence.acoustic_data_filled = True
    return sentence


def find_emphasis_alone(sentence):
    for ind, p in enumerate(sentence.pitch_list):
        if pitch_is_emphasis(p, sentence.pitch_mean, sentence.pitch_std):
            for i, w in enumerate(sentence.words):
                if float(sentence.pitch_ts[ind]) >= w.start_time and float(sentence.pitch_ts[ind]) <= w.end_time:
                    w.is_emphasis = True
    return sentence


def find_emphasis_object(intensity, pitch, sentence):
    '''
    Find emphasis time stamps according to the pitch information
    @param int: a tuple of two lists. First list contains timestamps, second contains intensities
    @param pitch: a tuple of two lists. First list contains timestamps, second contains pitches
    @param sentence: a SentenceData object containing text-base data of that sentence
    @return: the analyzed sentence.
    '''

    sentence.pitch_ts = pitch[0]
    sentence.pitch_list = pitch[1]
    sentence.pitch_mean = pitch[2]
    sentence.pitch_std = pitch[3]
    sentence.duration = pitch[4]
    sentence.intensity_ts = intensity[0]
    sentence.intensity_list = intensity[1]
    sentence.intensity_mean = intensity[2]
    sentence.intensity_std = intensity[3]

    for ind, p in enumerate(sentence.pitch_list):
        if pitch_is_emphasis(p, sentence.pitch_mean, sentence.pitch_std):
            for i, w in enumerate(sentence.words):
                if float(sentence.pitch_ts[ind]) >= w.start_time and float(sentence.pitch_ts[ind]) <= w.end_time:
                    w.is_emphasis = True
    return sentence


def pitch_is_emphasis(p, mean, std):
    return p >= mean + STD_COEF * std


def read_intensities(path):
    timestamp = []
    intensities = []
    f = open(path)
    meta = f.readline().split()
    mean = float(meta[1])
    std = float(meta[3])
    c_line = f.readline()
    while len(c_line) != 0:
        strings = c_line.split()
        c_line = f.readline()
        timestamp.append(float(strings[0]))
        intensities.append(float(strings[1]))
    return timestamp, intensities, mean, std


def read_intensities_from_autofile(path):
    timestamp = []
    intensities = []
    f = open(path)
    meta = f.readline().split()
    mean = float(meta[1])
    std = float(meta[3])
    duration = float(meta[5])
    c_line = f.readline()
    while len(c_line) != 0:
        strings = c_line.split()
        c_line = f.readline()
        timestamp.append(float(strings[0]))
        intensities.append(float(strings[1]))
    return timestamp, intensities, mean, std, duration


def read_pitches_from_autofile(path):
    timestamp = []
    pitches = []
    f = open(path)
    meta = f.readline().split()
    mean = float(meta[1])
    std = float(meta[3])
    duration = float(meta[5])
    c_line = f.readline()
    while len(c_line) != 0:
        strings = c_line.split()
        c_line = f.readline()
        if strings[1] != '--undefined--':
            timestamp.append(float(strings[0]))
            pitches.append(float(strings[1]))
    return timestamp, pitches, mean, std, duration


def read_pitches(path):
    '''
    Read pitch list from the given path and return a list containing the data
    @param path: the path of the pitch list file
    @return: a list containing the pitch data
    '''
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
    '''
    :param info:
    :param int_path:
    :param pitch_path:
    :return: a sentence text with emphasis and sentiment label
    '''
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
        if int(w_info[6]) != -1:
            sentence += '[' + str(int(w_info[6])) + ']'
        if int(w_info[3]) > 0:
            sentence += '[' + str(int(w_info[3]) / (float(w_info[2]) - float(w_info[1]))) + ']'
        if len(w_info[5]) > 0:
            sentence += w_info[5]
        sentence += ' '
    return sentence


def label_the_sentence_to_et(sentence_data, int_path, pitch_path):
    '''
    Labeling the sentence and generate a utf-8 string representing a XML file
    @param info: a list of tuples contain information of the sentence, each tuple contains information
     for a word in the sentence.
    @param int_path: the path string of the intensity list file.
    @param pitch_path: the path string of the pitch list file.
    @return: an ElementTree containing information of the labeled sentence.
    '''
    # building a tree structure
    # sentence_data = find_emphasis_object(read_intensities_from_autofile(int_path),
    #                                         read_pitches_from_autofile(pitch_path),
    #                                         sentence_data)
    fill_acoustic_data(read_intensities_from_autofile(int_path),
                       read_pitches_from_autofile(pitch_path),
                       sentence_data)
    find_emphasis_alone(sentence_data)
    return build_xml_tree(sentence_data)


def build_xml_tree(sentence_data):
    sentence = ET.Element("sentence")
    sentence.set(ATTRIB_DURATION, str(sentence_data.duration))
    sentence.set("title", sentence_data.title)

    for ind, w in enumerate(sentence_data.words):
        word = ET.SubElement(sentence, "word")
        word.text(ATTRIB_TEXT, w.text)
        word.set(ATTRIB_START, str(w.start_time))
        word.set(ATTRIB_END, str(w.end_time))

        if w.is_emphasis:
            word.set(ATTRIB_EMPH, "true")
        else:
            word.set(ATTRIB_EMPH, "false")
        if w.sentiment == 1:
            word.set(ATTRIB_SENTIMENT, POS_SENTIMENT)
        if w.sentiment == -1:
            word.set(ATTRIB_SENTIMENT, NEG_SENTIMENT)
        if len(w.special) != 0:
            word.set(ATTRIB_SPE, w.special)
        word.set(ATTRIB_SYLLABLES, str(w.num_syllables))
        word.set(ATTRIB_DURATION, str(w.end_time - w.start_time))
        if w.num_syllables > 0:
            word.set(ATTRIB_SPEED, str(w.num_syllables / (w.end_time - w.start_time)))
        if len(w.punct_after) > 0:
            word.set(ATTRIB_PUNCT, w.punct_after)
    return ET.ElementTree(sentence)

# if __name__ == '__main__':
#     sentiment_dict_path = '/Users/juncai/Dropbox/PlaIT Lab/TRUST/Sentiment_Analysis/reproduce/pitt_lexicon_reproduce.txt'
#
#     bml_path = 'User_HighHigh_Intro_May13_S3.bml'
#
#     int_path = 'User_HighHigh_Intro_May13_S3_int'
#
#     pitch_path = 'User_HighHigh_Intro_May13_S3_pitch'
#
#     text_path = 'User_HighHigh_Intro_May13_S3.txt'
#
#     sent_dict = build_sentiment_dict(sentiment_dict_path)
#     timestamps = get_time_stamp(bml_path)
#     sen = open(text_path).readline()
#     sen_info = build_sentence_info(timestamps, sen, sent_dict)
#
#     print label_the_sentence(sen_info, int_path, pitch_path)
