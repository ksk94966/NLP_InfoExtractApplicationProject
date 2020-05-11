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