# https://stackoverflow.com/questions/11968976/list-files-only-in-the-current-directory

import os
import json


#
# var data =
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
    # print('visit:', d_or_f)

    # use scan instead of listdir, because listdir return 'string' but scandir return object
    for f in os.scandir(d_or_f):
        # print('visit:', f)

        if os.path.isdir(f):
            url = dir_node['url']+'/'+os.path.basename(f)
        else:
            url = dir_node['url']+'/'+os.path.splitext(os.path.basename(f))[0]+'.html'
        child = {'name': os.path.basename(f),
                 'id': (seq_dict['seq']),
                 'is_dir': os.path.isdir(f),
                 'url': url}
        seq_dict['seq'] = seq_dict['seq'] + 1
        
        if 'children' not in dir_node:
            dir_node['children'] = []
        dir_node['children'].append(child)

        visit(f, child, seq_dict)


root = '../md'
seq = {'seq': 0}
data = {'name': os.path.basename(root),
        'id': seq['seq'],
        'url': 'md'}
seq['seq'] = seq['seq'] + 1

visit(root, data, seq)
print(json.dumps(data))

# python3 generate_github_index_data.py| python3 -m json.tool
