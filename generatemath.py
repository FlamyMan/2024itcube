import random
# import sympy as sp
from data.examples import Examples

# constants
opstring = "+-*/"

def generate_equation(radicalAmount: int, featureCount : int, xLimits : tuple = (0, 100), coefLimits : tuple = (0, 100), subXLimits : tuple = (1, 100)):
   
    x : int = random.randint(xLimits[0], xLimits[1])
    subX : int = x
    radicalList = []
    radicalNum = radicalAmount
    while (radicalNum > 0):
        coefficient = random.randint(coefLimits[0], coefLimits[1])
        action = random.randint(0, featureCount)
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
                    if i == 0 or i == 1 or i == subX or subX // i < subXLimits[0] or subX // i > subXLimits[1]:
                        continue
                    if (subX % i == 0):
                        coefficients.append(i)
                if (len(coefficients) == 0):
                    continue
                diff = [coefficient-i for i in coefficients]
                diff = diff.index(min(diff))
                coefficient = coefficients[diff]
                subX = int(subX // coefficient)
        radicalList.append((action, coefficient))
        
        radicalNum -= 1
    problemStr = f"{subX}"
    radicalList.reverse()
    for i in radicalList:
        match i[0]:
            case 0:
                problemStr = f"{problemStr}+{i[1]}"
            case 1:
                problemStr = f"{problemStr}-{i[1]}"
            case 2:
                problemStr = f"({problemStr})*{i[1]}"
    
    return problemStr, x

if __name__ == "__main__":
    print(generate_equation(5, 2))
