from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
import numpy as np

from keras.preprocessing.text import Tokenizer as KerasTokenizer
from collections import Counter

import unicodedata

import string
import re
import html

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer


# See https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
class Utils:

    def __init__(self):
        """

        :param library: keras, nltk, spacy
        :type library:
        """
        pass

    @staticmethod
    def text2words(text, method='nltk'):
        """
        Abstraction of text to sequence
        :param text: string
        :type text: basestring
        :param method: tools to use to transfrom string to seqeuence: keras or string (split)
        :return:
        :rtype:
        """
        if method== 'string':
            return text.split()
        elif method== 'keras':
            return text_to_word_sequence(text)
        elif method == 'nltk':
            return word_tokenize(text)

    @staticmethod
    def doc2sent(text):
        return sent_tokenize(text)

    @classmethod
    def calc_max_len_from_text(cls, texts):
        """
        This is different from TextFeatures method, as this one just uses split without tokenization
        :param texts: list of strings
        :type texts: list

        :return: maxlen
        :rtype: int
        """
        return max([len(cls.text2words(text)) for text in texts])

    @staticmethod
    def calc_max_len_from_ids(sequences):
        """
        Same as calc_max_len_from_text, but the input is list of tokens ids (not strings)
        :param texts: list of lists (sequence of tokens ids)
        :type texts: list
        :return: maxlen
        :rtype: int
        """
        return max([len(seq) for seq in sequences])

    @staticmethod
    def remove_special_chars(text):
        re1 = re.compile(r'  +')
        x1 = text.lower().replace('#39;', "'").replace('amp;', '&').replace('#146;', "'").replace(
            'nbsp;', ' ').replace('#36;', '$').replace('\\n', "\n").replace('quot;', "'").replace(
            '<br />', "\n").replace('\\"', '"').replace('<unk>', 'u_n').replace(' @.@ ', '.').replace(
            ' @-@ ', '-').replace('\\', ' \\ ')
        return re1.sub(' ', html.unescape(x1))

    @staticmethod
    def remove_non_ascii(cls, text):
        """Remove non-ASCII characters from list of tokenized words"""
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    @staticmethod
    def to_lowercase(text):
        return text.lower()


    @staticmethod
    def remove_punctuation(text):
        """Remove punctuation from list of tokenized words"""
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    @staticmethod
    def replace_numbers(text):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        return re.sub(r'\d+', '', text)

        '''
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words
        '''

    @staticmethod
    def remove_whitespaces(cls, text):
        return text.strip()

    @staticmethod
    def remove_stopwords(words, stop_words):
        """

        :param words:
        :type words:
        :param stop_words: from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
        or
        from spacy.lang.en.stop_words import STOP_WORDS
        :type stop_words:
        :return:
        :rtype:
        """
        return [word for word in words if word not in stop_words]

    @staticmethod
    def stem_words(words):
        """Stem words in text"""
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in words]

    @staticmethod
    def lemmatize_words(words):
        """Lemmatize words in text"""

        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in words]

    @staticmethod
    def lemmatize_verbs(words):
        """Lemmatize verbs in text"""

        lemmatizer = WordNetLemmatizer()
        return ' '.join([lemmatizer.lemmatize(word, pos='v') for word in words])

    @staticmethod
    @classmethod
    def normalize_text(cls, text):
        text = cls.remove_special_chars(text)
        text = cls.remove_non_ascii(text)
        text = cls.remove_punctuation(text)
        text = cls.to_lowercase(text)
        text = cls.replace_numbers(text)
        words = cls.text2words(text)
        words = cls.remove_stopwords(words)
        words = cls.stem_words(words)
        words = cls.lemmatize_words(words)
        words = cls.lemmatize_verbs(words)

        return ' '.join(words)


    @staticmethod
    @classmethod
    def normalize_corpus(cls, texts):
        s = [cls.normalize_text(text) for text in texts]


    @staticmethod
    def pad(texts, maxlen, method='keras'):
        """
        Append 0's to the end
        :param texts: list of lists (sequence of tokens)
        :type texts: list
        :param maxlen: max length of text in texts
        :type maxlen: int
        :param method: keras
        :return: padded sequence as numpy array
        :rtype: np.array
        """
        if method== 'keras':
            return np.array(pad_sequences(texts,
                                          maxlen=maxlen,
                                          padding='post',
                                          truncating='post'))


    @staticmethod
    def load_embeddings(embeddings_file, str2int, vocab_size, embedding_dim):
        embeddings_index = {}
        f = open(embeddings_file)
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

        f.close()


        embedding_matrix = np.random.random((vocab_size+1, embedding_dim))

        for word, i in str2int.items():
          embedding_vector = embeddings_index.get(word)
          if embedding_vector is not None:
              # words not found in embedding index will be random.
              embedding_matrix[i] = embedding_vector
        return embedding_matrix

'''
class Normalizer:
    def __init__(self, method='nltk'):
'''

class Tokenizer:
    def __init__(self, texts=None, method='keras', vocab_size=None, oov_token=None):
        self.library = method
        if method == 'keras':
            if vocab_size != None:
                self.tokenizer = KerasTokenizer(nb_words=vocab_size, oov_token=oov_token)
            else:
                self.tokenizer = KerasTokenizer(oov_token=oov_token)
            if texts != None:
                self.fit(texts)

    def fit(self, texts):
        if self.library == 'keras':
            self.tokenizer.fit_on_texts()


class Vocabulary:
    UNK_ID = 0  # 0 index is reserved for the UNK in both Keras Tokenizer and Embedding

    def __init__(self, texts=None, pre_vocab=None, method='string', vocab_size=None, oov_token=None, stop_words=None):
        self.library = method
        self.stop_words = stop_words

        if pre_vocab != None:
            self.str2idx = pre_vocab

        elif texts != None:
            self.build_vocab(texts, vocab_size, oov_token)


    def build_vocab(self, texts, vocab_size=None, oov_token='_UNK_'):

        if self.library == 'string':
            words = [word for text in texts for word in Utils.text2words(text, method=self.library)]
            word_counts = Counter(words)

            # Sort by most frequent. Not that .items() is a tuple, and counts is at index [1] of that tuple
            word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

            # Take most frequent as per vocab_size
            self.vocab_dict = {key:val for key, val in word_counts[:vocab_size]}

            # Insert UNK
            self.vocab_dict[oov_token] = Vocabulary.UNK_ID


    def update_inv_vocab(self):
        self.inv_vocab_dict = dict([(value, key) for (key, value) in self.vocab_dict.items()])

    @property
    def idx2str(self):
        return self.inv_vocab_dict

    @property
    def str2idx(self):
        return self.vocab_dict

    @str2idx.setter
    def str2idx(self, value):
        self.vocab_dict = value
        self.update_inv_vocab()


class TextFeatures:
    # Note that: it's highly recommended to use 'keras', since the tokenizer does few important things
    # 1. Splits the sentence words based on punctuations, not only spaces
    # 2. Can consider stop words
    # 3. Filters non important tokens when building vocab
    # 4. Considers lower in vocab and extraction
    def __init__(self, texts, vocab_size=None, method='keras', oov_token=None, stop_words=None):
        # TODO: stop words not in keras. Use spacy.
        self.library = method
        pre_vocab = None

        texts = Utils.normalize_corpus(texts)
        if method == 'keras':
            self.tokenizer = Tokenizer(texts, vocab_size, oov_token).tokenizer
            pre_vocab = self.tokenizer.word_index
        elif method == 'string':
            self.tokenizer = None
            pre_vocab = None
        # TODO: elif method == 'nltk':



        self.vocab = Vocabulary(texts=texts, pre_vocab=pre_vocab, method=method, vocab_size=vocab_size)

        self.maxlen = Utils.calc_max_len_from_text(texts)

    def text2features(self, texts, pad=True):
        raise NotImplementedError("extract to be implemented according to the exact representation method")

    def features2text(self, features):
        if self.library == 'keras':
            return self.tokenizer.sequences_to_texts(features)
        elif self.library == 'string':
            return [' '.join([self.vocab.idx2str[idx] for idx in vec]) for vec in features]



class SequenceFeatures(TextFeatures):
    def __init__(self, texts):
        super().__init__(texts=texts)

    def text2features(self, texts, pad=True):
        if self.library == 'keras':
            features = self.tokenizer.texts_to_sequences(texts)

        elif self.library == 'string':
            features = [[self.vocab.str2idx[word] for word in Utils.text2words(text)] for text in texts]
        else:
            raise Exception("No supported method set")

        if pad:
            return Utils.pad(features, self.maxlen, self.library)
        else:
            return features

class BoWFeatures(TextFeatures):
    def __init__(self, texts):
        super().__init__(texts=texts)

    def text2features(self, texts):
        pass


class CountFeatures(TextFeatures):
    def __init__(self, texts):
        super().__init__(texts=texts)

    def text2features(self, texts, pad=True):

        pass


class TFIDFFeatures(TextFeatures):
    def __init__(self, texts):
        super().__init__(texts=texts)

    def text2features(self, texts, pad=True):
        pass

