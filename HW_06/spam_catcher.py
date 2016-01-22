#! python3
# -*- coding: utf-8 -*-

import io, re
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer

############################
## A. Regular Expressions ##
############################

r_phone_number = re.compile(r'\s*(?:\+?\d{1,3})?(?:[- (]*\d{3}[- )]*)?\d{3}[- ]*\d{2,4}(?:[-x ]*\d+)?\s*')
r_url = re.compile(r'(?:\b[a-z\d.-]+://[^<>\s]+|\b(?:(?:(?:[^\s!@#$%^&*()_=+[\]{}\|;:\'",.<>/?]+)\.)+(?:ac|ad|aero|ae|af|ag|ai|al|am|an|ao|aq|arpa|ar|asia|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|biz|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|cat|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|coop|com|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|edu|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gov|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|info|int|in|io|iq|ir|is|it|je|jm|jobs|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mil|mk|ml|mm|mn|mobi|mo|mp|mq|mr|ms|mt|museum|mu|mv|mw|mx|my|mz|name|na|nc|net|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|org|pa|pe|pf|pg|ph|pk|pl|pm|pn|pro|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tel|tf|tg|th|tj|tk|tl|tm|tn|to|tp|travel|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--80akhbyknj4f|xn--9t4b11yi5a|xn--deba0ad|xn--g6w251d|xn--hgbk6aj7f53bba|xn--hlcj6aya9esc7a|xn--jxalpdlp|xn--kgbechtv|xn--zckzah|ye|yt|yu|za|zm|zw)|(?:(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))(?:[;/][^#?<>\s]*)?(?:\?[^#<>\s]*)?(?:#[^<>\s]*)?(?!\w))')

def preprocess(string):
    string = r_phone_number.sub("PHONENO", string)
    string = r_url.sub("URL", string)
    return string

#########################
## B. Filter Stopwords ##
#########################

# Load stopwords
f_stopwords = open('stopwords.txt','r')
stopwords = f_stopwords.read().replace('"','').split(',')
stopwords.extend(list('.,?!1234567890')+['...','..'])

# Define the function
def filter_stopwords(string):
    tokens = TweetTokenizer().tokenize(string.lower())
    return [tok for tok in tokens if tok not in stopwords]

#################
## D. Stemming ##
#################

def do_stemming(tokens):
    return [PorterStemmer().stem(tok) for tok in tokens]

#################
## E. Training ##
#################

# initialize classifiers
ham_num = 0
spam_num = 0
vocab_count = dict()

def train(strings, labels):
    global ham_num, spam_num, vocab_count
    # iterate train dataset
    for string, label in zip(strings, labels):
        ham_num += 1 if label=='ham' else 0
        spam_num += 1 if label=='spam' else 0
        words = list(set(do_stemming(filter_stopwords(preprocess(string)))))
        for word in words:
            idx = 0 if label=='ham' else 1
            if word in vocab_count:
                vocab_count[word][idx] += 1
            else:
                vocab_count[word] = [0,0]
                vocab_count[word][idx] += 1

#######################
## F. Classification ##
#######################

def classify(string):
    global ham_num, spam_num, vocab_count
    words = list(set(do_stemming(filter_stopwords(preprocess(string)))))
    ratio = spam_num / ham_num
    for word in words:
        if word in vocab_count:
            if 0 in vocab_count[word]: continue
            ratio *= (vocab_count[word][1] / spam_num) \
                    / (vocab_count[word][0] / ham_num)
    return 'spam' if ratio > 1 else 'ham'

##########
## Test ##
##########

# load train file
f_train = open('train', 'rU')
train_data = [tuple(line.strip().split('|',1)) for line in f_train]
train_labels = [pair[0].strip() for pair in train_data]
train_strings  = [pair[1].strip() for pair in train_data]

# train classifier using train dataset
train(train_strings, train_labels)
vocabulary = list(vocab_count.keys())
vocabulary.sort(key=lambda x: sum(vocab_count[x]), reverse=True)
print(vocabulary[:10])

# limit size of vocabulary
if len(vocab_count) > 10000:
    ham_cnt_sum = 0; spam_cnt_sum = 0;
    vocabulary = list(vocab_count.keys())
    vocabulary.sort(key=lambda x: sum(vocab_count[x]), reverse=True)
    for vocab in vocabulary[10000:]:
        val = vocab_count.pop(vocab)
        ham_cnt_sum += val[0]
        spam_cnt_sum += val[1]
    vocab_count['unknown'] = [ham_cnt_sum, spam_cnt_sum]

# load test file
f_test = open('test', 'rU')
test_data = [tuple(line.strip().split('|',1)) for line in f_test]
test_labels = [pair[0].strip() for pair in test_data]
test_strings  = [pair[1].strip() for pair in test_data]

tp = 0; fp = 0;
fn = 0; tn = 0;
for string, label in zip(test_strings, test_labels):
    result = classify(string)
    if label == 'spam':
        if label == result:
            tp += 1
        else:
            tn += 1
    else:
        if label == result:
            fn += 1
        else:
            fp += 1

# caculate precision and recall
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1score = 2 * tp / (2 * tp + fp + fn)

# print result
print("tp: %d, fp: %d, fn: %d, tn: %d" % (tp,fp,fn,tn))
print("precision: ", precision)
print("recall: ", recall)
print("f1score: ", f1score)
