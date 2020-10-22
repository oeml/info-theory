import argparse
import itertools
import math

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='File to compress')
args = parser.parse_args()

with open(args.file, 'r') as f:
    contents = f.read()

orig_len = len(contents) * 8
print('Total length of original text in bits = {}'.format(orig_len))

code = itertools.count()
phrases = {}
phrases[''] = next(code)
i = 0
while i < len(contents):
    s = contents[i]
    while s in phrases and i < len(contents) - 1:
        i += 1
        s += contents[i]
    phrases[s] = next(code)
    i += 1

last_code = next(code) - 1
codeword_len = len(bin(last_code)[2:])

def to_binary(val, size):
    tail = bin(val)[2:]
    leading_zeroes = '0' * (size - len(tail))
    return leading_zeroes + tail

def char_to_bin(char):
    byte = char.encode('cp1251')[0]
    return to_binary(byte, 8)

for (s, code) in phrases.items():
    phrases[s] = to_binary(code, codeword_len)

encoded = set()
res = ''
i = 0
while i < len(contents):
    s = contents[i]
    while s in encoded and i < len(contents) - 1:
        i += 1
        s += contents[i]
    encoded.add(s)
    curr_code = phrases[s[:-1]] + char_to_bin(s[-1])
    res += curr_code
    i += 1

print('Total length of encoded text = {}'.format(len(res)))
print('1 bit of original takes up {:1.2f} bits in encoded'.format(len(res) / orig_len))

print('c(n) = {}'.format(len(phrases)))
print('n / log(n) = {:1.2f}'.format(len(contents) / math.log(len(contents),32)))
