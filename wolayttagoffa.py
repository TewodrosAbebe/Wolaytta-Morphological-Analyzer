gofDict = {}
exceptionWord = []
analDict = {}
genDict = {}
rootDict = {}
wordDict = {}

def anal(): # Reads word word dictionary of Wal:Gof until end
    for ww, gw in wordDict.items():
        if ww == gw:
            # for key, feature in analDict.items():
            if ww in analDict:
                feature = analDict[ww]
                print("The Morphological Analysis of the word ", ww, "is ", feature)
                rGof = rDict(feature[0])
                wordGoffa = gen(rGof, feature[1])
                if gw == wordGoffa:
                    print("The Wolaytta word", ww, " and Goffa word ", gw, " are equivalent")
                    print("The analysis of the Goffa word ", gw, "is ", feature)
            else:
                print("The Wolaytta Morphological Analyzer doesn't analyze the word ", ww)
        else:
            for key, feature in analDict.items():
                if key == ww:
                    print("The two words ( ", ww,gw, ") are different.")
                    if gw.startswith(feature[0]):
                        print("The root of ", gw, "is ", feature[0])
                        print("The analysis of ", gw, "is", feature)
                    elif gw.endswith(ww[3:]):
                        print("The words ", ww, gw, "have the similar suffixes.")                     
                        print("The suffix of ", gw , "is ",ww[3:] )
                        print("The analysis of goffa word ", gw, "is", gw[:3],feature[1])
                    else:
                        pass
                else:
                    pass
                                                                             
    wolWor = (input("please insert Wolaytta word  "))
    gofWor = (input("please insert Goffa equivalent of word  "))
    exceptionWord.append(wolWor)
    exceptionWord.append(gofWor)
    b = suffixIdentifier(exceptionWord)
    rootIdentifier(exceptionWord)
                     
"""def rootIdentifier(l):
    root = ""
    for t in zip(*l):
        if not all(t[0] == s for s in t):
            break
        root += t[0]
    ln = len(root)
    pres = [s[ln:] for s in exceptionWord]
    print(root)"""
    
def suffixIdentifier(l):
    sufLet=""
    revList=[]
    for word in l:
        revList.append(word[::-1])
    for ltr in zip(*revList):
        if not all(ltr[0] == s for s in ltr):
            break
        sufLet+=ltr[0]
    ln = len(sufLet)
    for word in l:
        print("The Suffix of", word, "is  ",word[-ln:])
      
def rDict(root):
    for k, m in rootDict.items():    # k = Walaytta Root m = Goffa Root
        if root==m:
            print("The root translation of", root, "is ", k)
            return k
        
def gen(root, feature):
    for key, l in genDict.items():
        #print(root, key[0], feature, key[1])
        if root==key[0] and feature==key[1]:
            return(l)
    
def read(path1, path2):    # Reads the Wolaytta MA file and creat dictionary of analDict, genDict and rootDict
    with open(path1) as file:
        for line in file:
            word, root, features = line.split()
            analDict[word] = (root, features)
            genDict[(root, features)] = word
            rootDict[root] = (root)
        
    with open(path2) as file:
        for line in file:
            wolWor, gofWor = line.split()
            wordDict[wolWor] = gofWor
        #print(wordDict)
    
def write():
    with open("/home/tewodros/Desktop/GoffaDict", 'w') as file:
        for word, (root, features) in analDict.items():
            print("{} {} {}".format(word, root, features), file=file)       
   
def main():
    read("/home/tewodros/Desktop/wol-morphanal", "/home/tewodros/Desktop/wordword")
    #acceptWolEqu(analdict, gendict)
    anal()
main()
