# https://stackoverflow.com/questions/11968976/list-files-only-in-the-current-directory

import os
import json

#var data = 
#    {
#        name: 'node1', id: 1,
#        children: [
#            { name: 'child1', id: 2 },
#            { name: 'child2', id: 3 }
#        ]
#    };
def visit(d_or_f, dir_node, seq_dict):

    if not os.path.isdir(d_or_f):
        return
    #print('visit:', d_or_f)

    for f in os.listdir(d_or_f):
        #print('visit:', f)

        child = {'name':os.path.basename(f), 'id': (seq_dict['seq']), 'is_dir': os.path.isdir(f)}
        seq_dict['seq'] = seq_dict['seq'] + 1
        
        if 'children' not in dir_node:
            dir_node['children'] = []
        dir_node['children'].append(child)


        visit(f, child, seq_dict)


root='../md'
seq_dict = {'seq':0}
data = {'name':os.path.basename(root), 'id': seq_dict['seq']}
seq_dict['seq'] = seq_dict['seq'] + 1

visit(root, data, seq_dict)
print(json.dumps(data))


