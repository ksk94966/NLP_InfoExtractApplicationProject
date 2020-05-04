import nltk
import codecs
import os
import spacy
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")
from nltk.tokenize import word_tokenize, sent_tokenize 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
wordnet_lemmatizer = WordNetLemmatizer()


#word tokenization from the sentences
def sent_wordtokenization(s):
    tok_words = nltk.word_tokenize(s)
    print('----Word Tokenization-----')
    print(tok_words)


#word lemmatization
def sent_wordlemmatization(s):
    tok_words = nltk.word_tokenize(s)
    tempSent_lemmas = []
    for w in tok_words:
        tempSent_lemmas.append(wordnet_lemmatizer.lemmatize(w))
    print('----Word Lemmatization-----')
    print(tempSent_lemmas)

#pos tagging the words with respect to each sentence
def sent_postagging(s):
    pos_tok_templist = word_tokenize(s)
    word_postag = nltk.pos_tag(pos_tok_templist)
    print('----POS tagging the words-----')  
    print(word_postag)             
        
def sent_wordnetFeatures(s):
    wordslist = word_tokenize(s)
    hypernyms_dict = dict()
    hyponyms_dict = dict()
    meronyms_dict = dict()
    holonyms_dict = dict()
    for w in wordslist:
        temp_hyperlist = []
        temp_hypolist = []
        temp_merolist = []
        temp_hololist = []
        extracted_syns_list = wn.synsets(w)
        if(len(extracted_syns_list)!=0):
            for each_syn in extracted_syns_list:
                for e in each_syn.hypernyms():
                    for l in e.lemmas():
                        temp_hyperlist.append(l.name())
                for e in each_syn.hyponyms():
                    for l in e.lemmas():
                        temp_hypolist.append(l.name())
                for e in each_syn.part_meronyms():
                    for l in e.lemmas():
                        temp_merolist.append(l.name())
                for e in each_syn.part_holonyms():
                    for l in e.lemmas():
                        temp_hololist.append(l.name())
        hypernyms_dict[w] = temp_hyperlist
        hyponyms_dict[w] = temp_hypolist
        meronyms_dict[w] = temp_merolist
        holonyms_dict[w] = temp_hololist
    print("Extracted Wordnet Features of the sentence provided")
    print("----------Hypernyms-----------")
    print(hypernyms_dict)
    print("----------Hyponyms-----------")
    print(hypernyms_dict)
    print("----------Meronyms-----------")
    print(hypernyms_dict)
    print("----------Holonyms-----------")
    print(hypernyms_dict)

def sent_parsing(s):
    print("Dependency Parsing")
    print('\n')
    parse_sent = nlp(s)
    for tok in parse_sent:
        print(tok.text,"----->",tok.dep_,"----->",tok.pos_,)



if __name__ == '__main__':
	#print("Enter your input sentence:")
    content = None
    try:
        f = open("WikipediaArticles/sample.txt", "r")
        content = f.read()
    except UnicodeDecodeError:
        f = open("WikipediaArticles/sample.txt", "r", encoding = 'utf8')


    #Extacting the sentences from the text document
    # sent = []
    # tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # sent.extend(tokenizer.tokenize(content))      #sent[0] contains all the sentences

    sent = nltk.sent_tokenize(content)

    print('Total Sentences After splitting the document: ',len(sent))
    
    print('\n----------\n')

    print('Extracting features for each of the sentence and shown below:')

    print('\n')
    for s in sent:
        print(s)
        print('\n----------\n')
        sent_wordtokenization(s)
        print('\n')
        sent_wordlemmatization(s)
        print('\n')
        sent_postagging(s)
        print('\n')
        sent_wordnetFeatures(s)
        print('\n')
        sent_parsing(s)
        print('\n----------\n')
        print('\n--Extracting for next sentence--\n')
