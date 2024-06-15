import sys;args = sys.argv[1:]
import time

possibleChoices = [*'123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ']

global allLens
global return1
global return2
global solveReturn

data = {'invTrue': 0, 'invFalse': 0, 'isSolved': 0, 'pzl afer solved': 0, 'createDst': 0, 'findMin': 0, 'bfr1': 0, 'bfr2': 0}
OneOrMoreChoices = {'one':0, 'more':0, 'redirected': 0, 'failed': 0, 'timeInDual': 0}
choiceCounts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

#debug = {"bruteForce": 0, "IsInvalid": 0, "collectively exhausted": 0}

def setGlobals(pzl):
    global n
    global choiceSet
    global ConstrLookup
    global ConstraintDict
    global Neighbors

    n = int(len(pzl) ** 0.5)

    width = int(n**0.5)
    length = min([n//i for i in range(width, 0, -1) if n%i==0])

    choiceSet = {*pzl.replace('.', '')}
    i = 0
    while len(choiceSet) < n:
        if not possibleChoices[i] in choiceSet:
            choiceSet.add(possibleChoices[i])
        i+= 1

    ConstrLookup = [{i for i in range(n * j, n * (j + 1))} for j in range(n)] + \
                   [{i for i in range(j, ((n - 1) * n + j) + 1, n)} for j in range(n)]
    for i in range(length):
        bigRectStart = n*width*i
        for rectContrStart in range(bigRectStart, bigRectStart + n, length):
            newSet = set()
            for rowStart in range(rectContrStart, rectContrStart + n*width, n):
                for idx in range(rowStart, rowStart + length):
                    newSet.add(idx)
            ConstrLookup.append(newSet)
    



    ConstraintDict = {idx: [CS for CS in ConstrLookup if idx in CS] for idx in range(n ** 2)}


    Neighbors = [set().union(*ConstraintDict[idx]) - {idx} for idx in ConstraintDict]

def isInvalid(pzl,mostRecentIdx):
    for idx in Neighbors[mostRecentIdx]:
        if pzl[idx] == pzl[mostRecentIdx]:
            return True
    return False

def findOptimalSymbol(dataStruc, pzl):
    lst = dataStruc.values()
    if not lst:
        return False
    Min = (9999, 9999, 9999)
    for tup in lst:
        if tup[0] == 1:
            return tup
        if tup[0] == 0:
            return True
        if tup[0] < Min[0]:
            Min = tup
    else:
        dualSet = createDualDst(pzl, Min, dataStruc)
        return dualSet if dualSet else Min


def isSolved(pzl):
    return pzl.count('.') == 0

def updateDS(pos, dataStruc, takenChoice):
    del dataStruc[pos]
    if dataStruc:
        for idx in Neighbors[pos]:
            if idx in dataStruc:
                tup = dataStruc[idx]
                if takenChoice in tup[1]:
                    lstOfOptions = [op for op in tup[1]]
                    lstOfOptions.remove(takenChoice)
                    dataStruc[idx] = (len(lstOfOptions), lstOfOptions, idx)

def createDataStruc(pzl):
    dst = {}
    for i in range(len(pzl)):
        if pzl[i] == '.':
            Set = [choice for choice in choiceSet if not isInvalid(''.join((pzl[0:i], choice, pzl[i + 1:])), i)]
            dst[i] = (len(Set), Set, i)
    return dst

def createOtherDataStruc(pzl, dataStruc):
    toRet = {}
    for symbol in choiceSet:
        idxSet = {idx for idx in pzl if idx in dataStruc and symbol in dataStruc[idx][1]}
        toRet[symbol] = idxSet
    return toRet
#make dict where key is symbol and value is list of indicies where it can go, then in find optimal pos
#loop through all constraintSets and if that list union w a contraintSet is one then the symbol must go there

def createDualDst(pzl, Min, dataStruc):
    for CS in ConstrLookup:
        symbolsPlaced = {pzl[idx] for idx in CS if pzl[idx] != '.'}
        for symbolYetToBePlaced in (choiceSet - symbolsPlaced):
            numSpots = [spot for spot in CS if spot in dataStruc and symbolYetToBePlaced in dataStruc[spot][1]]
            if len(numSpots) == 0:
                return True
            if len(numSpots) < Min[0]:
                return (1, symbolYetToBePlaced, numSpots)
    return ""


def findMin(dataStruc):
    lst = dataStruc.values()
    return (-1, -1) if not lst else min(lst)

def bruteForce(pzl, dataStruc):
    Min = findOptimalSymbol(dataStruc, pzl)
    if type(Min) == bool and Min:
        return ""
    if isSolved(pzl):
        return pzl
    posCho = Min[1]
    choiceCounts[len(posCho)] = choiceCounts[len(posCho)] + 1
    idx = Min[2]
    if type(idx) == list:
        choice = posCho
        for i, spot in enumerate(idx):
            if i == len(idx) - 1:
                copyStruc = dataStruc
            else:
                copyStruc = {key: dataStruc[key] for key in dataStruc.keys()}
            updateDS(spot, copyStruc, choice)
            subPzl = ''.join((pzl[0:spot], choice, pzl[spot + 1:]))
            bF = bruteForce(subPzl, copyStruc)
            if bF: return bF
    else:
        for i, choice in enumerate(posCho):
            if i == len(posCho) - 1:
                copyStruc = dataStruc
            else:
                copyStruc = {key: dataStruc[key] for key in dataStruc.keys()}
            updateDS(idx, copyStruc, choice)
            subPzl = ''.join((pzl[0:idx], choice, pzl[idx + 1:]))
            bF = bruteForce(subPzl, copyStruc)
            if bF: return bF
    return ""

def main():
    import time
    asciiTable = {'0':48, '1':49, '2':50, '3':51, '4':52, '5':53, 
    '6':54, '7':55, '8':56, '9':57, 'A':65, 'B':66, 'C':67, 'D':68, 
    'E':69, 'F':70, 'G':71, 'H':72, 'I':73, 'J':74, 'K':75, 'L':76, 
    'M':77, 'N':78, 'O':79, 'P':80, 'Q':81, 'R':82, 'S':83, 'T':84, 
    'U':85, 'V':86, 'W':87, 'X':88, 'Y':89, 'Z':90}
    # fix ascii table at some point so that it accounts for all possible char combo possibilities
    totalStartTime = time.time()
    with open('data/puzzlesLarge.txt') as file:
        sudokuLst = [line.strip() for line in file]
        for idx,sd in enumerate(sudokuLst):
            startTime = time.time()
            setGlobals(sd)
            dt = createDataStruc(sd)
            solved = bruteForce(sd, dt)
            realTime = time.time() - startTime
            Time = f"{realTime}s"[0:4] + "s"
            minA = min([asciiTable[key] for key in asciiTable if key in solved])
            checksum = sum([asciiTable[num] - minA for num in solved])
            print(str(idx+1)+":", sd)
            print(' '*(1+len(str(idx+1))), solved, checksum, Time)
    print('count for # of choices', choiceCounts)
    print('# of times dualSet was used:', OneOrMoreChoices['timeInDual'])
    TotalTime = f"{time.time() - totalStartTime}s"[0:4] + "s"
    print('total time', TotalTime)
if __name__== "__main__": main()
# Akash Wudali, pd.4, 2024