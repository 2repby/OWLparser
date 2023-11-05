from owlready2 import *
from data import *

onto = get_ontology("/Users/kda/Documents/Интеллектуальные информационные системы/Модель компетенций/empty.rdf").load()
for competency in competencies:
    skill = onto.Skill(competency[0])
    skill.label = []
    for label in competency[1]:
        skill.label.append(locstr(label[0], lang=label[1]))
    if competency[2]:
        parent_skill = onto.Skill(competency[2])
        skill.isPartOf = [parent_skill]

for target_skill in set(map(lambda x: x[0], dependencies)):
    # print(target_skill)
    skill = list(filter(lambda x: x.name == target_skill, list(onto.individuals())))[0]
    required_skills = list(filter(lambda x: x.name in list(map(lambda z: z[1], filter(lambda y: y[0] == target_skill, dependencies))), list(onto.individuals())))
    skill.requires = required_skills
    print(skill.name, skill.label,"требует", list(map(lambda a: (a.name), required_skills)))

for course in courses:
    print(course)
    discipline = onto.Course(course[0])
    discipline.label = []
    for label in course[1]:
        discipline.label.append(locstr(label[0], lang=label[1]))

    discipline.credits = course[2]
    discipline.exam = []
    for exam in course[3]:
        discipline.exam.append(locstr(exam[0], lang=exam[1]))
    semester = list(filter(lambda x: x.name == course[4], list(onto.individuals())))[0]
    discipline.studiedDuring = semester

for course in set(map(lambda x: x[0], discipline_competency_mapping)):
    discipline = list(filter(lambda x: x.name == course, list(onto.individuals())))[0]
    # print(discipline)
    skills = list(filter(lambda x: x.name in list(map(lambda z: z[1], filter(lambda y: y[0] == course, discipline_competency_mapping))), list(onto.individuals())))
    # print(skills)
    discipline.train = skills


# sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
# sync_reasoner(infer_property_values = True)

onto.save(
        file="/Users/kda/Documents/Интеллектуальные информационные системы/Модель компетенций/Competencies2.rdf")

for course in onto.Course.instances():
    print('Курс:', course.label[0], 'Объем:', course.credits, 'Контроль:', course.exam[0])
    print('Формируемые компетенции:')
    for s in list(filter(lambda x: x[0] == course, list(onto.train.get_relations()))):
        print('      ', s[1].name, s[1].label[0])
