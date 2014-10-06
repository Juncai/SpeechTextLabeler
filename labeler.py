__author__ = 'juncai'


import Utilities as Ut

SENTIMENT_DICT = '/Users/juncai/Dropbox/PlaIT Lab/TRUST/Sentiment_Analysis/reproduce/pitt_lexicon_reproduce.txt'

HIGHHIGH = ('User_HighHigh_Intro_May13_S', 6)
HIGHLOW = ('User_HighLow_Intro_May13_S', 6)
LOWHIGH = ('User_LowHigh_Intro_S', 5)
LOWLOW = ('User_LowLow_Intro_New_S', 7)

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
    sent_dict = Ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = Ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_info = Ut.build_sentence_info(timestamps, sen, sent_dict)
        result = Ut.label_the_sentence(sen_info,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX)
        result_list.append(result)
    for r in result_list:
        print r
    return result_list

def label_speech_text_new():
    result_list = []
    personality_info = HIGHHIGH
    sent_dict = Ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = Ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_info = Ut.build_sentence_info(timestamps, sen, sent_dict)
        result = Ut.label_the_sentence(sen_info,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX_NEW,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX_NEW)
        result_list.append(result)
    for r in result_list:
        print r
    return result_list

def label_speech_text_to_xml():
    personality_info = HIGHHIGH
    sent_dict = Ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = Ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_info = Ut.build_sentence_info(timestamps, sen, sent_dict)
        result_tree = Ut.label_the_sentence_to_et(sen_info,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX)
        result_tree.write(personality_info[0] + str(ind) + XML_SUFFIX, "utf-8")
    return


def label_speech_text_to_xml_new():
    personality_info = HIGHHIGH
    sent_dict = Ut.build_sentiment_dict(SENTIMENT_DICT)
    for i in range(int(personality_info[1])):
        ind = i + 1
        timestamps = Ut.get_time_stamp(personality_info[0] + str(ind) + BML_SUFFIX)
        sen = open(personality_info[0] + str(ind) + TEXT_SUFFIX).readline()
        sen_info = Ut.build_sentence_info(timestamps, sen, sent_dict)
        result_tree = Ut.label_the_sentence_to_et(sen_info,
                                      personality_info[0] + str(ind) + INTENSITY_SUFFIX_NEW,
                                      personality_info[0] + str(ind) + PITCH_SUFFIX_NEW)
        result_tree.write(personality_info[0] + str(ind) + XML_SUFFIX, "utf-8")
    return

if __name__ == '__main__':
    label_speech_text_new()
    # label_speech_text_to_xml_new()