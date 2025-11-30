import os
import logging
import time
from colorama import Fore, Style, init

# Import our custom modules
from tools import ReaperTools, GlobalScopeGuardian
from repo_tools import RepoManager, DependencyGraph
from agents import get_inquisitor_agent, get_surgeon_agent, get_executioner_agent
from memory import MemoryBank

# Initialize Environment
init(autoreset=True)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    filename='codereaper_research.csv'
)

memory = MemoryBank()

def print_step(agent, action):
    print(f"\n{Fore.CYAN}┌── 🤖 {agent.upper()} ──────────────────────────────────┐")
    print(f"│ Action: {action}")
    print(f"└──────────────────────────────────────────────────────────┘{Style.RESET_ALL}")

def main():
    # --- CONFIGURATION ---
    # Use TheAlgorithms for the 'Research' demo, or a smaller one for quick testing
    GITHUB_REPO = "https://github.com/TheAlgorithms/Python" 
    
    print(f"{Fore.CYAN}🚀 INITIALIZING RESEARCH PROTOCOL: GRAPH-GUIDED SEMANTIC REFACTORING{Style.RESET_ALL}")
    
    # 1. SETUP ENV & CLONE
    repo_manager = RepoManager(GITHUB_REPO)
    repo_path = repo_manager.clone_repo()
    
    # 2. BUILD THE BRAIN (Dependency Graph)
    print(f"{Fore.MAGENTA}🕸️ Constructing AST Dependency Graph (Novelty Layer)...{Style.RESET_ALL}")
    graph = DependencyGraph(repo_path)
    logging.info("Graph Construction Complete.")
    
    # 3. FIND TARGETS (Inquisitor)
    all_files = repo_manager.get_all_python_files()
    priority_queue = []
    
    print(f"{Fore.YELLOW}🔍 Scanning {len(all_files)} files for Technical Debt...{Style.RESET_ALL}")
    
    # Demo Limit: We don't want to scan 1000 files in the video. Stop after finding 3 candidates.
    scan_limit = 50
    candidates_found = 0
    
    for i, file_path in enumerate(all_files):
        if i >= scan_limit: break
        if candidates_found >= 3: break
        
        try:
            # Skip tiny files or inits
            if os.path.getsize(file_path) < 500 or "__init__" in file_path: continue
            
            report = ReaperTools.analyze_complexity(file_path)
            # FORCE DEMO TARGET: Binary Search is perfect for demos (Clear Logic, Easy Tests)
            if "binary_search" in file_path:
                 priority_queue.insert(0, file_path) # Put at TOP of list
                 print(f"  Found PRIME Target: {os.path.basename(file_path)}")
                 candidates_found += 1
            
            # Keep the old check as backup
            elif "permutation" in file_path:
                 priority_queue.append(file_path)
                 
        except Exception as e:
            continue

    print(f"{Fore.RED}🎯 Targets Acquired: {len(priority_queue)} candidates.{Style.RESET_ALL}")
    
    if not priority_queue:
        print("No targets found. Try increasing scan_limit.")
        return

    # 4. EXECUTE SURGERY (Process only the first target for the Demo)
    target_file = priority_queue[0] 
    print(f"\n{Fore.CYAN}--- INITIATING SEMANTIC REFACTOR ON: {target_file} ---{Style.RESET_ALL}")

    # --- NOVELTY 1: DEPENDENCY SHIELD ---
    constraints = graph.generate_constraints(target_file)
    print(f"{Fore.MAGENTA}🛡️ ACTIVATING DEPENDENCY SHIELD:\n{constraints}{Style.RESET_ALL}")
    
    surgeon = get_surgeon_agent()
    executioner = get_executioner_agent()
    
    code_content = ReaperTools.read_file(target_file)
    
    # --- REFACTORING LOOP (With Scope Guardian) ---
    max_retries = 3
    current_try = 0
    new_code = ""
    refactor_success = False

    while current_try < max_retries:
        print(f"{Fore.YELLOW}Attempt {current_try+1} to generate safe code...{Style.RESET_ALL}")
        
        prompt = f"""
        You are a Senior Architect. Refactor this code to reduce complexity and improve readability.
        
        {constraints}
        
        Original Code:
        {code_content}
        
        CRITICAL INSTRUCTIONS:
        1. Output ONLY raw Python code. NO markdown blocks.
        2. Use Type Hints.
        3. Do NOT lose functionality.
        """
        
        # If this is a retry, inject the error message into context
        if current_try > 0:
            prompt += f"\n\nPREVIOUS ATTEMPT REJECTED. FIX THIS ERROR: {error_feedback}"

        response = surgeon.send_message(prompt)
        new_code = response.replace("```python", "").replace("```", "").strip()
        
        # --- VALIDATION LAYER ---
        
        # Check 1: Syntax
        valid_syntax, msg = ReaperTools.validate_syntax(new_code)
        if not valid_syntax:
            print(f"{Fore.RED}❌ Syntax Error: {msg}{Style.RESET_ALL}")
            error_feedback = f"Syntax Error: {msg}"
            current_try += 1
            continue

        # Check 2: NOVELTY - SCOPE GUARDIAN (Edge Case II Protection)
        is_safe, safety_msg = GlobalScopeGuardian.verify_refactor(code_content, new_code)
        if not is_safe:
            print(f"{Fore.RED}🛡️ SCOPE GUARDIAN TRIGGERED: {safety_msg}{Style.RESET_ALL}")
            error_feedback = f"CRITICAL SAFETY VIOLATION: {safety_msg}. You must pass these variables as arguments."
            current_try += 1
            continue
            
        # If we get here, code is Syntax-Valid and Scope-Safe
        refactor_success = True
        break

    if not refactor_success:
        print(f"{Fore.RED}🛑 FATAL: Could not generate safe code after {max_retries} attempts.{Style.RESET_ALL}")
        return

    # Commit to disk
    ReaperTools.write_file(target_file, new_code)
    print(f"{Fore.GREEN}✔ Code passed Safety Protocols. Applied to disk.{Style.RESET_ALL}")
    
    # --- STAGE 5: REGRESSION TESTING (Executioner) ---
    print_step("Executioner", "Generating Regression Tests...")
    
    test_prompt = f"""
    Write a pytest unit test for this code.
    Use 'sys.path.append' to handle imports if needed.
    Output ONLY raw python code. NO markdown.
    
    Code:
    {new_code}
    """
    
    test_code = executioner.send_message(test_prompt).replace("```python", "").replace("```", "").strip()
    
    # Save test file next to target
    test_file_path = target_file.replace(".py", "_reaper_test.py")
    ReaperTools.write_file(test_file_path, test_code)
    print(f"{Fore.GREEN}✔ Tests saved to {os.path.basename(test_file_path)}{Style.RESET_ALL}")
    
    # Run Tests
    print_step("Executioner", "Running Validation...")
    results = ReaperTools.run_tests(test_file_path)
    
    if "passed" in results:
        print(f"{Fore.GREEN}🎉 SUCCESS: Refactor verified clean.{Style.RESET_ALL}")
        logging.info(f"SUCCESS: {target_file}")
    else:
        print(f"{Fore.RED}⚠ WARNING: Tests failed. Manual review required.{Style.RESET_ALL}")
        logging.info(f"FAILURE: {target_file}")
        # Note: In a production run, we would enable the secondary Self-Healing loop here.

# --- STAGE 5: REGRESSION TESTING (Executioner) ---
    print_step("Executioner", "Generating Regression Tests...")
    
    test_prompt = f"""
    Write a pytest unit test for this code.
    Use 'sys.path.append' to handle imports if needed.
    Output ONLY raw python code. NO markdown.
    
    Code:
    {new_code}
    """
    
    test_code = executioner.send_message(test_prompt).replace("```python", "").replace("```", "").strip()
    test_file_path = target_file.replace(".py", "_reaper_test.py")
    ReaperTools.write_file(test_file_path, test_code)
    print(f"{Fore.GREEN}✔ Tests saved to {os.path.basename(test_file_path)}{Style.RESET_ALL}")
    
    # --- SELF-HEALING LOOP (The Fix) ---
    max_test_retries = 3
    test_attempts = 0
    
    while test_attempts < max_test_retries:
        print_step("Executioner", f"Running Validation (Attempt {test_attempts+1})...")
        results = ReaperTools.run_tests(test_file_path)
        
        if "passed" in results and "failed" not in results:
            print(f"{Fore.GREEN}🎉 SUCCESS: Refactor verified clean.{Style.RESET_ALL}")
            logging.info(f"SUCCESS: {target_file}")
            break
        else:
            print(f"{Fore.RED}❌ Tests Failed. Triggering Self-Healing...{Style.RESET_ALL}")
            # Feed error back to Surgeon
            error_feedback = f"Tests failed:\n{results}\nFix the code to pass these tests."
            
            prompt = f"Fix this code based on test failure:\n{error_feedback}\n\nCode:\n{new_code}\n\nReturn ONLY raw python."
            new_code = surgeon.send_message(prompt).replace("```python", "").replace("```", "").strip()
            
            # Validate Syntax/Scope again before saving
            is_valid, _ = ReaperTools.validate_syntax(new_code)
            if is_valid:
                ReaperTools.write_file(target_file, new_code)
                print(f"{Fore.YELLOW}🩹 Patch applied. Retrying tests...{Style.RESET_ALL}")
            
            test_attempts += 1

    if test_attempts >= max_test_retries:
        print(f"{Fore.RED}🛑 Manual Review Required.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()