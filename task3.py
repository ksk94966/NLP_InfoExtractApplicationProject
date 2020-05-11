# import task2
import nltk
import spacy
import neuralcoref
import pandas as pd
import json
from spacy_lookup import Entity
from nltk.tokenize import word_tokenize, sent_tokenize
from task2part import parse_part_template
from task2buy import parse_buy_template
from task2work import parse_work_template

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def main():
    #change input file name here
    file ="input.txt"
    outputfile = file[1:-4]+".json"

    content=None
    try:
        f = open(file, "r")
        content =f.read()
    except UnicodeDecodeError:
        f = open(file, "r", encoding='utf8')
        content =f.read()

    
    # Create a dataframe from csv
    df = pd.read_csv('./titles.csv')
    
    # User list comprehension to create a list of lists from Dataframe rows
    job_titles = [row[0] for row in df.values]

   
    # nlp.remove_pipe('entity')
    entity = Entity(keywords_list=job_titles, label='Job-Title')
   

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(entity , before='ner')
    neuralcoref.add_to_pipe(nlp)
    doc = nlp(content)

    #coreference resolution is done in the whole document
    content = doc._.coref_resolved

    #Extacting the sentences from the text document
    sentences = []
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences.extend(tokenizer.tokenize(content))

    output = {}
    output["document"] =file
    output["extraction"] = []
    for sentence in sentences:
        sen= nlp(sentence)

        #Find part  template
        locations_count = 0
        for ents in sen.ents:
            if ents.label_ =='GPE' or ents.label_ =='LOC':
                locations_count = locations_count + 1
        if locations_count >=2:
            resultset=parse_part_template(sen)
            for x in resultset:
                if x[0]!='' and x[1]!='':
                    part_temp={}
                    part_temp["template"] = "PART"
                    part_temp["sentences"] = []
                    part_temp["sentences"].append(sentence)
                    part_temp["arguments"] = {}
                    part_temp["arguments"]["1"] = x[0]
                    part_temp["arguments"]["2"] = x[1]
                    output["extraction"].append(part_temp)

        #Find work template
        isJobTitleGiven = False
        isOrgGiven = False
        for ents in sen.ents:
            
            if ents.label_ == 'Job-Title' :
                isJobTitleGiven = True
            if ents.label_ == 'ORG':
                isOrgGiven = True
        if isOrgGiven and isJobTitleGiven:
            results=parse_work_template(sen)
            for res in results:
                if res[0] != '' and res[1]!= '' and res[2]!= '':
                    work_temp={}
                    work_temp["template"] = "WORK"
                    work_temp["sentences"] = []
                    work_temp["sentences"].append(sentence)
                    work_temp["arguments"] = {}
                    work_temp["arguments"]["1"] = res[0]
                    work_temp["arguments"]["2"] = res[2]
                    work_temp["arguments"]["3"] = res[1]
                    work_temp["arguments"]["4"] = res[3]
                    output["extraction"].append(work_temp)

        #Find buy template
        for i, tok in enumerate(sen):
            if tok.dep_ == 'ROOT' or tok.pos_ == 'VERB':
                if tok.text.lower() in ['buy', 'bought','shop', 'acquire', 'acquired', 'purchase', 'invest in'\
                    'invested', 'get', 'obtain', 'obtained', 'secure', 'redeem', 'land', 'spent', 'get']:
                    results= parse_buy_template(sen)
                    if results[0]!= '' and results[1]!='':
                        buy_temp={}
                        buy_temp["template"] = "BUY"
                        buy_temp["sentences"] = []
                        buy_temp["sentences"].append(sentence)
                        buy_temp["arguments"] = {}
                        buy_temp["arguments"]["1"] = results[0]
                        buy_temp["arguments"]["2"] = results[1]
                        buy_temp["arguments"]["3"] = results[2]
                        buy_temp["arguments"]["4"] = results[3]
                        buy_temp["arguments"]["5"] = results[4]
                        output["extraction"].append(buy_temp)

    # Serializing json  
    json_object = json.dumps(output, indent = 4) 
    # Writing to sample.json 
    with open(outputfile, 'w+') as f:
        f.write(json_object)


if __name__ == "__main__":
    main()






