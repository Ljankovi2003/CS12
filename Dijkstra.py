import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
import time

matplotlib.use('Agg')  # Use non-interactive backend

def create_graph():
    G = nx.Graph()
    nodes = [(x, y) for x in range(6) for y in range(4)]  # Grid from (0,0) to (5,3)
    edges = []
    
    for x in range(6):
        for y in range(4):
            if x < 5:
                edges.append(((x, y), (x+1, y), 1))
            if y < 3:
                edges.append(((x, y), (x, y+1), 1))
    
    for node in nodes:
        G.add_node(node)
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    return G

def generate_map(G, robot_pos, path=[], show_path_first=False):
    plt.figure(figsize=(6, 4))
    pos = {node: node for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='black', node_size=500)
    
    if path:
        nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='blue', width=2)

    if not show_path_first:
        plt.scatter(*robot_pos, color='purple', s=800, marker='s', label='Robot')
        plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))  # Only show legend if robot is drawn

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()  # Close figure to prevent excessive open figures
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')
