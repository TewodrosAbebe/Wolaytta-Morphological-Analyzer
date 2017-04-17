#!/usr/bin/env python3
#wol-gof not analyzed
"""
Throughout this program, the ISO codes for Wolaytta and Gofa are used: Wal, Gof.
"""

## Initializing the system
import os
# Locations of files needed for looking up analyses, generation forms,
# and root translations
ANAL = "/home/teddy/Documents/wol-morphanal.txt" #"anal.txt"
ROOT = "/home/teddy/Documents/roottrans.txt" #"root.txt"
GEN =  "/home/teddy/Documents/gofvvgen.txt" #"gen.txt"
LEXC = "/home/teddy/Documents/lexc.txt" #"gof.lexc"
TWOL = "/home/teddy/Documents/twol.txt" #"gof.twol"
wordTrans = "/home/teddy/Documents/wordword.txt" #"word word"

# Dictionaries storing analyses, generation forms, and root translations.
# Note that genDict will not help with learning because it fails to
# give a trace of how a form is generated. Note: analDict is for
# analyzing Wal; genDict is for generating Gof.
analDict = {}
genDict = {}
rootDict = {}
# Lists storing contents of Gof lex and twol files. Later figure out how
# to organize these more efficiently, as dictionaries
goflex = []
goftwol = []

def init():
    """
    Creates Wal anal, Wal->Gof root, and Gof gen dicts.
    Should also (but it doesn't yet) read in Gofa .lexc and .twol files.
    """  
    read(ANAL, GEN, ROOT, LEXC, TWOL)
    wordDic(wordTrans)

def wordDic(wolgofpath):
    with open(wordTrans) as file:
        for line in file:
            walWord, gofWord = line.split()
            compare(walWord, gofWord)
            
def read(analpath, genpath, rootpath, lexcpath, twolpath):
    """Creates dicts analDict, genDict and rootDict and lexicon and rule lists
    from files.
    """
    with open(analpath) as file:
        for line in file:
            word, root, features = line.split()
            analDict[word] = (root, features)
    with open(genpath) as file:
        for line in file:
            root, features, word = line.split()
            genDict[root, features] = (word)
    with open(rootpath) as file:
        for line in file:
            wroot, groot = line.split()
            rootDict[wroot] = groot
    with open(lexcpath) as file:
        for line in file:
            line = line.strip()
            # Skip blank lines or lines beginning with comment char !
            if not line or line[0] == '!':
                continue
            goflex.append(line)
    with open(twolpath) as file:
        for line in file:
            line = line.strip()
            # Skip blank lines or lines beginning with comment char !
            if not line or line[0] == '!':
                continue
            goftwol.append(line)

## Top-level functions for comparing Gof words generated by system with actual Gof words.

def compare(source_word, target_word):
    """
    Input is a Wal word and its Gof translation. The system attempts to translate
    source_word into Gof to see if it matches target_word.
    """
    # trans either returns None if it fails or the results of the attempted translation
    trans_output = trans(source_word)   
    if not sys_trans:
        print("WalGof failed to translate {}".format(source_word))
        
        # Do something here...
        with open('not-analyzed.txt', 'r+') as f:
            found = False
            for line in f:
                if source_word in line: # Key line: check if `w` is in the line.
                    found = True
            if not found:
                f.write(source_word)
                f.write("\n")
                print('The translation cannot be found!')
    
        return False
    
    if sys_target_word == target_word:

        # The system's translation matches the actual translation
        print("SUCCESS")
        print("Output {} matches translation for {}".format(sys_target_word, source_word))
        w = sys_target_word, source_word
        with open('wol-gof.txt', 'r+') as f:
            found = False
            for line in f:
                if sys_target_word in line: # Key line: check if `w` is in the line.
                    found = True
            if not found:
                f.write(str(w[0]) + " " + str(w[1]))
                f.write("\n")
                print('The translation cannot be found!')
        return False

    # The system's translation fails to match the actual translation,
    # so we have a LEARNING OPPORTUNITY
    print("FAILURE")
    print("{} ≠ translation for {}: {}".format(sys_trans, source_word, target_word))
    # DO LEARNING HERE.
    # THIS REQUIRES KNOWING HOW THE GOFA WORD WAS GENERATED USING HFST RULES
    # AND LEXICON.
    # THIS IS WHERE ALL OF OUR WORK WILL BE FOR THE NEXT 6 MONTHS OR SO.
    # return True
    return learn(source_root, source_feats, sys_target_root, sys_target_word, target_word)

def learn(sys_trans, target_word):
    """This takes the system's Gofa output and an actual Gofa word, which
    are different, figures out what kind of difference this is, and ...
    """
    # Case 1: root is different
    #   return the old and new roots?
    analysis = anal(sys_trans)
    root, features = analysis
    if target_word.startswith(root):
        size = len(root)
        print("The root of Gofa word ", sys_trans, "is ", root,".")
        print("The features of Gofa suffix ", sys_trans[size:], "is ", features,".")
        
        #w = sys_trans, sys_trans[:len(root)], features
        analysis = (str(sys_trans) + " " + str(root)+ " " +  str(features))
        with open('gofanal.txt', 'r+') as f:
            found = False
            for line in f:
                if analysis in line: # Key line: check if `w` is in the line.
                    print(line)
                    found = True
            if not found:
                f.write(analysis)
                f.write("\n")
                print('The translation cannot be found!')
    
    # Case 2: suffix is different
    #   return the old and new suffixes??
    elif target_word.endswith(sys_trans[len(root):]):
        print("The root of Gofa word ", sys_trans, "is ", sys_trans[:len(root)],".")
        print("The suffix of of Gofa word ", sys_trans, "is ", sys_trans[len(root):],".")

        analysis = (str(sys_trans) + " " + str(sys_trans[:len(root)])+ " " +  str(features))
        with open('gofanal.txt', 'r+') as f:
            found = False
            for line in f:
                if analysis in line: # Key line: check if `w` is in the line.
                    print(line)
                    found = True
            if not found:
                f.write(str(w[0]) + " " + str(w[1])+ " " +  str(w[2]))
                f.write("\n")
                print('The translation cannot be found!')
        
    # Case 3: alternation rule is different
    #   We don't know how to handle these; we'll work on this later
    else:
        print("The words ", sys_trans, target_word, "needs further investigations.")
    
    return False
        
def trans(source_word):
    """
    Translates a word from Wal into Gof, according to the system's current
    knowledge. Returns None if it fails at any point.
    """
    analysis = anal(source_word)
    if analysis:
        source_root, features = analysis
        target_root = rtrans(source_root)
        if target_root:
            target_word = gen(target_root, features)
            if target_word:
                return source_root, features, target_root, target_word
            else:
                print("No word generated for {} / {}".format(target_root, features))
                
                w = target_root, features
                with open('no-word-generated.txt', 'r+') as f:
                    found = False
                    for line in f:
                        if target_root in line: # Key line: check if `w` is in the line.
                            found = True
                    if not found:
                        f.write(str(w[0]) + " " + str(w[1]))
                        f.write("\n")
                        print('The translation cannot be found!')

        else:
            print("No translation found for root {}".format(source_root))
            
            w = target_root, features
            with open('no-word-generated.txt', 'r+') as f:
                found = False
                for line in f:
                    if target_root in line: # Key line: check if `w` is in the line.
                        print(line)
                        found = True
                if not found:
                    f.write(str(w[0]) + " " + str(w[1]))
                    f.write("\n")
                    print('The translation cannot be found!')
            return
    else:
        print("No analysis for source word {}".format(source_word))
        return

## Basic low-level functions for analyzing Wal and generating Gof words

def anal(source_word):
    """Takes a Wal word and returns a root, grammatical feature pair or None
    if there is none in analDict."""
    return analDict.get(source_word)

def gen(target_root, features):
    """Takes a Gof root and set of grammatical features and returns a word
    or None if there is none in the genDict."""
    return genDict.get((target_root, features))

def rtrans(source_root):
    """Takes a Wal root and returns a Gof root, or None if there is none
    in rootDict."""
    return rootDict.get(source_root)

if __name__ == "__main__":
    print("This is WalGof, a program that learns Gofa morphology from Wolaytta morphology.")
    print("Version 0.1.")
    init()