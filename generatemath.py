import random
# import sympy as sp
from data.examples import Examples

# constants
opstring = "+-*/"

def radicalListToString(radicalList : list) -> str:
    radicalList.reverse()
    string = f"{radicalList[0][1]}"
    print(radicalList)
    lastPriority = 10000
    for i in radicalList[1:]:
        order = random.randint(0, 1)
        if (type(i[1]) == list):
            i[1] = radicalListToString[i[1]]
        match i[0]:
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
    

def generate_equation(radicalAmount : int, featureToggles : list, xLimits : tuple = (0, 100), coefLimits : tuple = (0, 100), subXLimits : tuple = (1, 100)):

    features = [i for i in range(len(featureToggles)) if featureToggles[i]]
    print(features)

    x : int = random.randint(xLimits[0], xLimits[1])
    subX : int = x
    radicalList = []
    radicalNum = radicalAmount
    lastElem = -1
    while (radicalNum > 0):
        print(f"New action, radically {radicalNum}")
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
            
        radicalList.append((action, coefficient)) 
        lastElem = coefficient
        radicalNum -= 1

    radicalList.append((-1, subX))
    
    return radicalListToString(radicalList), x

if __name__ == "__main__":
    print(generate_equation(5, (True, True, False, False)))
