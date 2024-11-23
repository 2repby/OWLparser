from owlready2 import *
onto = get_ontology("competencies2.rdf").load()
sync_reasoner(infer_property_values=True)
semesters = list(default_world.sparql("""
           SELECT ?s ?l
           WHERE {?s a <http://www.enu.kz/ontologies/curriculum#Semester>.
            ?s rdfs:label ?l.
            FILTER(LANG(?l) = "" || LANGMATCHES(LANG(?l), "en"))
           }  
           ORDER BY ?s
    """))
for semester in semesters:
    print('=======================================================================')
    print(semester[1])
    print('=======================================================================')
    courses = list(default_world.sparql("""
               SELECT ?c ?l
               WHERE {?c <http://www.enu.kz/ontologies/curriculum#studiedDuring> ?s .
               ?c rdfs:label ?l.
              
               ?s rdfs:label '""" + semester[0].label[0] + """'.
               FILTER(LANG(?l) = "" || LANGMATCHES(LANG(?l), "en")).
               }
               
                ORDER BY ?c
        """))
    for course in courses:
        print('-----------------------------------------------------------------------')
        print('Course:', course[1])
        print('-----------------------------------------------------------------------')
        print('Trained competencies:')
        competencies = list(default_world.sparql("""
                   SELECT ?lcmp
                   WHERE {?c <http://www.enu.kz/ontologies/curriculum#train> ?cmp .
                   ?cmp rdfs:label ?lcmp .
                   FILTER(LANG(?lcmp) = "" || LANGMATCHES(LANG(?lcmp), "en")).
                   ?c rdfs:label '""" + course[1] + """'
                   }
                    ORDER BY ?c
            """))
        i = 1
        for competency in competencies:
            print("  ", i, ".", competency[0], sep='')
            i += 1

print('============= Skills tree =================')
# recursive function
def get_skills(skill, i):
    skills = list(default_world.sparql("""
           prefix enu: <http://www.enu.kz/ontologies/curriculum#>
           SELECT ?s ?l
           WHERE {
           ?s enu:isPartOf ?x.
           ?s rdfs:label ?l
            ?x rdfs:label '""" + skill + """'
            FILTER(LANG(?l) = "" || LANGMATCHES(LANG(?l), "en"))
           }
            ORDER BY ?s
    """))
    i += 1
    for s in skills:
        print(' ' * 2 * i, s[0].name[6:], '. ', s[1], sep='')
        get_skills(s[1], i)
# Obtaining top-level competencies (not having parent ones)
top_skills = list(default_world.sparql("""
           prefix enu: <http://www.enu.kz/ontologies/curriculum#>
           SELECT ?s ?l
           WHERE {
           ?s a enu:Skill .
           ?s rdfs:label ?l .
              FILTER NOT EXISTS {
                ?s enu:isPartOf ?x
                }.
            FILTER(LANG(?l) = "" || LANGMATCHES(LANG(?l), "en"))
           }
            ORDER BY ?s
    """))
for skill in top_skills:
    print(skill[0].name[6:], '. ', skill[1], sep='')
    get_skills(skill[1], 1)




