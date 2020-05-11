from stanfordcorenlp import StanfordCoreNLP
import logging
import json

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word': token['word'],
                'lemma': token['lemma'],
                'pos': token['pos'],
                'ner': token['ner']
            }
        return tokens

if __name__ == '__main__':
    sNLP = StanfordNLP()
    import nltk
    import codecs
    from nltk.tokenize import word_tokenize, sent_tokenize 
    import glob
    title_list=[]
    state_list=[]
    location_list=[]
    city_list=[]
    for file in glob.glob("WikipediaArticles/*.txt"):
        
        try:
            f = open(file, "r")
            content =f.read()
        except UnicodeDecodeError:
            f = open(file, "r", encoding='utf8')
            content =f.read()
        
        print(type(content))
        # doc = codecs.open("WikipediaArticles/AbrahamLincoln.txt", 'r', 'utf-8')
        # content = doc.read()

        sent = []
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sent.extend(tokenizer.tokenize(content))
        
        # text = 'A blog post using Stanford CoreNLP Server. Visit www.khalidalnajjar.com for more details.'
        for sentences in sent:
            for tok in sNLP.ner(sentences):
                
                templist=list(x.encode('utf-8') for x in list(tok))
                if templist[1].decode('utf-8')=='TITLE':
                    title_list.append(templist[0].decode('utf-8'))
                if templist[1].decode('utf-8')=='STATE_OR_PROVINCE':
                    state_list.append(templist[0].decode('utf-8'))
                if templist[1].decode('utf-8')=='LOCATION':
                    location_list.append(templist[0].decode('utf-8'))
                if templist[1].decode('utf-8')=='CITY':
                    city_list.append(templist[0].decode('utf-8'))
    print(title_list)
    import pandas
    df = pandas.DataFrame(data={"Title": list(set(title_list))})
    df.to_csv("./titles.csv",mode='a',header=False, sep=',',index=False)

    df = pandas.DataFrame(data={"city": list(set(city_list))})
    df.to_csv("./cities.csv",mode='a',header=False, sep=',',index=False)

    df = pandas.DataFrame(data={"location": list(set(location_list))})
    df.to_csv("./locations.csv",mode='a',header=False, sep=',',index=False)

    df = pandas.DataFrame(data={"state": list(set(state_list))})
    df.to_csv("./states.csv",mode='a',header=False, sep=',',index=False)
       
    