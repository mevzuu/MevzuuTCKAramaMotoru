import re
from spacy.lang.tr.stop_words import STOP_WORDS
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

lcase_table = tuple(u'abcçdefgğhıijklmnoöprsştuüvyz')
ucase_table = tuple(u'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ')


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += " " + ele

    return str1


def clean_tex(example_sent):
    if len(example_sent) > 0:
        with open('../TextCleanFiles/TRStopWords.txt', 'r', encoding="utf8") as st:
            st_content = st.read()
            st_list = st_content.split()
            double_letter_r = re.sub(r'(.)\1{2,}', r'\1', example_sent)
            underscore_r = re.sub(r'(?:{})|([^\w\s.]+|_+)', '  ', double_letter_r)
            text_nonum = re.sub(r'\d+', '  ', underscore_r)
            text_nopunct = re.sub(r'[^\w\s]', '  ', text_nonum)
            text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()

            word_tokens = word_tokenize(text_no_doublespace)

            stop_words = list(get_stop_words('tr'))
            nltk_words = list(stopwords.words('turkish'))
            nltk_words.extend(st_list)
            stop_words.extend(nltk_words)
            STOP_WORDS.update(stop_words)
            lower_case = [lower_tr(l) for l in word_tokens]

            output = [w for w in lower_case if not w in STOP_WORDS]
            cleaned_stc = listToString(output)
            return cleaned_stc
    else:
        return example_sent


def lower_tr(data):
    data = data.replace(u'İ', u'i')
    data = data.replace(u'I', u'ı')
    result = ''
    for char in data:
        try:
            char_index = ucase_table.index(char)
            lcase_char = lcase_table[char_index]
        except:
            lcase_char = char
        result += lcase_char
    return result
