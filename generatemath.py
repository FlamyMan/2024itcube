import random, math
import time
# import sympy as sp
from data.examples import Example

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

def generateExpressionInternal(radicalAmount : int, featureToggles : list = (True, True, True, True), recursiveAmount : list = (0, 0), equationMode : bool = False, xLimits : tuple = (0, 100), coefLimits : tuple = (0, 100), subXLimits : tuple = (0, 100)):

    initTime = time.time_ns()

    features = [i for i in range(len(featureToggles)) if featureToggles[i]]
    if len(features) == 0:
        return

    x : int = random.randint(xLimits[0], xLimits[1])
    subX : int = x
    radicalList = []
    radicalNum = radicalAmount - 1
    lastElem = -1
    while (radicalNum > 0 and time.time_ns() - initTime < 500000000):
        coefficient = random.randint(coefLimits[0], coefLimits[1])
        action = random.choice(features)
        match action:   # addition
            case 0:
                if (subX < subXLimits[0]):  # we straight up can't subtract any more m8
                    continue
                while (subX - coefficient < subXLimits[0]):
                    coefficient = int(coefficient // random.uniform(0.4, 4))
                if (coefficient == 0 or subX - coefficient == 0):
                    continue
                subX -= coefficient
            case 1: # subtraction
                if (subX > subXLimits[1]):  # we straight up can't add any more m8
                    continue
                while (subX + coefficient > subXLimits[1]):
                    coefficient = int(coefficient // random.uniform(0.4, 4))
                if (coefficient == 0 or subX + coefficient == 0):
                    continue
                subX += coefficient
            case 2: # multiplication
                if (subX < subXLimits[0]):  # we straight up can't divide any more m8
                    continue
                coefficients = []
                for i in range(coefLimits[0], coefLimits[1]+1):
                    if i == 0 or i == 1 or i == subX or i == lastElem or subX // i < subXLimits[0] or subX // i > subXLimits[1] or subX // i == 0:
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
                if (subX > subXLimits[1] or subX == 0 or subX == 1):  # we straight up can't multiply any more m8
                    continue
                # the coefficient gotta stay below (subXLimits[1] / subX)
                if (subXLimits[1] / subX == 1 or subXLimits[1] / subX == 0):
                    continue
                attCount = 0
                while (coefficient > subXLimits[1] / subX or coefficient == 1 or coefficient == 0 or coefficient == subX or subX // coefficient == 0):
                    coefficient = random.randint(min(0, max(coefLimits[0], int(subXLimits[0] / subX))), max(0, min(int(subXLimits[1] / subX), coefLimits[1])))
                    attCount += 1
                    if attCount > 20:
                        break    # screw this
                if attCount > 20:
                    continue
                subX *= coefficient
            
        radicalList.append([action, coefficient]) 
        lastElem = coefficient
        radicalNum -= 1

    for recurCounter in range (recursiveAmount[0]):
        # print(f"A: {radicalList}")
        linearRadicalList = linearizeRadicalList(radicalList)
        if len(linearRadicalList) == 0:
            return [], -1, -1
        oldExpr = random.choice(linearRadicalList)
        # print(f"B: {oldExpr}")
        newExpr = generateExpressionInternal(recursiveAmount[1], featureToggles, (0, 0), False, (oldExpr[1], oldExpr[1]), coefLimits, subXLimits)
        # print(f"C: {newExpr}")
        listRef = radicalList
        for i in oldExpr[2]:
            listRef = listRef[i]
            if len(listRef) == 2 and type(listRef[0]) == int and type(listRef[1]) == list:
                listRef = listRef[1]
            # print(f"L: {listRef}")
        listRef[1] = newExpr[0]
        # print(f"D: {radicalList}\n\n")
        
    if equationMode:
        radicalList.append([-1, "x"])
    else:
        radicalList.append([-1, subX])
    return radicalList, x, subX

def generateExpressionLessInternal(radicalAmount : int, featureToggles : list = (True, True, True, True), recursiveAmount : list = (0, 0), equationMode : bool = False, xLimits : tuple = (0, 100), coefLimits : tuple = (0, 100), subXLimits : tuple = (0, 100)):
    radicalList, x, subX = generateExpressionInternal(radicalAmount, featureToggles, recursiveAmount, equationMode, xLimits, coefLimits, subXLimits)
    if equationMode:
        return len(radicalList), f"{radicalListToString(radicalList)} = {x}", subX
    else:
        return len(radicalList), radicalListToString(radicalList), x


def generateExpression(expressionType : int, difficulty : float, exponent : int, additionalSettings : list) -> tuple:
    if (expressionType == 0 or expressionType == 1):
        # additional settings should be the feature toggles, checking that
        if (len(additionalSettings) != 4 or difficulty < 0 or difficulty > 2):
            return ()
        
        totalRadicalAmount = int(2.5 * (difficulty + random.random()) + 3)
        minRadicalAmount = int(2.5 * (difficulty + 0) + 3)
        maxRadicalAmount = int(2.5 * (difficulty + 1) + 3)

        configs = [(totalRadicalAmount, (0, 0))]
        for i in range(1, totalRadicalAmount-1):
            for j in [x for x in range(1, i) if i % x == 0]:
                configs.append((totalRadicalAmount - i, (j, (i // j)+1)))

        negativeAllowed = exponent < 0
        exponent = abs(exponent)
        subXLimits = (0, 10**math.ceil(exponent)-1)
        coefLImits = ((10**math.floor(exponent-1)), 10**math.ceil(exponent)-1)
        xLimits = (-(10**math.ceil(exponent)) if negativeAllowed else (10**math.floor(exponent-1)), 10**math.ceil(exponent)-1)
        equationMode = expressionType == 1

        curRadAmount = -1

        while (curRadAmount < minRadicalAmount or curRadAmount > maxRadicalAmount): # protection from hanging
            radicalAmount, recurArgs = random.choice(configs)

            return_val = generateExpressionLessInternal(radicalAmount, additionalSettings, recurArgs, equationMode, xLimits, coefLImits, subXLimits)
            curRadAmount = return_val[0]
            return_val = return_val[1:]
        
        return return_val
            

if __name__ == "__main__":
    for i in range (3*33):
        timeA = time.time()
        print(i, printExpression(generateExpression(0, i // 33, 4.3, (True, True, True, True))))
        timeB = time.time()
        print(f"Generated in {timeB-timeA} seconds.")
