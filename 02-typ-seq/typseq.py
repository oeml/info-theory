import argparse
import math
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('--n', help='Sequence length')
parser.add_argument('--eps', help='Epsilon')
parser.add_argument('-v', action='store_true', help='Print all sequences')
args = parser.parse_args()

n = int(args.n)
eps = float(args.eps)

p = 1/3
h_x = -p * math.log(p,2) - (1-p) * math.log(1-p,2)
print('Entropy H(X) = {:1.2f}'.format(h_x))

seqs = [''.join(seq) for seq in itertools.product('01', repeat=n)]
if args.v:
    print('All sequences = {}'.format(seqs))

prob_lower = math.pow(2, -n * (h_x + eps))
prob_upper = math.pow(2, -n * (h_x - eps))
print('f(x_) is between {:1.5f} and {:1.5f}'.format(prob_lower, prob_upper))

black_lower = int(math.ceil(n * (p - eps)))
black_upper = int(math.floor(n * (p + eps)))
typ_seqs = [seq for seq in seqs 
            if seq.count('1') >= black_lower and seq.count('1') <= black_upper]
if args.v:
    print('Typical sequences = {}'.format(typ_seqs))
print('Number of typical sequences = {}, {:1.2f} of all sequences'.format(
      len(typ_seqs), len(typ_seqs)/len(seqs)))
prob_sum = 0
for t in range(black_lower, black_upper+1):
    prob_t = math.pow(p,t) * math.pow(1-p,n-t)
    n_typ_seq = sum(1 for seq in typ_seqs if seq.count('1') == t)
    prob_sum += prob_t * n_typ_seq
print('Total probability of typical sequences = {:1.2f}'.format(prob_sum))

card_t_eps_x_lower = (1-eps) * math.pow(2, n * (h_x-eps))
card_t_eps_x_upper = math.pow(2, n * (h_x+eps))
print('cardTeps(X) is between {:1.2f} and {:1.2f}'.format(card_t_eps_x_lower, card_t_eps_x_upper))
