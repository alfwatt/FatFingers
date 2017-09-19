#!/usr/bin/python

#
# FatFingers a word-list generator which will generate variations of a given string with
# typos you might accidnetaly make if you have fat fingers
#

import sys

# TODO add special values for
#
# DELETE = -1 # removes a character in the string
# CAPS_LOCK = 1 # change the remaning characters to ALL CAPS
#
# N.B. this was generated from an Apple Keybard, YKBMV
#
quertyKeyNeighbors = {
    #row 1
    '`':  ['1', '\t'],
    '1':  ['`', '2', '\t', 'q'],
    '2':  ['1', '3', 'q', 'w'],
    '3':  ['2', '4', 'w', 'e'],
    '4':  ['3', '5', 'e', 'r'],
    '5':  ['4', '6', 'r', 't'],
    '6':  ['5', '7', 't', 'y'],
    '7':  ['6', '8', 'y', 'u'],
    '8':  ['7', '9', 'u', 'i'],
    '9':  ['7', '0', 'i', 'o'],
    '0':  ['9', '-', 'o', 'p'],
    '-':  ['0', '=', 'p', '['],
    '+':  ['-', '[', ']'], # DELETE
    # row 2
    '\t': ['`', '1', 'q', 'a'],
    'q':  ['1', '2', 'w', 'a'],
    'w':  ['2', '3', 'q', 'e', 'a', 's'],
    'e':  ['3', '4', 'w', 'r', 's', 'd'],
    'r':  ['4', '5', 'e', 't', 'd', 'f'],
    't':  ['5', '6', 'r', 'y', 'f', 'g'],
    'y':  ['6', '7', 't', 'u', 'g', 'h'],
    'u':  ['7', '8', 'y', 'i', 'h', 'j'],
    'i':  ['8', '9', 'u', 'o', 'j', 'k'],
    'o':  ['9', '0', 'i', 'p', 'k', 'l'],
    'p':  ['0', '-', 'o', '[', 'l', ';'],
    '[':  ['-', '=', 'p', ']', ';', '\'', '\n'], # DELETE
    ']':  ['=', '[', '\\', '\'', '\n'], # DELETE
    '\\': [']', '\n'], # DELETE
    # row 3
    'a':  ['q', 'w', 's', '', 'z'], # CAPS_LOCK
    's':  ['w', 'e', 'a', 'd', 'z', 'x'],
    'd':  ['e', 'r', 's', 'f', 'x', 'c'],
    'f':  ['r', 't', 'd', 'g', 'c', 'v'],
    'g':  ['t', 'y', 'f', 'h', 'v', 'b'],
    'h':  ['y', 'u', 'g', 'j', 'b', 'n'],
    'j':  ['u', 'i', 'h', 'k', 'n', 'm'],
    'k':  ['i', 'o', 'j', 'l', 'm', ','],
    'l':  ['o', 'p', 'k', ';', ',', '.'],
    ';':  ['p', '[', 'l', '\\', '.', '/'],
    '\'': ['[', ']', ';', '\n', '/'], # DELETE
    # row 4
    'z':  ['a', 's', '', 'x'],
    'x':  ['s', 'd', 'z', 'c', ' '],
    'c':  ['d', 'f', 'x', 'v', ' '],
    'v':  ['f', 'g', 'c', 'b', ' '],
    'b':  ['g', 'h', 'v', 'n', ' '],
    'n':  ['h', 'j', 'b', 'm', ' '],
    'm':  ['j', 'k', 'n', ',', ' '],
    ',':  ['k', 'l', 'm', '.', ' '],
    '.':  ['l', ';', ',', '/'],
    '/':  [';', '\'', ',', '/'],
    # row 5
    ' ':  ['x', 'c', 'v', 'b', 'n', 'm'],
}

quertyKeyShiftPairs = {
    #row 1
    '`':  '~',
    '1':  '!',
    '2':  '@',
    '3':  '#',
    '4':  '$',
    '5':  '%',
    '6':  '^',
    '7':  '&',
    '8':  '*',
    '9':  '(',
    '0':  ')',
    '-':  '_',
    '+':  '=',
    # row 2
    '\t': '',
    'q':  'Q',
    'w':  'W',
    'e':  'E',
    'r':  'R',
    't':  'T',
    'y':  'Y',
    'u':  'U',
    'i':  'I',
    'o':  'O',
    'p':  'P',
    '[':  '{',
    ']':  '}',
    '\\': '|',
    # row 3
    'a':  'A',
    's':  'S',
    'd':  'D',
    'f':  'F',
    'g':  'G',
    'h':  'H',
    'j':  'J',
    'k':  'K',
    'l':  'L',
    ';':  ':',
    '\'': '"',
    # row 4
    'z':  'Z',
    'c':  'C',
    'x':  'X',
    'v':  'V',
    'b':  'B',
    'n':  'N',
    'm':  'M',
    ',':  '<',
    '.':  '>',
    '/':  '?',
    # row 5
    ' ':  ' '
}

def duplicateKeyGenerator( string=''):
    index = 0;
    while index < len(string):
        next = index + 1
        char =   string[index]
        prefix = string[:index]
        suffix = string[next:]
        doubled = prefix + char + char + suffix
        index = next
        yield doubled

def reverseAndMergeShiftPairs(shiftPairs=quertyKeyShiftPairs):
   pairKeys = shiftPairs.keys()
   mergedMap = shiftPairs.copy()
   for key in pairKeys:
       value = shiftPairs[key]
       mergedMap[value] = key
   return mergedMap

# generator for shift-swapping each character in the string
def shiftSwapGenerator( string='', shiftMap=quertyKeyShiftPairs):
    mergedMap = reverseAndMergeShiftPairs( quertyKeyShiftPairs)
    index = 0;
    while index < len(string):
        next = index + 1
        char = string[index]
        shifted = mergedMap[char]
        swapped = string[:index] + shifted + string[next:]
        index = next
        yield swapped

# generator for pair swapping each character in the string
def pairSwapGenerator( string=''):
    index = 0;
    while index < (len(string) - 1):
        next = index + 1
        swapped = string[:index] + string[next] + string[index] + string[next + 1:];
        index = next
        yield swapped

def shiftAndMergeNeighorKeys(neighborMap=quertyKeyNeighbors, shiftMap=quertyKeyShiftPairs):
    mergedShiftMap = reverseAndMergeShiftPairs(shiftMap)
    neighborKeys = neighborMap.keys()
    mergedMap = neighborMap.copy()
    for key in neighborKeys:
        shifted = mergedShiftMap[key]
        mergedMap[shifted] = neighborMap[key]
    return mergedMap

def neighborSwapGenerator( string='', neighborMap=quertyKeyNeighbors):
    mergedMap = shiftAndMergeNeighorKeys(neighborMap)
    index = 0;
    while index < len(string):
        next = index + 1
        prefix = string[:index]
        suffix = string[next:]
        char = string[index]
        for near in mergedMap[string[index]]:
            swapped = prefix + near + suffix
            yield swapped
        index = next;

def printUsage():
    print 'FatFingers.py -p -s "string"'
    print '  -d -- key duplicates: double each character in the string'
    print '  -p -- pair swapping: swap each character pair in the string'
    print '  -s -- shift swapping: shift each caracter in the string (e.g. \'a\' > \'A\')'
    print '  -n -- neighbor swapping: replace each character in the string with each near key'

#
# FatFingers.py -- genearte a word list of typos based on neighrest neighbor and shift pairing
#
#   TODO:
#
#    -d -- double each letter in the sequence
#    -N -- drunken neighbor swapping: iterate two levels of key neighbors
#
if __name__ == '__main__':
    dupeKeys = False
    swapPairs = False
    swapShift = False
    swapNear = False
    string = sys.argv[-1]
    # print 'argv: %s string: %s' % (sys.argv, string)

    if (len(sys.argv) < 3):
        printUsage()
        sys.exit(2)
    
    # read the arguments into booleans
    if '-d' in sys.argv:
        dupeKeys = True
    
    if '-p' in sys.argv:
        swapPairs = True
        
    if '-s' in sys.argv:
        swapShift = True

    if '-n' in sys.argv:
        swapNear = True

    # TODO combinaions

    if dupeKeys:
        dupes = duplicateKeyGenerator(string)
        while True:
            try:
                print dupes.next()
            except StopIteration:
                break

    if swapPairs:
        # print '-p %s' % (string)
        swapper = pairSwapGenerator(string)
        while True:
            try:
                print swapper.next()
            except StopIteration:
                break

    if swapShift:
        # print '-s %s' % (string)
        shifter = shiftSwapGenerator(string)
        while True:
            try:
                print shifter.next()
            except StopIteration:
                break

    if swapNear:
        #print '-n %@' % (string)
        neighbor = neighborSwapGenerator(string)
        while True:
            try:
                print neighbor.next()
            except StopIteration:
                break
