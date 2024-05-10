import random


DEGREE, MULTIPLICATION, DIVISION, MINUS, PLUS = range(5) # operators by order of solving
OPERATORS_CHARACTERS = {
    PLUS: "+",
    MINUS: "-",
    MULTIPLICATION: "*",
    DIVISION: "/",
    DEGREE: "^"
}
BASE_CHANCES = {
    DEGREE: 0,
    PLUS: 25,
    MINUS: 25,
    DIVISION: 25,
    MULTIPLICATION: 25
}
BASE_BRAKETS_CHANCE = 10


class OperatorTable:
    def __init__(self, chances: dict = BASE_CHANCES):
        """
        Create operator table from chances.

        :param chances: a dict with keys PLUS, MINUS... and values int. The sum of values must be == 100 
        """
        self.chances = chances
        chance_sum = sum(self.chances.values())
        if chance_sum != 100:
            raise ValueError("Sum of chances must be equal to 100")
        self.chance_table = OperatorTable.generate_chance_table(chances)

    @staticmethod
    def generate_chance_table(chances):
        """
        """
        last = 0
        operators_table = []
        for v in chances.values():
            operators_table.append(last+v)
            last += v
        return operators_table
    
    @staticmethod
    def get_operator_by_order(n: int) -> str:
        """
        gets operator eg. +, -, *, or / by it's order
        """
        if n not in OPERATORS_CHARACTERS.keys():
            raise ValueError("No such operator order")
        return OPERATORS_CHARACTERS[n]

    def get_operator_by_chance_table(self, n: int) -> str: # n must be an integer in [0, 100]
        if n < 0:
            raise ValueError("n can't be less than 0")
        
        i = 0
        while i < len(self.chance_table):
            if n < self.chance_table[i]:
                return OperatorTable.get_operator_by_order(i)
            i += 1 # fuck python please give me i++
            
    def get_random_operator(self) -> str:
        rndn = random.randint(0, 99)
        return self.get_operator_by_chance_table(rndn)

class Generator:
    def __init__(self, min_n: int, max_n: int, hardness: int, brakets_chance: int = BASE_BRAKETS_CHANCE , operator_table: OperatorTable = OperatorTable()) -> None:
        self.max_n: int = max_n
        self.min_n: int = min_n
        self.hardness: int = hardness
        self.brakets_chance: int = brakets_chance
        self.operator_table: OperatorTable = operator_table
    
    def build_example(self, radicals: list) -> str:
        output = ""
        for radical in radicals:
            op = Generator.check_radical_operator(radical)
            if op == "/" or op == "*":
                output = self.try_add_brakets(output)
            output += radical
        return output
    
    @staticmethod
    def check_radical_operator(radical):
        return radical[0]
    def try_add_brakets(self, str) -> str:
        rndn = random.randint(0, 99)
        if rndn < self.brakets_chance:
            return "(" + str + ")"
        else:
            return str
        
    def generate_raw(self) -> list:
        output = []
        i = 0
        while i < (self.hardness + 1) * 4:
            output.append(self.generate_radical())
            i += 1
        return output

    def generate_radical(self) -> str: 
        """
        the radical is a small part for example
        "22+4-5*4/3" will have radicals: ["+22", "+4", "-5", "*4", "/3"]
        """
        operator = self.operator_table.get_random_operator()
        n = random.randint(self.min_n, self.max_n - 1)
        return operator + str(n)

gen = Generator(0, 100, 0)
raw = gen.generate_raw()
print(raw)
print(gen.build_example(raw))