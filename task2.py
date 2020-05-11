
# Part(Location, Location)
def parse_part_template(doc):
    print("part template")
    gpe = []
    # iterate through all the tokens in the input sentence 
    for ent in doc.ents: 
        if ent.label_ == 'LOC'or ent.label_ == 'GPE':
            gpe.append(ent.text)


    
    results = set()
    row = tuple()
    for i,tok in enumerate(doc):
        if tok.text in ['of', 'in' , 'is']:
            locations = []
            for tok1 in list(tok.subtree):
                if (tok1.ent_type_ == 'GPE' or tok1.ent_type_ == 'LOC') and tok1.dep_ !='compound':
                    loc =tok1.text
                    children= tok1.children
                    for child in children:
                      if child.dep_ == 'compound':
                        loc = child.text+' ' + loc
                    locations.append(loc)

            print(locations)
                
            for i in range(0,len(locations)-1):
                for j in range(i+1,len(locations)):
                    results.add((locations[i],locations[j]))

  
    return results

    # WORK(Person, Organization, Position, Location)
def parse_work_template(doc):
    temp_PVJO = False
    temp_JOVP = False
  
    for i,tok in enumerate(doc): 
        if tok.dep_=='nsubj':
            if tok.ent_type_ == 'PERSON':
                temp_PVJO =True
            elif tok.ent_type_ == 'Job-Title' or tok.ent_type_ == 'ORG':
                temp_JOVP =True
    print(temp_PVJO)
    compound_noun = ''     
    person= ''
    prev_per=''
    job_titles = ''
    org = ''
    place = ''
    results = []
    row = []
    # iterate through all the tokens in the input sentence 
    for i,tok in enumerate(doc): 
        if temp_PVJO:


            # extract subject 
            if (tok.dep_== "nsubj" or tok.ent_type_ =='PERSON') and tok.head.dep_ =='ROOT' : 
                
                if person =='':
                    person = compound_noun + ' ' + tok.text
                elif job_titles!='' and org !='':
                    row.append(person)
                    row.append(job_titles)
                    row.append(org)
                    row.append(place)
                    results.append(row)
                    row=[]
                    prev_per=person
                    person = ''
                    org = ''
                    job_titles = ''
                    place=''
                else:
                    person = compound_noun + ' ' + tok.text

            if tok.pos_ == 'PUNCT' and tok.text == ';':
                row.append(person)
                row.append(job_titles)
                row.append(org)
                row.append(place)
                results.append(row)
                row=[]
                prev_per=person
                person = ''
                org = ''
                job_titles = ''
                place=''
            # extract Job-title
            if tok.ent_type_ =='Job-Title':
                if person == '':
                    person = prev_per
                if job_titles == '':
                    job_titles = compound_noun + ' ' + tok.text
                else:
                    job_titles = job_titles+',' + compound_noun + ' ' + tok.text 


            # extract organisation
            if tok.ent_type_ == 'ORG':
                if org=='':
                    org = compound_noun +' '+tok.text
                elif compound_noun!='':
                    org = compound_noun + " " +tok.text
                else:
                    org = org+ " " +tok.text


            #extract place
            if tok.ent_type_ == 'GPE'  and (tok.head.ent_type_ == 'ORG' or tok.head.pos_ == 'ADP'):
                place = tok.text  
            

            if tok.dep_ == 'compound':
                compound_noun = compound_noun+ ' ' + tok.text
            else:
                compound_noun = ''

        else:

            # extract subject 
            if tok.dep_== "nsubj" and tok.ent_type_ =='Job-Title' : 
                if job_titles == '':
                    job_titles = compound_noun + ' ' + tok.text
                else:
                    job_titles = job_titles+',' + compound_noun + ' ' + tok.text 


            # extract Person
            if tok.ent_type_ =='PERSON' and tok.head.dep_ == 'ROOT':
                if person =='':
                    person = compound_noun + ' ' + tok.text
                else:
                    person = person+ ' '+tok.text
            


            # extract organisation
            if tok.ent_type_ == 'ORG':
                if org=='':
                    org = compound_noun +' '+tok.text
                else:
                    org = org +" " +tok.text

            #extract place
            if tok.ent_type_ == 'GPE'  and (tok.head.ent_type_ == 'ORG' or tok.head.pos_ == 'ADP'):
                place = tok.text   

            
            if tok.dep_ == 'compound':
                compound_noun = compound_noun+ ' ' + tok.text
            else:
                compound_noun = ''
    row.append(person)
    row.append(job_titles)
    row.append(org)
    row.append(place)
    results.append(row)

    return results

    # BUY(Buyer, Item, Price, Quantity, Source)

def parse_buy_template(doc):
    subjpass = 0

    for i,tok in enumerate(doc):
        # find dependency tag that contains the text "subjpass"    
        if tok.dep_.find("subjpass") == True and tok.head.dep_ == 'ROOT':
            subjpass = 1
    x =''
    y =''
    verb =''
    price =''
    prev_tok_price = False
    compound_noun = ''
    more_y = False
    quantity =''
    y_children=[]
    # if subjpass == 1 then sentence is passive
    if subjpass == 1:
        print('Passive')
        # iterate through all the tokens in the input sentence 
        for i,tok in enumerate(doc): 
            
            # extract subject 
            if tok.dep_== "nsubjpass" and (tok.pos_ == 'PROPN' or tok.pos_ == 'NOUN') : 
                y = compound_noun + ' '+ tok.text 
                y_children = tok.conjuncts
                child = [child for child in tok.rights if child.pos_=='NOUN']
                if len(y_children)!= 0:
                    more_y =True
                elif len(child)!=0 and child[0].dep_ == 'appos':
                    y_children = child[0].conjuncts
                    more_y = True

            if more_y and tok.dep_ == 'conj' and tok in y_children:
                y = y+ ',' + compound_noun + ' '+ tok.text
            
            # extract object 
            if tok.dep_.endswith("obj") == True and (tok.pos_ == 'PROPN' or tok.pos_ == 'NOUN') and tok.head.dep_=='agent': 
                x = compound_noun + ' ' + tok.text 

            # extract verb (BUY )
            if tok.dep_ == 'ROOT' and tok.pos_ == 'VERB' :
                verb = tok.text

            # extract price
            if tok.ent_type_ == 'MONEY' or tok.text.lower == 'us$':
                if prev_tok_price:
                    price = price+ tok.text
                else:
                    price = tok.text
                    prev_tok_price = True

            #extract quantity
            if (tok.dep_ == 'nummod' or tok.pos_ == 'NUM') and  tok.i < len(doc)-1 and tok.nbor() == tok.head and tok.ent_type_ != 'MONEY':
                if quantity == '':
                    quantity = tok.text
                else :
                    quantity = quantity + ','+tok.text

            if tok.dep_ == 'compound':
                compound_noun = compound_noun+ ' ' + tok.text
            else:
                compound_noun = ''


    else:
        print('Active')
        # iterate through all the tokens in the input sentence 
        for i,tok in enumerate(doc): 
            
            # extract subject 
            if tok.dep_ == "nsubj" and (tok.pos_ == 'PROPN' or tok.pos_ == 'NOUN') and tok.head.dep_=='ROOT': 
                x = compound_noun + ' '+ tok.text 
            
            # extract object 
            if tok.dep_.endswith("obj") == True and (tok.pos_ == 'PROPN' or tok.pos_ == 'NOUN') and tok.head.dep_ == 'ROOT': 
                y = compound_noun + ' '+ tok.text
                y_children = tok.conjuncts
                child = [child for child in tok.rights if child.pos_=='NOUN']
                if len(y_children)!= 0:
                    more_y =True
                elif len(child)!=0 and child[0].dep_ == 'appos':
                    y_children = child[0].conjuncts
                    more_y = True

            if more_y and tok.dep_ == 'conj' and tok in y_children:
                y = y+ ',' + compound_noun + ' '+ tok.text

            # extract verb (BUY )
            if tok.dep_ == 'ROOT' and tok.pos_ == 'VERB' :
                verb = tok.text 
            
            # extract price
            if tok.ent_type_ == 'MONEY' or tok.text.lower == 'us$':
                if prev_tok_price:
                    price = price+ tok.text
                else:
                    price = tok.text
                    prev_tok_price = True
            
            #extract quantity
            if (tok.dep_ == 'nummod' or tok.pos_ == 'NUM') and tok.i < len(doc)-1  and tok.nbor() == tok.head and tok.ent_type_ != 'MONEY':
                if quantity == '':
                    quantity = tok.text
                else :
                    quantity = quantity + ','+tok.text 

            if tok.dep_ == 'compound':
                compound_noun = compound_noun + ' '+ tok.text
            else:
                compound_noun = ''

    return [x, y, price, quantity,'']

