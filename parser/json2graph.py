import json, os, sys
from pprint import pprint

raw = json.loads(open("edges.json").read())
edges = [{'p': d['parent'], 'c': d['child']} for d in raw]

# get # of links
print "{0} edges in raw data".format(len(edges))

# remove edges with duplicate children: cleans parallel edges and circles
edges = {e['c']:e for e in edges}.values()

print "{0} edges with duplicate children removed".format(len(edges))

# get unique sets of ids
parent_ids = set([e['p'] for e in edges]) 
child_ids = set([e['c'] for e in edges]) 
all_ids = parent_ids.union(child_ids) 

# get disconnected root nodes
root_node_ids = parent_ids - child_ids

print "found {0} disconnected root nodes".format(len(root_node_ids))

# create ancestor node
ancestor_id = max(all_ids) + 1

print "created ancestor_id: {0}".format(ancestor_id)

# add ancestor edges
ancestor_edges = [{'p': ancestor_id,
		   'c': root_node_id} for root_node_id in root_node_ids]

print "created {0} ancestor edges".format(len(ancestor_edges))

edges.extend(ancestor_edges)

print "{0} edges in final tree".format(len(edges))

# sort edges by parent id:
edges = sorted(edges, key=lambda e: e['p'])

edges_str =  ",\n\t\t".join(["{{ {0}; {1}; }}".format(edge['p'], edge['c']) for edge in edges])
link_values_str =  ",\n\t\t\t\t".join(["{{ @id={0}; @value=T; }}".format(x) for x in xrange(0,len(edges) + 1)])

out = """Graph
{{
	"name";
	"desc";
	{max_node_id}; {num_edges}; 0; 0;
	[
		{edges}
	];
	@enumerations=;
	@attributeDefinitions=[
		{{
			@name=$root;
			@type=bool;
			@default=|| false ||;
			@nodeValues=[ {{ @id=0; @value=T; }} ];
			@linkValues=;
			@pathValues=;
		}},
		{{
			@name=$tree_link;
			@type=bool;
			@default=|| false ||;
			@nodeValues=;
			@linkValues=[
				{link_values}
			];
			@pathValues=;
		}};
	];
}}
""".format(max_node_id=ancestor_id + 1, num_edges=len(edges) + 1, edges=edges_str, link_values=link_values_str)

f = open('out.graph', 'w')
f.write(out)
f.close()

