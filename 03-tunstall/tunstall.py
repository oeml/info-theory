import queue
import math
import itertools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='Symbols produced by the source with probabilities')
parser.add_argument('--D', help='Number of code symbols')
parser.add_argument('--n', help='Desired codeword length')
args = parser.parse_args()

class TunstallNode(object):
    def __init__(self, path, prob, children):
        self.path = path
        self.prob = prob
        self.children = children

prob = {}
with open(args.file, 'r') as f:
    for line in f:
        splitline = line.split()
        prob[splitline[0]] = float(splitline[1])

class TunstallTreeBuilder(object):
    def __init__(self, prob):
        self.probs = {s:p for (s,p) in prob.items()}
        self.root = TunstallNode("", 1, prob)
        self.pq = queue.PriorityQueue()
        self.tiebreaker = itertools.count()
        self._insert_children_into_queue(self.root)

    def _insert_children_into_queue(self, node):
        for (sym, prob) in node.children.items():
            pq_entry = (-prob, next(self.tiebreaker), node.path + sym)
            self.pq.put(pq_entry)

    def _find_node(self, path):
        node = self.root
        for step in path[:-1]:
            node = node.children[step]
        return (node, path[-1])

    def build(self, d, n):
        l = len(self.root.children)
        q = int((math.pow(d,n) - l) // (l - 1))
        
        for i in range(q):
            (_, _, path) = self.pq.get()
            (parent,last_step) = self._find_node(path)  # here it's just probability
            new_node_prob = parent.children[last_step]
            children = {sym : prob*new_node_prob for (sym, prob) in self.probs.items()}
            parent.children[last_step] = TunstallNode(path, new_node_prob, children)
            self._insert_children_into_queue(parent.children[last_step])

        codes = {}
        bin_str = [''.join(p) for p in itertools.product('10', repeat=n)]
        while self.pq.qsize() > 0:
            (_, _, path) = self.pq.get()
            codes[path] = bin_str[self.pq.qsize() - 1]
        return codes

ttb = TunstallTreeBuilder(prob)
codes = ttb.build(int(args.D), int(args.n))
for (source, code) in codes.items():
    print('{:10s}: {:s}'.format(source, code))

av_len = 0
for (source, code) in codes.items():
    seq_prob = 1
    for sym in source:
        seq_prob *= ttb.probs[sym]
    av_len += len(source) * seq_prob

print('Average number of code symbols for source symbol = {:1.2f}'.format(float(args.n) / av_len))

entropy = 0
for (_,p) in ttb.probs.items():
    entropy -= p * math.log(p,2)
print('Theoretical lower bound = {:1.2f}'.format(entropy / math.log(float(args.D),2)))
