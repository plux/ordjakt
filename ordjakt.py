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
  -p --palindrome       Find palindromes.

"""
import sys
import re
import string
import docopt

def main(args):
    words = read_words(args['--dict'])
    pattern = make_pattern(args['<letters>'] or '.')
    matches = filter(pattern.match, words)
    matches = custom_filter_matches(args, matches)
    print('\n'.join(matches).encode('utf-8'))

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

def custom_filter_matches(args, matches):
    if args['--length']:
        matches = filter(lambda m: len(m) <= int(args['--length']), matches)
    if args['--palindrome']:
        matches = filter(is_palindrome, matches)
    if args['--count']:
        matches = matches[-int(args['--count']):]
    return matches

def is_palindrome(word):
    return word == word[::-1]

if __name__ == "__main__":
    args = docopt.docopt(__doc__, version='Ordjakt 1.1.0')
    main(args)
