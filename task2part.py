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

                     
            for i in range(0,len(locations)-1):
                for j in range(i+1,len(locations)):
                    results.add((locations[i],locations[j]))

  
    return results