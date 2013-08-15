#!/usr/bin/env python2
"""Ordjakt

A simple script to cheat at the mobile phone game Ordjakten.

Usage:
  ./ordjakt.py [options] [<letters>]

Options:
  -h --help             Show this screen.
  -v --version          Show version.
  -d --dict=<filename>  Specify dictionary file to use. [default: ./dicts/sv_SE.dic]
  -n --count=<n>        Only show n number of matches.
  -l --length=<length>  Max word length.

"""
import sys
import re
import string
import docopt

def main(args):
    words = read_words(args['--dict'])
    max_length = int(args['--length'] or sys.maxint)
    words = filter(lambda word: len(word) <= max_length, words)
    pattern = make_pattern(args['<letters>'] or '.')
    matches = filter(lambda word: pattern.match(word), words)
    count = int(args['--count'] or 0)
    print('\n'.join(matches[-count:]).encode('utf-8'))

def read_words(filename):
    with open(filename, 'rb') as f:
        lines = f.read().decode('utf-8').split('\n')
        words = map(sanitize, lines)
        words = filter(unicode.isalpha, words)
        return sorted(words, cmp=by_length)

def sanitize(line):
    return line.split('/')[0].lower()

def by_length(a, b):
    return len(a) - len(b)

def make_pattern(letters):
    letters = letters.decode('utf-8')
    return re.compile('^' + ''.join([c + ".*" for c in letters]))

if __name__ == "__main__":
    args = docopt.docopt(__doc__, version='Ordjakt 1.0.0')
    main(args)
