import queue
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='Text file with symbols and probabilities')
args = parser.parse_args()

class HuffmanNode(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_children(self):
        return (self.left, self.right)

prob = []
with open(args.file, 'r') as f:
    for line in f:
        sym = line.split()
        prob.append((float(sym[1]), sym[0]))

def create_tree(probs):
    pq = queue.PriorityQueue()
    for sym in prob:
        pq.put(sym)
    while pq.qsize() > 1:
        node1, node2 = pq.get(), pq.get()
        combined = HuffmanNode(node1, node2)
        pq.put((node1[0] + node2[0], combined))
    return pq.get()

root = create_tree(prob)

codes = {}
def generate_codes(node, prefix=""):
    if isinstance(node[1], HuffmanNode):
        generate_codes(node[1].left, prefix + "0")
        generate_codes(node[1].right, prefix + "1")
    else:
        codes[node[1]] = prefix
        return 

generate_codes(root)

average_codeword_length = 0
for sym in prob:
    print(sym[1], '{:6.2f}'.format(sym[0]), codes[sym[1]])
    average_codeword_length += sym[0] * len(codes[sym[1]])
print('Average codeword length is', average_codeword_length)

entropy = 0
for sym in prob:
    entropy -= sym[0] * math.log(sym[0], 2)
print('Source entropy is {:.2f}'.format(entropy))
