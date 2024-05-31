import random
# import sympy as sp
from data.examples import Examples

# constants
opstring = "+-*/"
subxreplacement = "__SUBX__"

def generate_equation(radicalAmount: int, featureCount : int, xLimits : tuple = (0, 100), coefLimits : tuple = (0, 100), subXLimits : tuple = (1, 100)):
   
    x : int = random.randint(xLimits[0], xLimits[1])
    subX : int = x
    problemStr = subxreplacement
    i = radicalAmount
    while (i > 0):
        coefficient = random.randint(coefLimits[0], coefLimits[1])
        action = random.randint(0, featureCount)
        if (action == 0):   # addition
            if (subX < subXLimits[0]):  # we can't fucking subtract any more m8
                continue
            while (subX - coefficient < subXLimits[0]):
                coefficient = int(coefficient // random.uniform(0.4, 4))
            if (coefficient == 0):
                continue
            subX -= coefficient
            problemStr = f"{problemStr}+{coefficient}"
        elif (action == 1): # subtraction
            if (subX > subXLimits[1]):  # we can't fucking add any more m8
                continue
            while (subX + coefficient > subXLimits[1]):
                coefficient = int(coefficient // random.uniform(0.4, 4))
            if (coefficient == 0):
                continue
            subX += coefficient
            problemStr = f"{problemStr}-{coefficient}"
        
        i -= 1
    idx = problemStr.find(subxreplacement)
    problemStr = f"{problemStr[:idx]}{subX}{problemStr[idx+len(subxreplacement):]} = ?"
    
    return problemStr, x

if __name__ == "__main__":
    print(generate_equation(3, 1))
