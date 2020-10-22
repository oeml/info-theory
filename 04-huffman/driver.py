from huffman import Huffman

import argparse
import re
import math
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='File to compress')
parser.add_argument('--out1', help='Where to save file compressed based on frequency of letters in language in general')
parser.add_argument('--out2', help='Where to save file compressed based on frequencies of letters in that particular file')
parser.add_argument('--out3', help='Where to save file compressed based on frequencies of pairs of letters in that particular file')
args = parser.parse_args()

regex = re.compile('[^ абвгдежзийклмнопрстуфхцчшщьыюя]')

with open(args.file, 'r') as f:
    contents = f.read()
    contents = contents.lower()
    contents = contents.replace('ъ', 'ь')
    contents = contents.replace('ё', 'е')
    contents = regex.sub('', contents)
    
prob = [(0.175,' '), (0.090,'о'), (0.072,'е'), (0.062,'а'),
        (0.062,'и'), (0.053,'т'), (0.053,'н'), (0.045,'с'), 
        (0.040,'р'), (0.038,'в'), (0.035,'л'), (0.028,'к'), 
        (0.026,'м'), (0.025,'д'), (0.023,'п'), (0.021,'у'),
        (0.018,'я'), (0.016,'ы'), (0.016,'з'), (0.014,'ь'), 
        (0.014,'б'), (0.013,'г'), (0.012,'ч'), (0.010,'й'),
        (0.009,'х'), (0.007,'ж'), (0.006,'ю'), (0.006,'ш'),
        (0.004,'ц'), (0.003,'щ'), (0.003,'э'), (0.002,'ф')]

huffman_general = Huffman(prob)
huffman_general.encode(contents, args.out1)
print('Source entropy based on letter probabilities is {:1.2f}'.format(huffman_general.entropy()))
print('Average codeword length is {:1.2f}'.format(huffman_general.average_code_len()))

freq = {}
for sym in contents:
    if sym not in freq:
        freq[sym] = 1
    else:
        freq[sym] += 1

text_prob = []
for sym,freq in freq.items():
    text_prob.append((freq/len(contents), sym))

huffman_from_text = Huffman(text_prob)
huffman_from_text.encode(contents, args.out2)
print('Source entropy based on letter probabilities is {:1.2f}'.format(huffman_from_text.entropy()))
print('Average codeword length is {:1.2f}'.format(huffman_from_text.average_code_len()))

prob_dict = {sym:freq for freq,sym in prob}
relative_entropy = 0
for f_x,x in text_prob:
    g_x = prob_dict[x]
    relative_entropy += f_x * math.log(f_x / g_x)
print('Relative entropy is {:1.2f}'.format(relative_entropy))

freq = {}
as_pairs = [contents[i*2:(i+1)*2] for i in range(len(contents) // 2)]
for pair in as_pairs:
    if pair not in freq:
        freq[pair] = 1
    else:
        freq[pair] += 1

pair_prob = []
for pair,freq in freq.items():
    pair_prob.append((freq/len(as_pairs), pair))

huffman_pairs = Huffman(pair_prob)
huffman_pairs.encode(as_pairs, args.out3)
print('Source entropy based on pair probabilities is {:1.2f}'.format(huffman_pairs.entropy()))
print('Average codeword length is {:1.2f}'.format(huffman_pairs.average_code_len()))
