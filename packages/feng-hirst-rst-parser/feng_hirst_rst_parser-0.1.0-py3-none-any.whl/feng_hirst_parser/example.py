import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

from feng_hirst_parser.parse import DiscourseParser
from feng_hirst_parser.trees.extract_metrics import extract_metrics, extract_relation_ngrams

import os


def demo(output_dir: str):
    verbose = False
    skip_parsing = False
    file_list = []
    global_features = False
    logging = False
    save_preprocessed = True
    parser = DiscourseParser(
        verbose,
        skip_parsing,
        global_features,
        save_preprocessed,
        output_dir=output_dir
    )
    current_file_dir = os.path.dirname(__file__)
    pt = parser.parse(os.path.join(current_file_dir, 'example.txt'))
    G = pt.to_networkx()
    labels = {
        node: f"{data['concept']}\n{data.get('text', '')}"
        for node, data in G.nodes(data=True)
    }
    plt.figure(figsize=(15, 12))
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, font_size=10)
    plt.show()

    metrics = extract_metrics(G, relation_ngrams=[(1, 2), (3, 4)])
    print(metrics)


if __name__ == '__main__':
    demo(os.environ['OUTPUT_DIR'])
