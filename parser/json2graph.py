import json
from pprint import pprint


data = json.loads(open("edges.json").read())

# pprint(data)
# print json.dumps(data,indent=1)

for i in range(5):
    pprint(data[i]["parent"] + data[i]["child"])
    print(data[i]["parent"], " ", data[i]["child"] )

print(len(data))
