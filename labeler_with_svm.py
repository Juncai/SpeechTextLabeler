__author__ = 'juncai'

import labeler as lr
from sklearn import svm
from sklearn.externals import joblib
import utilities as ut
from data_classes import LearningData

MODEL_FILE = 'original_model.pkl'
XML_SUFFIX = '.xml'
RESULT_ONLY_PITCH = 'result_only_pitch.txt'
MANNUAL_LABELED_TEXT = 'mannual_labeling.txt'


def label_with_svm(if_balanced):
    l_data = lr.generate_learning_data()
    if if_balanced:
        l_data = ut.create_balanced_training_data(l_data, 1, 0)
    # for test
    # print len(l_data.target)
    # count0 = 0
    # count1 = 0
    # for t in l_data.target:
    #     if t == 1:
    #         count1 += 1
    #     else:
    #         count0 += 1
    # print count0, count1

    # clf = svm.SVC(gamma=0.001, C=100.)
    clf = svm.SVC()
    if len(l_data.data) == len(l_data.target):
        # clf.fit(l_data.data[0:-100], l_data.target[0:-100])
        clf.fit(l_data.data, l_data.target)
        joblib.dump(clf, MODEL_FILE)
        # print compute_correctness(clf, l_data)
        # print clf.predict(l_data.data[-1])
        # print clf.predict(l_data.data[0])
        # print clf.predict(l_data.data[5])
    else:
        print 'length error'
        print len(l_data.data)
        print len(l_data.target)


def output_training_data():
    l_data = lr.generate_learning_data()
    o_file = open('training_data.txt', 'w+')
    for d in l_data.data:
        o_file.write('%s\n' % d)
    o_file.close()


def compute_correctness(model_path, l_data):
    # p_result = clf.predict(l_data.data[239:])
    clf = joblib.load(model_path)
    p_result = clf.predict(l_data.data)
    correct_count = 0
    print p_result[0]
    for i, r in enumerate(p_result):
        # if r == l_data.target[i + 239]:
        if r == l_data.target[i]:
            correct_count += 1
    correctness = float(correct_count) / len(p_result)
    print correctness
    return correctness


def generate_results(model_path):
    l_data = lr.generate_learning_data()
    clf = joblib.load(model_path)
    p_result = clf.predict(l_data.data)
    # print p_result
    s_list = lr.generate_sentence_data()
    result_ind = 0
    for s in s_list:
        for w in s.words:
            w.is_emphasis = (p_result[result_ind] == 1)
            result_ind += 1
        # ut.build_xml_tree(s).write(s.title + XML_SUFFIX, 'utf-8')
    generate_results_to_text(s_list)
    return 0


def compare_results(s_result, t_result):
    if len(s_result) != len(t_result):
        return -1
    correct_count = 0.0
    for i in range(0, len(s_result)):
        if s_result[i] == t_result[i]:
            correct_count += 1
    return correct_count / len(s_result)


def generate_results_to_text(s_list):
    output_text_file = open('label_result_text.txt', 'w+')
    for s in s_list:
        for w in s.words:
            output_text_file.write(w.text)
            if w.is_emphasis:
                output_text_file.write('[e]')
            output_text_file.write(' ')
        output_text_file.write('\n')
    output_text_file.close()
    return 0


def output_xml_for_experts():
    s_list = lr.generate_sentence_data()
    output_xml_for_some_sentence(s_list, 0, 5, 'User_HighHigh_Intro_May13')
    output_xml_for_some_sentence(s_list, 6, 11, 'User_HighLow_Intro_May13')
    output_xml_for_some_sentence(s_list, 12, 16, 'User_LowHigh_Intro')
    output_xml_for_some_sentence(s_list, 17, 23, 'User_LowLow_Intro_New')

def output_xml_for_some_sentence(s_list, start, end, title):
    ele_list = []
    for i in range(start, end+1):
        ele_list.append(ut.build_xml_element_for_sentence(s_list[i]))
    ut.build_xml_tree(ele_list).write(title + XML_SUFFIX, 'utf-8')


if __name__ == '__main__':
    # label_speech_text_new()
    # label_speech_text_to_xml_new()
    label_with_svm(True)
    compute_correctness(MODEL_FILE, lr.generate_learning_data())
    # output_traning_data()
    generate_results(MODEL_FILE)

    # # compare pitch only
    # s_list = lr.generate_target(RESULT_ONLY_PITCH)
    # t_list = lr.generate_target(MANNUAL_LABELED_TEXT)
    # print compare_results(s_list, t_list)

    # XML for experts
    # output_xml_for_experts()
