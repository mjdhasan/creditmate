from bs4 import BeautifulSoup
import numpy as np
from init import UPLOAD_DIRECTORY, SCRAPED_DIRECTORY, UPLOAD_PARSED_DIRECTORY

file_name = f'{SCRAPED_DIRECTORY}/scb_test.html'

# html structure into network graph:
# https://stackoverflow.com/questions/53817270/html-structure-into-network-graph
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
from collections import defaultdict
from bs4 import BeautifulSoup as soup


def find_first_match(l_1, l_2):
    """
    Return the first element in l_1 that matches an element in l_2
    :param l_1:
    :param l_2:
    :return:
    """
    for elem_1 in l_1:
        if elem_1 in l_2:
            return elem_1
    return None
# find_first_match(l_1=['iframe', 'head', 'html', '[document]'],
#                  l_2=['html', 'link'])


def format_text(text):
    for code in ['\xa0']:
        text = text.replace(code, '')
    for code in ['\t', '\n']:
        text = text.replace(code, '')

    text = text.lstrip()
    text = text.rstrip()

    return text


def get_node_attrs(i):
    node_dict = {}
    node_name = i.name
    node_dict['node'] = i
    node_dict['name'] = node_name
    # node_dict['title'] = i.attrs['title']
    if node_name == 'html':
        node_title = i.title.text if i.title is not None else ''
        node_title = format_text(node_title)
        if node_title != '':
            node_dict['text'] = node_title
    elif node_name in ['p', 'span']:
        node_text = format_text(i.text)
        if node_text != '':
            node_dict['text'] = node_text
    elif node_name in ['a']:
        node_title = i.attrs['title'] if 'title' in i.attrs.keys() else ''
        node_title = format_text(node_title)
        if node_title != '':
            node_dict['text'] = node_title
        node_href = i.attrs['href'] if 'href' in i.attrs.keys() else ''
        if node_href != '':
            node_dict['href'] = node_href
    elif node_name in ['img']:
        node_title = i.attrs['title'] if 'title' in i.attrs.keys() else ''
        node_title = format_text(node_title)
        if node_title != '':
            node_dict['text'] = node_title
        node_alt = node_details.attrs['alt'] if 'alt' in node_details.attrs.keys() else ''
        if node_alt != '':
            node_dict['alt'] = node_alt
        node_src = node_details.attrs['src'] if 'src' in node_details.attrs.keys() else ''
        if node_src != '':
            node_dict['src'] = node_src

    return node_dict


# ex0 = "<html><head><title>Are you lost ?</title></head><body><h1>Lost on the Intenet ?</h1><h1>Don't panic, we will help you</h1><strong><pre>    * <----- you are here</pre></strong></body></html>"
with open(file_name, 'r') as f:
    contents = f.read()
d = soup(contents, 'html.parser')

# def _traverse_html(_d: soup, _graph: nx.Graph, _counter, _dict, _parent=None) -> None:
#     for i in _d.contents:
#         if (i.name is not None):  # and (i.name not in l_tag_exclude)
#             try:
#                 _name_count = _counter.get(i.name)
#                 _name = i.name if not _name_count else f'{i.name}_{_name_count}'
#
#                 if _parent is not None:
#                     _graph.add_node(_parent)
#                     _graph.add_edge(_parent, _name)
#
#                 _counter[i.name] += 1
#                 _dict[_name] = i
#                 _traverse_html(i, _graph, _counter, _dict, _name)
#             except AttributeError:
#                 pass

l_tag_exclude = ['div', 'ul', 'li', 'g', 'style', 'svg', 'script', 'noscript', 'button']
l_tag_include = ['html', 'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'iframe', 'image', 'img',
                 'picture', 'p', 'span', 'a', 'title', 'nav', 'label', 'link', 'input']


def _traverse_html(_d: soup, _graph: nx.Graph, _counter, _dict, _parent=None) -> None:
    for i in _d.contents:
        if i.name is not None:  # and (i.name not in l_tag_exclude)
            try:
                _name_count = _counter.get(i.name)
                _name = i.name if not _name_count else f'{i.name}_{_name_count}'
                _counter[i.name] += 1
                if i.name in l_tag_include:
                    # find all parents of i
                    i_parents = [node.name for node in i.find_parents()]
                    # identify the first parent of i present in _graph nodes
                    _parent = find_first_match(l_1=i_parents, l_2=list(_graph.nodes))
                    if _parent is not None:
                        # _graph.add_node(_parent)
                        _graph.add_edge(_parent, _name)
                    else:
                        _graph.add_node(_name)
                    _parent = _name
                    # _dict[_parent] = i
                    _dict[_parent] = get_node_attrs(i=i)
                _traverse_html(i, _graph, _counter, _dict, _parent)
            except AttributeError as e:
                print(e)
                pass


_full_graph = nx.DiGraph()
node_dict = {}
_traverse_html(d, _full_graph, defaultdict(int), node_dict)
node_dict['body']['text'] = node_dict['html']['text']

# nx.draw(_full_graph, with_labels=True)
# plt.show()

pos = graphviz_layout(_full_graph, prog='dot')
nx.draw_networkx_edges(_full_graph, pos, arrows=True, label=True)


dir(_full_graph)

# examine node_dict
list(node_dict.keys())[:20]
l_node_names = np.unique([node_dict[key]['name'] for key in node_dict.keys()])
node_dict['iframe']
node_dict['title']
node_dict['a_10']
nx.descendants(_full_graph, 'link_2')
nx.ancestors(_full_graph, 'nav')
_full_graph.subgraph(['html', 'body', 'nav', 'p_30']).edges
# examine edges
l_edges = [edge for edge in _full_graph.edges]
l_edges[:20]
# examine nodes
len(_full_graph.nodes)
len(node_dict.keys())
l_nodes = [node for node in _full_graph.nodes]
len(l_nodes)
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

pos = nx.spring_layout(sG, scale=20, k=3 / np.sqrt(_full_graph.order()))
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
#### extract relevant info for each node ####
#############################################

#### loop over node_dict, and extract relvant text
l_nodes = [node for node in _full_graph.nodes]
l_node_names = np.unique([node_dict[node].name for node in _full_graph.nodes])
l_nodes_ul = [node for node in l_nodes if node_dict[node].name == 'img']
l_tag_exclude = ['style', 'svg', 'script', 'noscript', 'button']
name_dict = {}
title_dict = {}
text_dict = {}
href_dict = {}
for node_id in l_nodes:
    try:
        node_details = node_dict[node_id]
    except Exception as e:
        title_dict[node_id] = ''
        text_dict[node_id] = ''
        href_dict[node_id] = ''
        print('error in node_details = node_dict[node_id] in html_parse.py:')
        print(e)
        continue

    node_name = node_details.name if node_details.name is not None else ''
    node_title = node_details.title if node_details.title is not None else ''
    # try:
    #     node_name = node_details.name
    #     name_dict[node_id] = node_name
    # except Exception as e:
    #     print('error in node_name = node_details.name in html_parse.py')
    #     print(e)

    name_dict[node_id] = node_name
    if node_name in l_tag_exclude:
        title_dict[node_id] = ''
        text_dict[node_id] = ''
        href_dict[node_id] = ''
    elif node_name == 'html':
        title_dict[node_id] = node_title
        text_dict[node_id] = node_title
        href_dict[node_id] = ''
    elif node_name == 'head':
        title_dict[node_id] = node_title
        text_dict[node_id] = node_title
        href_dict[node_id] = ''
    elif node_name in ['p', 'span']:
        title_dict[node_id] = node_title
        text_dict[node_id] = node_details.text
        href_dict[node_id] = ''
    elif node_name in ['ul']:
        node_title = node_details.attrs['title'] if 'title' in node_details.attrs.keys() else ''
        title_dict[node_id] = node_title
        text_dict[node_id] = node_title
        href_dict[node_id] = ''
    elif node_name in ['a']:
        node_title = node_details.attrs['title'] if 'title' in node_details.attrs.keys() else ''
        node_href = node_details.attrs['href'] if 'href' in node_details.attrs.keys() else ''
        title_dict[node_id] = node_title
        text_dict[node_id] = node_details.text
        href_dict[node_id] = node_href
    elif node_name in ['li']:
        title_dict[node_id] = node_title
        text_dict[node_id] = node_details.text
        href_dict[node_id] = node_href
    elif node_name in ['img']:
        title_dict[node_id] = node_title
        text_dict[node_id] = node_details.attrs['alt'] if 'alt' in node_details.attrs.keys() else ''
        href_dict[node_id] = node_details.attrs['src'] if 'src' in node_details.attrs.keys() else ''
    else:
        title_dict[node_id] = ''
        text_dict[node_id] = ''
        href_dict[node_id] = ''

node_dict['a_184'].parent.name
text_dict['a_184']
l_desc = list(nx.descendants(_full_graph, 'a_184'))
len(l_desc)
text_dict[l_desc[6]]
list(nx.descendants(_full_graph, 'title_2'))
[{id: node_dict[id]} for id in nx.descendants(_full_graph, 'title_10')]
[{id: node_dict[id]} for id in nx.descendants(_full_graph, 'path_157')]
node_dict['a_10'].attrs['title']
[{id: node_dict[id].text} for id in nx.descendants(_full_graph, 'a_10') if 'span' in id]

node_dict['a_22'].attrs['title']
node_dict['a_22'].text
node_dict['p_10']
nx.ancestors(_full_graph, 'p_10')
# draw network graph from an an id
sG = nx.subgraph(_full_graph, ['p_10'] + list(nx.ancestors(_full_graph, 'p_10')))
sG.edges
nx.draw(sG)
pos = graphviz_layout(_full_graph, prog='dot')
nx.draw_networkx_edges(_full_graph, pos, arrows=True)
