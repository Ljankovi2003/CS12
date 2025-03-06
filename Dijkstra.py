import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
import time

matplotlib.use('Agg')

def create_graph():
    G = nx.Graph()
    nodes = [(x, y) for x in range(6) for y in range(4)]  # Grid from (0,0) to (5,3)
    edges = []
    
    for x in range(6):
        for y in range(4):
            G.add_node((x, y))
            if x < 5:
                edges.append(((x, y), (x+1, y), 1))
            if y < 3:
                edges.append(((x, y), (x, y+1), 1))
    
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    return G

def generate_map(G, robot_pos, path=[], show_path_first=False):
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#161b22')
    pos = {node: node for node in G.nodes()}
    
    ax.set_facecolor('#161b22')
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    nx.draw(G, pos, with_labels=True, node_color='#00aaff', edge_color='#00ff99', node_size=600, font_color='white', ax=ax)
    
    if path:
        nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='#ffcc00', width=2, ax=ax)
    
    if not show_path_first:
        ax.scatter(*robot_pos, color='purple', s=900, marker='s')
        
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', facecolor='#161b22')
    plt.close(fig) 
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')
