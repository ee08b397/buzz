import json, os, sys
from operator import itemgetter
from pprint import pprint

data = json.loads(open("edges.json").read())

# pprint(data)
# print json.dumps(data,indent=1)
tmplen = len(data)
partial_size = 1315
for i in xrange(partial_size ,tmplen ):
    del data[partial_size]
# get # of links
print(len(data))
sorted(data, key=itemgetter('parent'))

data = sorted(data, key=itemgetter('parent'))

'''
# get # of nodes
dic = {}
# for i in range(5):
for i in range(len(data)):
    dic[data[i]["parent"]] = 1
    dic[data[i]["child"]] = 1
print(len(dic))

'''

dupcount = []
#for i in range(10):
#    for j in xrange(i + 1,10):
for i in range(len(data)):
    for j in xrange(i + 1, len(data)):
        #if data[i]["child"] == data[j]["child"] and data[i]["parent"] != data[j]["parent"]:
        if data[i]["child"] == data[j]["child"]:
            print (
                    str(data[i]["parent"]) + " " + str(data[i]["child"]) + 
                    ") and (" + 
                    str(data[j]["parent"]) + " " + str(data[j]["child"])
                  )
            dupcount.append(j)

dupcount.sort()
print len(dupcount)
for i in range(len(dupcount)):
    data[dupcount[i] - i]
    del data[dupcount[i] - i]

# for i in xrange(50, len(data)):
#    del data[50]

print(len(data))


# unique set of parent and child ids
parent_ids = set([d["parent"] for d in data]) 
child_ids = set([d["child"] for d in data]) 

# all ids
all_ids = parent_ids.union(child_ids) 

mxv = max(all_ids)
print "\n\n" + str(all_ids - set(range(mxv)))

# root nodes only
root_node_ids = parent_ids - child_ids

print "no of free roots: ", str(len(root_node_ids))

# ancestor node
ancestor_id = max(all_ids) + 1

# ancestor edges
for root_node_id in root_node_ids:
    data.append({'parent': ancestor_id,
                 'child': root_node_id})
    print "added ancestor edge: {0}, {1}".format(ancestor_id, root_node_id)



# make node list linear by adding dummy node (n) and dummy edge (n-1, n)
# remember to paint them transparent
# print(set(dic.keys()) - set(range(max(dic) + 1)))
# print(set(range(max(all_ids) + 1)) - set(all_ids))
unused_ids = set(range(max(all_ids) + 1)) - set(all_ids)
print "unused id numbers: " + str(unused_ids)
for num in unused_ids:
    data.append({'parent': ancestor_id,
                 'child' : num })
    print "added accessory edge: {0}, {1}".format(ancestor_id, num)
all_ids = all_ids.union(unused_ids)


'''
parent_ids = set([d["parent"] for d in data]) 
child_ids = set([d["child"] for d in data]) 
all_ids = parent_ids.union(child_ids) 
print "\n " + str(all_ids - set(range(max(all_ids) + 1)))

'''



# recheck: make sure all circles cleaned
dupcount = []
#for i in range(10):
#    for j in xrange(i + 1,10):
for i in range(len(data)):
    for j in xrange(i + 1, len(data)):
        if data[i]["child"] == data[j]["child"]:
            print (
                    str(data[i]["parent"]) + " " + str(data[i]["child"]) + 
                    ") and (" + 
                    str(data[j]["parent"]) + " " + str(data[j]["child"])
                  )
            dupcount.append(j)

print dupcount

# get # of nodes
dic = {}
# for i in range(5):
for i in range(len(data)):
    dic[data[i]["parent"]] = 1
    dic[data[i]["child"]] = 1
print(len(dic))



data = sorted(data, key=itemgetter('parent','child'))


out = "Graph\n{\n"
# name
out += "\t\"name\";\n"

# description
out += "\t\"desc\";\n"

# #nodes, #links, #paths, and #path links
# out += "\t" + str(len(dic)) + "; " + str(len(data)) + "; 0; 0;\n"  
out += "\t" + str(ancestor_id+1) + "; " + str(len(data)) + "; 0; 0;\n"  
# out += "\t" + str(7) + "; " + str(5) + "; 0; 0;\n"  

out += "\t[\n"
# for i in range(4):
for i in range(len(data) - 1):
    out += "\t\t{ " + str(data[i]["parent"]) + "; " + str(data[i]["child"]) + "; },\n"
    # pprint(data[i]["parent"] + data[i]["child"])
    # print(str(data[i]["parent"]), " ", str(data[i]["child"]))
out += "\t\t{ " + str(data[len(data)-1]["parent"]) + "; " + str(data[len(data) - 1]["child"]) + "; }\n"
out += "\t];\n"

# path list
out += "\t; \n" 


out += ("\t@enumerations=;\n" + 
       "\t@attributeDefinitions=[\n"+
       "\t\t{\n"+
       "\t\t\t@name=$root;\n"+
       "\t\t\t@type=bool;\n"+
       "\t\t\t@default=|| false ||;\n"+
       "\t\t\t@nodeValues=[ { @id=" + str(ancestor_id) + "; @value=T; } ];\n"+
       "\t\t\t@linkValues=;\n"+
       "\t\t\t@pathValues=;\n"+
       "\t\t},\n"+
       "\t\t{\n"+
       "\t\t\t@name=$tree_link;\n"+
       "\t\t\t@type=bool;\n"+
       "\t\t\t@default=|| false ||; \n"+
       "\t\t\t@nodeValues=;\n"+
       "\t\t\t@linkValues=[\n")

# for i in range(4):
# for i in range(len(dic) - 1):
# for i in range(3133):
for i in range(len(data) - 1):
#for i in dic:
    out += "\t\t\t\t{ @id=" + str(i) + "; @value=T; },\n"
out += "\t\t\t\t{ @id=" + str(len(data) - 1) + "; @value=T; }\n"

out += (" ];\n" + 
    "@pathValues=; } ]; \n"+
    "@qualifiers=[ { \n" + 
    "@type=$spanning_tree; \n" + 
    "@name=$sample_spanning_tree; \n" +
    "@description=; \n" + 
    "@attributes=[ { \n" + 
    "@attribute=0; \n" + 
    "@alias=$root; }, { \n" + 
    "@attribute=1; \n" + 
    "@alias=$tree_link; } ]; } \n" +
    "];")

# visualization hints
out += "\t; ; ; ;\n"

# interface hints
out += "\t; ; ; ; ;\n"

# file end
out += "}\n"
# print out

f = open('out.graph', 'w')
f.write(out)
f.close()

