import random
import sympy as sp

def generate_super_easy_example():
    num_operations = random.randint(1, 4)
    operands = [str(random.randint(1, 100)) for _ in range(num_operations)]
    operators = [random.choice(['+', '-', '*', '/']) for _ in range(num_operations - 1)]
    example = ' '.join([f"{operands[i]} {operators[i]}" for i in range(num_operations - 1)]) + f" {operands[-1]}"
    answer = eval(example)
    return example+" = ?", answer

def generate_easy_example():
    while True:
        a = random.randint(1, 100)
        b = random.randint(1, 20)
        c = random.randint(1, 100)
        example_type = random.choice([1, 2])
        
        if example_type == 1:
            example = f"{a} + x = {b}x + {c}"
            x = sp.symbols('x')
            solution = sp.solve(sp.Eq(a + x, b*x + c), x)
        else:
            example = f"{a} - x = {b}x - {c}"
            x = sp.symbols('x')
            solution = sp.solve(sp.Eq(a - x, b*x - c), x)
        
        if solution and all(is_valid_solution(sol) for sol in solution):
            answer = float(solution[0])
            return example, answer

def generate_medium_example():
    while True:
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        c = random.randint(1, 100)
        example_type = random.choice([1, 2])
        
        if example_type == 1:
            example = f"x^2 + {a}x + {b} = {c}"
            x = sp.symbols('x')
            solution = sp.solve(sp.Eq(x**2 + a*x + b, c), x)
        else:
            example = f"{a}x^2 + {b}x = {c}"
            x = sp.symbols('x')
            solution = sp.solve(sp.Eq(a*x**2 + b*x, c), x)
        
        if solution and all(is_valid_solution(sol) for sol in solution):
            answer = float(solution[0])
            return example, answer

def generate_hard_example():
    while True:
        base = random.randint(2, 10)
        result = random.randint(1, 5)
        example_type = random.choice([1, 2])
        
        if example_type == 1:
            example = f"log_{base}(x) = {result}"
            x = sp.symbols('x')
            solution = sp.solve(sp.Eq(sp.log(x, base), result), x)
        else:
            example = f"log_{base}({result}*x) = {result + 1}"
            x = sp.symbols('x')
            solution = sp.solve(sp.Eq(sp.log(result*x, base), result + 1), x)
        
        if solution and all(is_valid_solution(sol) for sol in solution):
            answer = float(solution[0])
            return example, answer

def is_valid_solution(solution):
    if isinstance(solution, (sp.Integer, sp.Rational)):
        return -100 <= float(solution) <= 100 and abs(float(solution) % 1) <= 0.01
    return False

def generate_example(difficulty):
    if difficulty == "super_easy":
        return generate_super_easy_example()
    elif difficulty == "easy":
        return generate_easy_example()
    elif difficulty == "medium":
        return generate_medium_example()
    elif difficulty == "hard":
        return generate_hard_example()
    else:
        return "Invalid difficulty level"

# Пример использования
difficulty = "super_easy"
example, answer = generate_example(difficulty)
print(example)
print("Answer:", answer)
