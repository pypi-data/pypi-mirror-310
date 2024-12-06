#!python
import sys
import argparse
from . import csv_deserialize, csv_serialize
from . import json_deserialize, json_serialize

parser = argparse.ArgumentParser(
    description='A bit of extra help to transform stuff in the command line',
    epilog='Your feedback is appreciated: https://github.com/andyil/retx')

parser.add_argument('-i', '--input', action='store', nargs='*', default=['stdin'])
parser.add_argument('-o', '--output', action='store', default='stdout', nargs='?')
parser.add_argument('-c', '--cmd', action='store', choices=('j2c', 'c2j'))


i = parser.parse_args()
cmd = i.cmd
if cmd == 'j2c':
    serializer = csv_serialize
    deserializer = json_deserialize

else: #cmd == 'c2j'
    serializer = json_serialize
    deserializer = csv_deserialize

if i.output == 'stdout':
    outfile = sys.stdout
elif i.output == 'stderr':
    outfile = sys.stderr
else:
    outfile = open(i.output, 'w')

for inp in i.input:
    if inp == 'stdin':
        s = sys.stdin
    else:
        s = open(inp, 'r')
    serializer(deserializer(s), outfile)


