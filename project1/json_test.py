import json


with open ('test.json', 'r', encoding='utf-8') as f:
    qa = json.load(f)

print(qa)

for i in qa["q_and_a"]:
    print(i["qwe"])
#    print(i["ans"])
    for z in i["ans"]:
        print(z)

with open('test_wr.json', 'w', encoding='utf-8') as fw:
    json.dump(qa,fw,indent=2)

#for i in qa["q_and_a"]:
#    for q in i["ans"]:
#        print(q["ans"])