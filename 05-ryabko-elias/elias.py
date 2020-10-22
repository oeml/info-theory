import argparse
import itertools
import math

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='File to compress')
parser.add_argument('--kmin', help='Minimum value of k to test')
parser.add_argument('--kmax', help='Maximum value of k to test')
args = parser.parse_args()

class RyabkoElias(object):
    def __init__(self, k):
        self.phrases = [''.join(seq) for seq in itertools.product('01', repeat=k)]

    def _with_prefix(self,n):
        l_n = int(math.log(n,2))
        prefix = '0' * l_n
        return prefix + bin(n)[2:]

    def _elias(self, phrase):
        n = self.phrases.index(phrase)+1
        l_n = int(math.log(n,2))+1
        encoded =  self._with_prefix(l_n) + bin(n)[3:]
        return encoded
    
    def encode_phrase(self, phrase):
        code = self._elias(phrase)
        self.phrases.remove(phrase)
        self.phrases.insert(0,phrase)
        return code

with open(args.file, 'r') as f:
    contents = bytes(f.read(), 'CP1251')

bitstring = ''
for byte in contents:
    bits = bin(byte)[2:]
    leading_zeroes = '0' * (8 - len(bits))
    bitstring += leading_zeroes + bits

averages = []
for k in range(int(args.kmin), int(args.kmax)+1):
    rem = len(bitstring) % k
    if rem != 0:
        trailing_zeroes = '0' * (k - rem)
        bitstring += trailing_zeroes
    phrases = [bitstring[i*k : (i+1)*k]
               for i in range(len(bitstring) // k)]
    
    ryabko_elias = RyabkoElias(k)
    res = ''
    for phrase in phrases:
        code = ryabko_elias.encode_phrase(phrase)
        res += code
    
    average_code_len = len(res) / len(phrases) / k
    averages.append(average_code_len)
    print('for k = {} average code length = {:1.2f}'.format(k, average_code_len))

with open('codelen.csv','w') as f:
    for val in averages:
        f.write(str(val) + '\n')
