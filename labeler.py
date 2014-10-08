__author__ = 'juncai'


import utilities as ut
import re
import numpy as np
from data_classes import LearningData

SENTIMENT_DICT = '/Users/juncai/Dropbox/PlaIT Lab/TRUST/Sentiment_Analysis/reproduce/pitt_lexicon_reproduce.txt'

HIGHHIGH = ('User_HighHigh_Intro_May13_S', 6)
HIGHLOW = ('User_HighLow_Intro_May13_S', 6)
LOWHIGH = ('User_LowHigh_Intro_S', 5)
LOWLOW = ('User_LowLow_Intro_New_S', 7)
p_list = [HIGHHIGH, HIGHLOW, LOWHIGH, LOWLOW]

MANNUAL_LABELED_TEXT = 'mannual_labeling.txt'

PITCH_SUFFIX = '_pitch'
PITCH_SUFFIX_NEW = '_pitches'
INTENSITY_SUFFIX = '_int'
INTENSITY_SUFFIX_NEW = '_intensities'
TEXT_SUFFIX = '.txt'
WAVE_SUFFIX = '.wav'
BML_SUFFIX = '.bml'
XML_SUFFIX = '.xml'


def label_speech_text():
    result_list = []
    personality_info = HIGHHIGH
    sent_dict = ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_info = ut.build_sentence_info(timestamps, sen, sent_dict)
        result = ut.label_the_sentence(sen_info,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX)
        result_list.append(result)
    for r in result_list:
        print r
    return result_list


def label_speech_text_new():
    result_list = []
    personality_info = HIGHHIGH
    sent_dict = ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_info = ut.build_sentence_info(timestamps, sen, sent_dict)
        result = ut.label_the_sentence(sen_info,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX_NEW,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX_NEW)
        result_list.append(result)
    for r in result_list:
        print r
    return result_list


def label_speech_text_to_xml():
    personality_info = HIGHHIGH
    sent_dict = ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_info = ut.build_sentence_info(timestamps, sen, sent_dict)
        result_tree = ut.label_the_sentence_to_et(sen_info,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX)
        result_tree.write(personality_info[0] + str(ind) + XML_SUFFIX, "utf-8")
    return


def label_speech_text_to_xml_new():
    personality_info = HIGHHIGH
    sent_dict = ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_data = ut.build_sentence_data(personality_info[0] + str(ind), timestamps, sen, sent_dict)
        result_tree = ut.label_the_sentence_to_et(sen_data,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX_NEW,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX_NEW)
        result_tree.write(personality_info[0] + str(ind) + XML_SUFFIX, "utf-8")
    return


def generate_sentence_data():

    sent_dict = ut.build_sentiment_dict(SENTIMENT_DICT)
    s_list = []
    for p in p_list:
        for i in range(int(p[1])):
            ind = i + 1
            timestamps = ut.get_time_stamp(p[0] + str(ind) + BML_SUFFIX)
            sen = open(p[0] + str(ind) + TEXT_SUFFIX).readline()
            sen_data = ut.build_sentence_data(p[0] + str(ind), timestamps, sen, sent_dict)
            ut.fill_acoustic_data(ut.read_intensities_from_autofile(p[0] + str(ind) + INTENSITY_SUFFIX_NEW),
                                  ut.read_pitches_from_autofile(p[0] + str(ind) + PITCH_SUFFIX_NEW),
                                  sen_data)
            s_list.append(sen_data)
    return s_list


def generate_source_data(sen_list):
    data = []
    # print len(sen_list)
    for s in sen_list:
        for w in s.words:
            word_data = []
            word_data.append(s.pitch_mean)
            word_data.append(s.pitch_std)
            word_data.append(s.intensity_mean)
            word_data.append(s.intensity_std)
            word_data.append(w.pitch_mean)
            word_data.append(w.intensity_mean)
            word_data.append(w.speed)
            data.append(word_data)
    return data


def generate_source_data_processed(sen_list):
    data = []
    # print len(sen_list)
    for s in sen_list:
        for w in s.words:
            word_data = []
            # word_data.append(s.pitch_mean)
            # word_data.append(s.pitch_std)
            # word_data.append(s.intensity_mean)
            # word_data.append(s.intensity_std)
            word_data.append(w.pitch_mean / s.pitch_mean)
            word_data.append(w.intensity_mean / s.intensity_mean)
            word_data.append(w.speed)
            data.append(word_data)
    return data


def generate_target(path):
    # read mannually labeling text file
    man_text_file = open(path)
    target = []
    text = man_text_file.readlines()
    for s in text:
        # words = re.split('[,.!?\r\n ]+', s)
        words = s.split()
        for w in words:
            if '[E]' in w:
                target.append(1)
            else:
                target.append(0)
    return target


def generate_learning_data():
    l_data = LearningData(generate_source_data(generate_sentence_data()),
                          generate_target(MANNUAL_LABELED_TEXT))
    # l_data = LearningData(generate_source_data_processed(generate_sentence_data()),
    #                       generate_target(MANNUAL_LABELED_TEXT))
    return l_data



# if __name__ == '__main__':
#     # label_speech_text_new()
#     # label_speech_text_to_xml_new()
#     print generate_target(MANNUAL_LABELED_TEXT)