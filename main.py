import nltk
import codecs
import os
from nltk.tokenize import word_tokenize, sent_tokenize 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
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

#lemmatizing the words

word_lemm = dict()
word_lemma_list = []
#print("{0:20}{1:20}".format("Word","Lemma"))
for word in sent_wordsAll:
    word_lemm[word] = wordnet_lemmatizer.lemmatize(word)
    #word_lemma_list.extend(wordnet_lemmatizer.lemmatize(word))
    #print(word,word_lemm[word])
    #print ("{0:20}{1:20}".format(word,wordnet_lemmatizer.lemmatize(word)))

print('lemmacount : ',len(word_lemm))

#print(len(word_lemma_list))

#pos tagging the words with respect to each sentence
word_tag = dict()    
for s in sent:
    tokenized = sent_tokenize(s)              #Transforming the sentence into one array with quotations
    for i in tokenized: 
        wordsList = nltk.word_tokenize(i)  
        word_tag[s] = nltk.pos_tag(wordsList)  

print(len(word_tag))

#print(word_tag)

hypernyms_dict = dict()
hyponyms_dict = dict()
meronyms_dict = dict()
holonyms_dict = dict()
for word in sent_wordsAll:
    extracted_syns = wn.synsets(word)
    #print(extracted_syns)
    if(len(extracted_syns)!=0):
        hypernyms_dict[word] = extracted_syns[0].hypernyms()
        hyponyms_dict[word] = extracted_syns[0].hyponyms()
        meronyms_dict[word]  = extracted_syns[0].part_meronyms()
        holonyms_dict[word]  = extracted_syns[0].part_holonyms()

print(len(hypernyms_dict))
print(len(hyponyms_dict))
print(len(meronyms_dict))
print(len(holonyms_dict))













