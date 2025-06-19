import subprocess
import json
import tempfile
import os

def check_syntax(code):
    try:
        compile(code, '<string>', 'exec')
        return None
    except SyntaxError as e:
        return f"Syntax Error: {e.msg} on line {e.lineno}"

def run_code_against_test_cases(user_code, test_cases_json, language='Python'):
    if language.lower() != 'python':
        return {"status": "Language Not Supported", "details": "Only Python is supported."}
    
    syntax_error = check_syntax(user_code)
    if syntax_error:
        return {"status": "Syntax Error", "details": syntax_error}
    
    results = []
    test_cases = json.loads(test_cases_json)
    try:
        function_name = user_code.split('def ')[1].split('(')[0].strip()
    except IndexError:
        return {"status": "Evaluation Error", "details": "Could not find a function definition ('def...'). Please define a function."}

    for i, test in enumerate(test_cases):
        test_input_str = ', '.join(map(repr, test["input"]))
        full_script = f"{user_code}\n\nprint({function_name}({test_input_str}))"
        
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".py") as temp_f:
                temp_f.write(full_script)
                temp_f_path = temp_f.name
            
            process = subprocess.run(['python', temp_f_path], capture_output=True, text=True, timeout=5)
            os.remove(temp_f_path)

            if process.returncode == 0:
                actual_output_str = process.stdout.strip()
                try:
                    # Try to evaluate the output to handle lists, numbers etc.
                    actual_output = eval(actual_output_str)
                except:
                    actual_output = actual_output_str

                expected_output = test["output"]
                if actual_output == expected_output:
                    results.append({"passed": True, "input": test["input"], "output": actual_output})
                else:
                    results.append({"passed": False, "input": test["input"], "expected": expected_output, "got": actual_output})
            else:
                return {"status": "Runtime Error", "details": process.stderr.strip()}
        except Exception as e:
            return {"status": "Evaluation Error", "details": str(e)}

    if all(r['passed'] for r in results):
        return {"status": "All Tests Passed", "details": results}
    else:
        return {"status": "Tests Failed", "details": results}