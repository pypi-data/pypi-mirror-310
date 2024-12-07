import uuid

import networkx as nx
from nltk.tree import ParentedTree


class ParseTree(ParentedTree):
    def get_hash(self, T=None):
        if T is None:
            T = self
        if isinstance(T, ParseTree):
            return T.label() + '(' + self.get_hash(T[0]) + ',' + self.get_hash(T[1]) + ')'
        else:
            return str(len(T))

    def __deepcopy__(self, memo=None):
        return self.copy(True)

    def count_left_of(self, pos):
        if not pos:
            return 0
        if pos[-1] == 1:
            if isinstance(self[pos[:-1]][0], ParseTree):
                add = len(self[pos[:-1]][0].leaves())
            else:
                add = 1
        else:
            add = 0
        return add + self.count_left_of(pos[:-1])

    def count_right_of(self, pos):
        if not pos:
            return 0
        if pos[-1] == 0:
            if isinstance(self[pos[:-1]][1], ParseTree):
                add = len(self[pos[:-1]][1].leaves())
            else:
                add = 1
        else:
            add = 0
        return add + self.count_right_of(pos[:-1])

    def get_first_left(self, pos):
        if not pos:
            return ()
        if pos[-1] == 1:
            return pos[:-1] + [0]
        else:
            return self.get_first_left(pos[:-1])

    def get_first_right(self, pos):
        if not pos:
            return ()
        if pos[-1] == 0:
            return pos[:-1] + [1]
        else:
            return self.get_first_right(pos[:-1])

    def to_networkx(
            self,
            g=None,
            parent=None,
            concept=None
    ):
        if g is None:
            g = nx.DiGraph()
        if concept is None:
            concept = 'ROOT'
        label = self.label()
        try:
            relation, first, second = label.split('[')
        except ValueError:
            relation, first, second = label, label, label
        first = first.split(']')[0]
        second = second.split(']')[0]
        node_id = uuid.uuid4()
        g.add_node(node_id, concept=concept, text=label, relation=relation)
        if parent is not None:
            g.add_edge(parent, node_id)
        if isinstance(self[0], ParseTree):
            self[0].to_networkx(g=g, parent=node_id, concept=first)
        else:
            leaf_id = uuid.uuid4()
            g.add_node(leaf_id, concept=first, text=self[0], relation='Leaf')
            g.add_edge(node_id, leaf_id)
        if len(self) > 1 and isinstance(self[1], ParseTree):
            self[1].to_networkx(g=g, parent=node_id, concept=second)
        else:
            leaf_id = uuid.uuid4()
            try:
                g.add_node(leaf_id, concept=second, text=self[1], relation='Leaf')
            except IndexError:
                g.add_node(leaf_id, concept=second, text=self[0], relation='Leaf')
            g.add_edge(node_id, leaf_id)
        return g
