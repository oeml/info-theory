import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='Source file')
parser.add_argument('--out', help='Where to save processed file')
args = parser.parse_args()

regex = re.compile('[^ абвгдежзийклмнопрстуфхцчшщьыюя]')

with open(args.file, 'r') as f:
    contents = f.read()
    contents = contents.lower()
    contents = contents.replace('ъ', 'ь')
    contents = contents.replace('ё', 'е')
    contents = regex.sub('', contents)
 
with open(args.out, 'w') as f:
    f.write(contents)
