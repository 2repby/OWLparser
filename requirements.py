from owlready2 import *
onto = get_ontology("/Users/kda/Documents/Интеллектуальные информационные системы/Модель компетенций/competencies2.rdf").load()
# onto = get_ontology("/Users/kda/ontologies/curriculum/curriculum.owl").load()
# sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
sync_reasoner(infer_property_values=True)
LANG = "en"

for semester in onto.Semester.instances():
    print('=======================================================================')
    print(semester.label.get_lang("en")[0])
    print('=======================================================================')
    print("Skills obtained in previous semesters:")
    prev_skills = list(default_world.sparql("""
                   prefix enu: <http://www.enu.kz/ontologies/curriculum#>
                   SELECT DISTINCT ?c  ?l
                   WHERE {
                       ?c rdfs:label ?l .
                        ?c enu:trainedBy ?d .
                        ?d enu:studiedDuring ?p.
                        ?p enu:goesBefore ?s .
                        FILTER(LANG(?l) = "" || LANGMATCHES(LANG(?l), "en")).
                       ?s rdfs:label '""" + semester.label[0] + """' 
                      }
               """))
    for skill in prev_skills:
        print('      ', skill[0].name, skill[1])

    # print("Courses taken:")
    # courses = list(default_world.sparql("""
    #                prefix enu: <http://www.enu.kz/ontologies/curriculum#>
    #                SELECT DISTINCT ?d
    #                WHERE {
    #                     ?d enu:studiedDuring ?s.
    #                    ?s rdfs:label '""" + semester.label[0] + """'
    #                   }
    #            """))
    # for c in courses:
    #     print('      ', c[0].name, c[0].label[0])

    # print("Skills developed:")
    # comp1 = list(default_world.sparql("""
    #                prefix enu: <http://www.enu.kz/ontologies/curriculum#>
    #                SELECT DISTINCT ?c
    #                WHERE {
    #                     ?d enu:train ?c .
    #                     ?d enu:studiedDuring ?s .
    #                    ?s rdfs:label '""" + semester.label[0] + """'
    #                   }
    #
    #            """))
    # for c in comp1:
    #     print('      ', c[0].name, c[0].label[0])

    print("Skills required:")
    prereq_skills = list(default_world.sparql("""
                   prefix enu: <http://www.enu.kz/ontologies/curriculum#>
                   SELECT DISTINCT ?q ?l
                   WHERE {
                        ?c enu:requires ?q
                        ?q rdfs:label ?l .
                        ?d enu:train ?c .
                        ?d enu:studiedDuring ?s.
                        FILTER(LANG(?l) = "" || LANGMATCHES(LANG(?l), "en")).
                       ?s rdfs:label '""" + semester.label[0] + """' 
                      }
               """))
    for skill in prereq_skills:
        print('      ', skill[0].name, skill[1])

    print("MISSING SKILLS:")
    for skill in prereq_skills:
        if skill[0].name not in map(lambda x: x[0].name, prev_skills):
            print('      ', skill[0].name, skill[1])

