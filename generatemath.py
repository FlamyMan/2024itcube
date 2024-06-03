import random
# import sympy as sp
from data.examples import Examples

# constants
opstring = "+-*/"

def radicalListToString(radicalList : list) -> str:
    radicalList.reverse()
    string = ""
    # print(radicalList)
    lastPriority = 10000
    for i in radicalList:
        order = random.randint(0, 1)
        if (type(i[1]) == list):
            i[1] = f"({radicalListToString(i[1])})"
        match i[0]:
            case -1:
                string = f"{i[1]}"
            case 0:
                string = f"{string}+{i[1]}" if order else f"{i[1]}+{string}"
                lastPriority = 0
            case 1:
                string = f"{string}-{i[1]}"
                lastPriority = 0
            case 2:
                if lastPriority >= 1:
                    string = f"{string}*{i[1]}" if order else f"{i[1]}*{string}"
                else:
                    string = f"({string})*{i[1]}" if order else f"{i[1]}({string})"
                lastPriority = 1
            case 3:
                string = f"{string}/{i[1]}" if lastPriority >= 1 else f"({string})/{i[1]}"
                lastPriority = 1
    return string
    
def linearizeRadicalList(radicalList : list, currentIndex : list = [0,]) -> list:
    output = []
    curIdx = currentIndex.copy()
    for elem in radicalList:
        if type(elem[1]) == int:
            output.append([elem[0], elem[1], curIdx.copy()])
        elif type(elem[1]) == list or type(elem[1]) == tuple:
            tmpIdx = curIdx.copy()
            tmpIdx.append(0)
            output += linearizeRadicalList(elem[1], tmpIdx)
        curIdx[-1] += 1
    return output

def generateEquationInternal(radicalAmount : int, featureToggles : list = (True, True, True, True), recursiveAmount : list = (0, 0), xLimits : tuple = (0, 100), coefLimits : tuple = (0, 100), subXLimits : tuple = (1, 100)):

    features = [i for i in range(len(featureToggles)) if featureToggles[i]]
    if len(features) == 0:
        return

    x : int = random.randint(xLimits[0], xLimits[1])
    subX : int = x
    radicalList = []
    radicalNum = radicalAmount - 1
    lastElem = -1
    while (radicalNum > 0):
        coefficient = random.randint(coefLimits[0], coefLimits[1])
        action = random.choice(features)
        match action:   # addition
            case 0:
                if (subX < subXLimits[0]):  # we can't fucking subtract any more m8
                    continue
                while (subX - coefficient < subXLimits[0]):
                    coefficient = int(coefficient // random.uniform(0.4, 4))
                if (coefficient == 0):
                    continue
                subX -= coefficient
            case 1: # subtraction
                if (subX > subXLimits[1]):  # we can't fucking add any more m8
                    continue
                while (subX + coefficient > subXLimits[1]):
                    coefficient = int(coefficient // random.uniform(0.4, 4))
                if (coefficient == 0):
                    continue
                subX += coefficient
            case 2: # multiplication
                if (subX < subXLimits[0]):  # we can't fucking divide any more m8
                    continue
                coefficients = []
                for i in range(coefLimits[0], coefLimits[1]+1):
                    if i == 0 or i == 1 or i == subX or i == lastElem or subX // i < subXLimits[0] or subX // i > subXLimits[1]:
                        continue
                    if (subX % i == 0):
                        coefficients.append(i)
                if (len(coefficients) == 0):
                    continue
                diff = [coefficient-i for i in coefficients]
                diff = diff.index(min(diff))
                coefficient = coefficients[diff]
                subX = int(subX // coefficient)
            case 3: # division
                if (subX > subXLimits[1] or subX == 0 or subX == 1):  # we can't fucking multiply any more m8
                    continue
                # the coefficient gotta stay below (subXLimits[1] / subX)
                if (subXLimits[1] / subX == 1 or subXLimits[1] / subX == 0):
                    continue
                attCount = 0
                while (coefficient > subXLimits[1] / subX or coefficient == 1 or coefficient == 0 or coefficient == subX):
                    coefficient = random.randint(subXLimits[0], int(subXLimits[1] / subX))
                    attCount += 1
                    if attCount > 20:
                        break    # fuck this shit
                if attCount > 20:
                    continue
                subX *= coefficient
            
        radicalList.append([action, coefficient]) 
        lastElem = coefficient
        radicalNum -= 1

    for recurCounter in range (recursiveAmount[0]):
        # print(f"A: {radicalList}")
        linearRadicalList = linearizeRadicalList(radicalList)
        oldExpr = random.choice(linearRadicalList)
        # print(f"B: {oldExpr}")
        newExpr = generateEquationInternal(recursiveAmount[1], featureToggles, (0, 0), (oldExpr[1], oldExpr[1]), coefLimits, subXLimits)
        # print(f"C: {newExpr}")
        listRef = radicalList
        for i in oldExpr[2]:
            listRef = listRef[i]
            if len(listRef) == 2 and type(listRef[0]) == int and type(listRef[1]) == list:
                listRef = listRef[1]
            # print(f"L: {listRef}")
        listRef[1] = newExpr[0]
        # print(f"D: {radicalList}\n\n")
        
    radicalList.append([-1, subX])
    
    return radicalList, x

def generateExpression(outputOfGEI : list) -> str:
    return f"{radicalListToString(outputOfGEI[0])} = {outputOfGEI[1]}"

if __name__ == "__main__":
    print(generateExpression(generateEquationInternal(5, (True, True, True, True), (3, 2))))
