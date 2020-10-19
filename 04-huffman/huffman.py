import queue
import itertools
import math

class Huffman(object):
    def __init__(self, prob):
        self.prob = prob
        self.codes = self._get_huffman_codes()

    class HuffmanNode(object):
        def __init__(self, left=None, right=None):
            self.left = left
            self.right = right
    
        def get_children(self):
            return (self.left, self.right)
    
    def _get_huffman_codes(self):
        pq = queue.PriorityQueue()
        tiebreaker = itertools.count()
        for sym in self.prob:
            pq.put((sym[0], next(tiebreaker), sym[1]))
        while pq.qsize() > 1:
            node1, node2 = pq.get(), pq.get()
            combined = self.HuffmanNode(node1, node2)
            pq.put((node1[0] + node2[0], next(tiebreaker), combined))
        root = pq.get()
        
        codes = {}
        def generate_codes(node, prefix=""):
            if isinstance(node[2], self.HuffmanNode):
                generate_codes(node[2].left, prefix + "0")
                generate_codes(node[2].right, prefix + "1")
            else:
                codes[node[2]] = prefix
                return 
        
        generate_codes(root)
        return codes
    
    def entropy(self):
        entropy = 0
        for sym in self.prob:
            entropy -= sym[0] * math.log(sym[0], 2)
        return entropy

    def average_code_len(self):
        average = 0
        for sym in self.prob:
             average += sym[0] * len(self.codes[sym[1]])
        return average
    
    def encode(self, text, outfile):
        to_write = []
        curr_byte = ''
        leftover = ''
        for sym in text:
            curr_sym = leftover + self.codes[sym]
            leftover = ''
            sym_len = len(curr_sym)
            curr_byte_cap = 8 - len(curr_byte)
            if curr_byte_cap > sym_len:
                curr_byte += curr_sym
            else:
                if curr_byte_cap < sym_len:
                    leftover = curr_sym[curr_byte_cap:]
                    curr_sym = curr_sym[:curr_byte_cap]
                curr_byte += curr_sym
                to_write.append(int(curr_byte,2))
                curr_byte = ''
                                            
        bytes_to_write = bytes(to_write)
        with open(outfile, 'wb') as f:
            f.write(bytes_to_write)
