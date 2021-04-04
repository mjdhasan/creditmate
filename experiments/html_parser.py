from bs4 import BeautifulSoup
import numpy as np
from init import UPLOAD_DIRECTORY, SCRAPED_DIRECTORY, UPLOAD_PARSED_DIRECTORY
file_name = f'{SCRAPED_DIRECTORY}/scb_test.html'

# test that saved html file is parsable
with open(file_name, 'r') as f:
    contents = f.read()
soup = BeautifulSoup(contents, 'html.parser')
dir(soup)
# get head
soup_head = soup.find_all('head')[0]
soup_head_children = [child for child in soup_head.findChildren(recursive=False)]
len(soup_head_children)
np.unique([child.name for child in soup_head_children])
for child_name in ['title']:  # , 'link', 'meta'
    l_child = [child for child in soup_head_children if child.name == child_name]
    for child in l_child:
        dir(child)
        tag_text = child.text

# body details
soup_body = soup.find_all('body')[0]
soup_body_children = [child for child in soup_body.findChildren(recursive=False)]
np.unique([child.name for child in soup_body_children])
l_tag_exclude = ['style', 'svg', 'script', 'noscript', 'button']
soup_body_exclude = [child for child in soup_body_children if child.name in l_tag_exclude]
soup_body_noscript = [child for child in soup_body_children if child.name in ['noscript']]
soup_body_children = [child for child in soup_body_children if child.name not in l_tag_exclude]
l_tags = []
for child in soup_body_children:
    # dir(child)
    if child.name == 'header':
        child = child.findAll('nav')[0]
    l_grandchild = [child for child in child.findChildren(recursive=False) if child.name not in l_tag_exclude]
    l_grandchild_names = [child.name for child in l_grandchild]
    for grandchild in l_grandchild:
        l_ggrandchild = [child for child in grandchild.findChildren(recursive=False) if child.name not in l_tag_exclude]
        for ggrandchild in l_ggrandchild:
            if ggrandchild.name == 'li':
                l_tags = l_tags + [{'span': ggrandchild.a.span}]
                ggrandchild.a['href']
                ggrandchild.a.text
                ggrandchild.find_all('href')


        len([grandchild.findChildren()])
        dir(grandchild)
        grandchild.attrs

        len(tag_nav.findChildren(recursive=False))

# all soup_children
soup_children = [child for child in soup.findChildren()]
len(soup_children)
l_child_names = [child.name for child in soup_children]
l_child_names = np.unique(l_child_names).tolist()
l_input = [child for child in soup_children if child.name == 'input']
l_para = [child for child in soup_children if child.name == 'p']
len(l_input)
dir(l_input[2])
[child for child in l_input[2].children]
l_input[2].attrs
len(l_para)
l_para[10].text
l_para[10].parent
[child for child in l_para[10].findChildren()]

soup_body = soup.find_all('body')
len(soup_body)
body_children = [child for child in soup_body[0].children]
body_children = [child for child in soup_body[0].findChildren(recursive=False)]
len(body_children)
type(body_children[0])
# np.unique([type(child) for child in body_children])
# body_children[1].name
[child.name for child in body_children]
l_header = [child for child in body_children if child.name == 'header']
len(l_header)
header_children = [l_header[0].findChildren(recursive=False)]
len(header_children[0][0])
type(header_children[0][0])
header_children[0][0].name
header_grand_child = [child for child in header_children[0][0].findChildren(recursive=False)]
type(header_grand_child)
len(header_grand_child)
dir(header_grand_child)
dir(header_grand_child[0])
len([child for child in header_grand_child[0].findChildren(recursive=False)])


# convet html to tree: https://stackoverflow.com/questions/14172028/html-parse-tree-using-python-2-7s
import networkx as nx
from lxml import html
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

# raw = "...your raw html"
with open(file_name, 'r') as f:
    contents = f.read()

# def traverse(parent, graph, labels):
#     labels[parent] = parent.tag
#     for node in parent.getchildren():
#         graph.add_edge(parent, node)
#         traverse(node, graph, labels)

from bs4.element import NavigableString
def traverse(parent, graph, labels):
    labels[parent] = parent.name
    for node in parent.children:
        if isinstance(node, NavigableString):
            continue
        # graph.add_edge(hash(parent), hash(node))
        graph.add_edge(parent, node)
        traverse(node, graph, labels)

G = nx.DiGraph()
labels = {}     # needed to map from node to tag
with open(file_name, 'r') as f:
    contents = f.read()
# html_tag = html.document_fromstring(contents)
html_tag = soup(contents, 'html.parser')
# dir(html_tag)
# html_tag.find('div')[0]
traverse(html_tag, G, labels)
dir(G)
type(G.nodes)
l_nodes = [node for node in G.nodes]
len(l_nodes)
type(l_nodes[500])
dir(l_nodes[500])
l_nodes[4].name
l_nodes[500].get_text()
# l_nodes[500].find_rel_links('body')
[item for item in l_nodes[500].items()]
l_nodes[500].getparent().text
l_nodes[500].getnext().text
l_nodes[500].base_url
l_nodes[500].attrib
l_nodes[500].text
l_nodes[500].text_content()
l_nodes[500].keys()
dir(l_nodes[500].getroottree())
# l_nodes[500].xpath()

pos = graphviz_layout(G, prog='dot')

label_props = {'size': 16,
               'color': 'black',
               'weight': 'bold',
               'horizontalalignment': 'center',
               'verticalalignment': 'center',
               'clip_on': True}
bbox_props = {'boxstyle': "round, pad=0.2",
              'fc': "grey",
              'ec': "b",
              'lw': 1.5}

nx.draw_networkx_edges(G, pos, arrows=True)
ax = plt.gca()

for node, label in labels.items():
    x, y = pos[node]
    ax.text(x, y, label,
            bbox=bbox_props,
            **label_props)

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
plt.show()

# nodes with descendants
l_nodes = [node for node in G.nodes]
l_nodes_w_desc = []
i = 0
for node in l_nodes:
    l_descendants = list(nx.descendants(G, node))
    if len(l_descendants) > 0:
        print(f'{i}: {node}')
        l_nodes_w_desc = l_nodes_w_desc + [{'i': node}]
    i = i + 1

print('nodes')
print(l_nodes_w_desc)

# html structure into network graph:
# https://stackoverflow.com/questions/53817270/html-structure-into-network-graph
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from bs4 import BeautifulSoup as soup
# ex0 = "<html><head><title>Are you lost ?</title></head><body><h1>Lost on the Intenet ?</h1><h1>Don't panic, we will help you</h1><strong><pre>    * <----- you are here</pre></strong></body></html>"
with open(file_name, 'r') as f:
    contents = f.read()
d = soup(contents, 'html.parser')


def _traverse_html(_d: soup, _graph: nx.Graph, _counter, _dict, _parent=None) -> None:
    for i in _d.contents:
        if (i.name is not None):  # and (i.name not in l_tag_exclude)
            try:
                _name_count = _counter.get(i.name)
                _name = i.name if not _name_count else f'{i.name}_{_name_count}'

                if _parent is not None:
                    _graph.add_node(_parent)
                    _graph.add_edge(_parent, _name)

                _counter[i.name] += 1
                _dict[_name] = i
                _traverse_html(i, _graph, _counter, _dict, _name)
            except AttributeError:
                pass


_full_graph = nx.DiGraph()
node_dict = {}
_traverse_html(d, _full_graph, defaultdict(int), node_dict)
nx.draw(_full_graph, with_labels=True)
# plt.show()

pos = graphviz_layout(_full_graph, prog='dot')
nx.draw_networkx_edges(_full_graph, pos, arrows=True)

dir(_full_graph)
len(_full_graph.nodes)
len(node_dict.keys())
l_nodes = [node for node in _full_graph.nodes]
l_nodes[550].name
l_nodes[550].get_text()
l_nodes[550].find('a', href=True)
dir(l_nodes[550])
# edges
l_edges = [edge for edge in _full_graph.edges]
len(l_edges)
l_edges[:20]


# print subgraph of descendants
l_nodes = [node for node in _full_graph.nodes]
l_nodes_w_desc = []
i = 0
for node in l_nodes:
    l_descendants = list(nx.descendants(_full_graph, node))
    if len(l_descendants) > 0:
        print(f'{i}: {node}')
        l_nodes_w_desc = l_nodes_w_desc + [[{'i': i}, {'node': node}, {'n_desc': len(l_descendants)}]]
    i = i + 1

len(l_nodes_w_desc) / len(l_nodes)
l_nodes_w_desc[150]

# l_descendants = list(nx.descendants(_full_graph, l_nodes[500]))
# len(l_descendants)
# dir(l_descendants[0])
# l_descendants[0].title
#
l_nodes = [node for node in _full_graph.nodes]
l_descendants = list(nx.descendants(_full_graph, l_nodes[394]))
# l_descendants[:10]
_subgraph = _full_graph.subgraph([l_nodes[394], l_descendants[25]])
# _subgraph = _full_graph.subgraph([l_nodes[394], l_descendants[10], l_descendants[25]])
len(_subgraph.nodes)
# pos = nx.spring_layout(_subgraph, scale=20, k=3/np.sqrt(_full_graph.order()))
# nx.draw(_subgraph, pos,
#         node_color='lightblue',
#         with_labels=True,
#         node_size=1500,
#         arrowsize=20)
pos = graphviz_layout(_subgraph, prog='dot')
nx.draw_networkx_edges(_subgraph, pos, arrows=True)


_full_graph.subgraph([l_nodes[10]]).edges
_subgraph = _full_graph.subgraph([l_nodes[10], l_descendants[5]])
dir(_subgraph)
_subgraph.nodes
_subgraph.edges

# extract subgraphs
from itertools import combinations

H = nx.to_undirected(_full_graph)
l_nodes = [node for node in _full_graph.nodes]
len(l_nodes)
nodelist = [l_nodes[0], l_nodes[10], l_descendants[5], l_nodes[100], l_nodes[110], l_nodes[910]]
paths = {}
path_lenghts = {}
l_nodes = [node for node in combinations(nodelist, r=2)]
for nodes in combinations(nodelist, r=2):
    path_lenghts[nodes] = nx.shortest_path_length(_full_graph, *nodes)
    paths[nodes] = nx.shortest_path(G=_full_graph, source=nodes[0], target=nodes[1])

print(paths)

max_path = max(paths.items(), key=lambda x: x[1])[0]
longest_induced_path = nx.shortest_path(H, *max_path)

sG = nx.subgraph(G=_full_graph, nbunch=longest_induced_path)

pos = nx.spring_layout(sG, scale=20, k=3/np.sqrt(_full_graph.order()))
nx.draw(sG, pos, node_color='lightblue',
        with_labels=True,
        node_size=1500,
        arrowsize=20)


# weakly connected subgraphs
dir(nx)
l_subgraphs = list(nx.connected_components(_full_graph))
len(l_subgraphs)
len(l_subgraphs[0].nodes)

#############################################
#### extract relevant text for each node ####
#############################################

#### loop over node_dict, and extract relvant text