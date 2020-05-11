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

