__author__ = 'juncai'


class SentenceData(object):
    '''
    Sentence data model for storing acoustic and labeling data for each word in a sentence.
    '''

    title = ''
    text = ''
    words = []
    num_of_words = 0
    duration = 0
    intensity_mean = 0
    intensity_std = 0
    intensity_ts = []
    intensity_list = []
    pitch_mean = 0
    pitch_std = 0
    pitch_ts = []
    pitch_list = []
    acoustic_data_filled = False
    labeled = False


    def __init__(self, title, text):
        self.title = title
        self.text = text





class WordData(object):
    '''

    '''

    text = ''
    start_time = 0
    end_time = 0
    sentiment = 0
    num_syllables = 0
    speed = 0
    punct_after = ''
    special = ''
    pitch_list = []
    pitch_mean = 0
    intensity_list = []
    intensity_mean = 0
    acoustic_data_filled = False
    behavior_type = ''
    behavior_intensity = 0
    is_emphasis = False

    def __init__(self, text, start, end, sentiment, syllables, punct, special):
        self.pitch_list = []
        self.intensity_list = []
        self.text = text
        self.start_time = start
        self.end_time = end
        self.sentiment = sentiment
        self.num_syllables = syllables
        self.punct_after = punct
        self.special = special
        if syllables > 0:
            self.speed = syllables / (end - start)


class LearningData(object):
    target = []
    data = []

    def __init__(self, data, target):
        self.target = target
        self.data = data
