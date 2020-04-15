import nltk
import codecs
import os
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

doc = codecs.open("WikipediaArticles/AbrahamLincoln.txt", 'r', 'utf-8')
content = doc.read()


#Extacting the sentences from the text document
sent = []
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sent.extend(tokenizer.tokenize(content))      #sent[0] contains all the sentences

print('Total Sentences : ',len(sent))

#word tokenization from the sentences
sent_wordsAll = []
k = 0
for i in sent:
    sent_wordsAll.extend(nltk.word_tokenize(i))

print('Total Words : ',len(sent_wordsAll))

# punctuations="?:!.,;)("

# for word in sent_wordsAll[0]:
#     if word in punctuations:
#         sent_wordsAll[0].remove(word)

# print(len(sent_wordsAll))

word_lemm = dict()
#print("{0:20}{1:20}".format("Word","Lemma"))
for word in sent_wordsAll:
    word_lemm[word] = wordnet_lemmatizer.lemmatize(word)
    #print ("{0:20}{1:20}".format(word,wordnet_lemmatizer.lemmatize(word)))

print('lemmacount : ',len(word_lemm))







