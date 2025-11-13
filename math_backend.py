from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp
from sympy import symbols, diff, integrate, solve, limit, series
import re

app = Flask(__name__)
CORS(app)

def parse_math_input(input_text):
    """Parse user input and determine the operation"""
    input_text = input_text.lower().replace(' ', '')
    
    # Detect derivative
    if 'd/dx' in input_text or 'derivative' in input_text:
        expr = input_text.replace('d/dx', '').replace('derivative', '').replace('(', '').replace(')', '')
        return {'type': 'derivative', 'expression': expr}
    
    # Detect integral
    elif '∫' in input_text or 'integral' in input_text:
        expr = input_text.replace('∫', '').replace('integral', '').replace('dx', '')
        return {'type': 'integral', 'expression': expr}
    
    # Detect equation solving
    elif '=' in input_text:
        return {'type': 'solve', 'expression': input_text}
    
    # Default to expression simplification
    else:
        return {'type': 'simplify', 'expression': input_text}

@app.route('/solve', methods=['POST'])
def solve_math():
    try:
        data = request.json
        problem = data.get('problem', '')
        
        parsed = parse_math_input(problem)
        x = symbols('x')
        result = {}
        
        if parsed['type'] == 'derivative':
            expr = sp.sympify(parsed['expression'])
            derivative = diff(expr, x)
            result = {
                'steps': [
                    f'Problem: d/dx({expr})',
                    f'Step 1: Apply derivative rules',
                    f'Step 2: Derivative of {expr} with respect to x',
                    f'Final Answer: {derivative}'
                ],
                'answer': str(derivative)
            }
            
        elif parsed['type'] == 'integral':
            expr = sp.sympify(parsed['expression'])
            integral = integrate(expr, x)
            result = {
                'steps': [
                    f'Problem: ∫{expr} dx',
                    f'Step 1: Apply integration rules',
                    f'Step 2: Integral of {expr} with respect to x',
                    f'Final Answer: {integral} + C'
                ],
                'answer': str(integral) + ' + C'
            }
            
        elif parsed['type'] == 'solve':
            # Simple equation solving
            equation = sp.sympify(parsed['expression'])
            solution = solve(equation, x)
            result = {
                'steps': [
                    f'Problem: {equation}',
                    f'Step 1: Solve for x',
                    f'Step 2: Solution set',
                    f'Final Answer: {solution}'
                ],
                'answer': str(solution)
            }
            
        else:
            expr = sp.sympify(parsed['expression'])
            simplified = sp.simplify(expr)
            result = {
                'steps': [
                    f'Problem: {expr}',
                    f'Step 1: Simplify expression',
                    f'Final Answer: {simplified}'
                ],
                'answer': str(simplified)
            }
            
        return jsonify({'success': True, 'result': result})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)