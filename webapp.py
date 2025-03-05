from flask import Flask, render_template, jsonify, request
from Dijkstra import create_graph, generate_map
import networkx as nx
import time

app = Flask(__name__)
G = create_graph()
robot_position = (0, 0)

@app.route('/')
def index():
    return render_template('index.html', map_image=generate_map(G, robot_position))

@app.route('/navigate', methods=['POST'])
def navigate():
    global robot_position
    target = tuple(map(int, request.json['target'].split(',')))

    if target in G.nodes:
        path = nx.shortest_path(G, source=robot_position, target=target, weight='weight')

        # Show the full Dijkstra path first
        path_image = generate_map(G, robot_position, path, show_path_first=True)

        # Simulate movement along the shortest path only
        images = [path_image]
        for pos in path:
            robot_position = pos
            images.append(generate_map(G, robot_position, path))
            time.sleep(0.2)  # Shorter delay for smooth animation

        return jsonify({'map_images': images})
    else:
        return jsonify({'error': 'Invalid target node'}), 400

if __name__ == '__main__':
    app.run(debug=True)
