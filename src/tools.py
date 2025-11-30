import os
import subprocess
import radon.complexity as radon_cc
from radon.visitors import ComplexityVisitor
import json
import ast
from googlesearch import search
import builtins  # IMPORT BUILTINS TO FIX THE 'list' FALSE POSITIVE

class ReaperTools:
    @staticmethod
    def read_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def write_file(filepath, content):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    @staticmethod
    def analyze_complexity(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            v = ComplexityVisitor.from_code(code)
            results = []
            for func in v.functions:
                results.append({
                    "name": func.name,
                    "complexity": func.complexity,
                    "grade": "CRITICAL" if func.complexity > 10 else "ACCEPTABLE"
                })
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error analyzing complexity: {str(e)}"

    @staticmethod
    def run_tests(test_filepath):
        try:
            # -v for verbose, -o to disable warnings that clutter logs
            result = subprocess.run(
                ["pytest", test_filepath, "-v", "-o", "warning_filter=ignore"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return f"TESTS PASSED:\n{result.stdout}"
            else:
                return f"TESTS FAILED:\n{result.stdout}\n{result.stderr}"
        except Exception as e:
            return f"Error running tests: {str(e)}"

    @staticmethod
    def google_search_tool(query):
        try:
            results = []
            for result in search(query, num_results=3, advanced=True):
                results.append(f"Title: {result.title}\nDescription: {result.description}\nURL: {result.url}")
            return "\n---\n".join(results)
        except Exception as e:
            return f"Search failed: {str(e)}"

    @staticmethod
    def validate_syntax(code_string):
        try:
            ast.parse(code_string)
            return True, "Syntax Valid"
        except SyntaxError as e:
            return False, f"Syntax Error: {e}"

class GlobalScopeGuardian:
    """
    Research Module: Addresses 'Edge Case II: Scope Shadowing'.
    Detects if a refactored function loses access to module-level globals.
    """
    
    @staticmethod
    def get_global_usage(code_str):
        """Returns a set of variable names that are used but not defined locally."""
        try:
            tree = ast.parse(code_str)
            used_names = set()
            assigned_names = set()
            defined_funcs_classes = set() # Track functions/classes defined at top level

            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Load):
                        used_names.add(node.id)
                    elif isinstance(node.ctx, ast.Store):
                        assigned_names.add(node.id)
                elif isinstance(node, ast.arg):
                    assigned_names.add(node.arg)
                # FIX 1: Track function and class definitions so recursion isn't flagged
                elif isinstance(node, ast.FunctionDef):
                    defined_funcs_classes.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    defined_funcs_classes.add(node.name)
            
            # Globals are used but not assigned locally, AND not defined as functions/classes
            potential_globals = used_names - assigned_names - defined_funcs_classes
            
            # FIX 2: Robust Builtin Filter (Fixes the 'list' error)
            builtin_names = set(dir(builtins))
            return potential_globals - builtin_names
        except Exception:
            return set()

    @staticmethod
    def verify_refactor(original_code, new_code):
        original_globals = GlobalScopeGuardian.get_global_usage(original_code)
        new_globals = GlobalScopeGuardian.get_global_usage(new_code)
        
        try:
            new_tree = ast.parse(new_code)
            new_args = set()
            for node in ast.walk(new_tree):
                if isinstance(node, ast.FunctionDef):
                    for arg in node.args.args:
                        new_args.add(arg.arg)
        except:
            return False, "Syntax Error in New Code"

        missing_vars = []
        for var in original_globals:
            # It's safe if it's still used as a global OR passed as an arg
            if var not in new_globals and var not in new_args:
                missing_vars.append(var)
        
        if missing_vars:
            return False, f"CRITICAL SAFETY VIOLATION: Refactor dropped usage of Global Variables: {missing_vars}. This triggers 'Scope Shadowing' [Edge Case II]."
        
        return True, "Scope Safety Check Passed."