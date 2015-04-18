import json, os, sys
from pprint import pprint

data = json.loads(open("edges.json").read())

# pprint(data)
# print json.dumps(data,indent=1)


# get # of links
print(len(data))

# get # of nodes
dic = {}
for i in range(5):
# for i in range(len(data)):
    dic[data[i]["parent"]] = 1
    dic[data[i]["child"]] = 1
print(len(dic))
out = "Graph\n{\n"




# name
out += "\t\"name\";\n"

# description
out += "\t\"desc\";\n"

# #nodes, #links, #paths, and #path links
# out += "\t" + str(len(dic)) + "; " + str(len(data)) + "; 0; 0;\n"  
out += "\t" + str(7) + "; " + str(5) + "; 0; 0;\n"  

out += "\t[\n"
for i in range(5):
    out += "\t\t{ " + str(data[i]["parent"]) + "; " + str(data[i]["child"]) + "; },\n"
    # pprint(data[i]["parent"] + data[i]["child"])
    print(str(data[i]["parent"]), " ", str(data[i]["child"]))
out += "\t];\n"

# path list
out += "\t;" 

# enum-def, attr-def, qualifer lists
out += "\t; ; ;\n"

# visualization hints
out += "\t; ; ; ;\n"

# interface hints
out += "\t; ; ; ; ;\n"

# file end
out += "}"
print out

f = open('out', 'w')
f.write(out)
f.close()

