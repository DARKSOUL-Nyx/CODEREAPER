import os
import logging
import time
from colorama import Fore, Style, init
from tools import ReaperTools
from repo_tools import RepoManager, DependencyGraph
from agents import get_inquisitor_agent, get_surgeon_agent, get_executioner_agent
from memory import MemoryBank

init(autoreset=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename='codereaper_research.csv')

memory = MemoryBank()

def print_step(agent, action):
    print(f"\n{Fore.CYAN}┌── 🤖 {agent.upper()} ──────────────────────────────────┐")
    print(f"│ Action: {action}")
    print(f"└──────────────────────────────────────────────────────────┘{Style.RESET_ALL}")

def main():
    # --- RESEARCH CONFIGURATION ---
    # We use a repo with varied algorithms to show versatility
    GITHUB_REPO = "https://github.com/TheAlgorithms/Python" 
    
    print(f"{Fore.CYAN}🚀 INITIALIZING RESEARCH PROTOCOL: GRAPH-AWARE REFACTORING{Style.RESET_ALL}")
    
    # 1. SETUP ENV & CLONE
    repo_manager = RepoManager(GITHUB_REPO)
    repo_path = repo_manager.clone_repo()
    
    # 2. BUILD THE BRAIN (Dependency Graph)
    print(f"{Fore.MAGENTA}🕸️ Constructing AST Dependency Graph...{Style.RESET_ALL}")
    graph = DependencyGraph(repo_path)
    
    # 3. FIND TARGETS (Inquisitor)
    all_files = repo_manager.get_all_python_files()
    priority_queue = []
    
    print(f"{Fore.YELLOW}🔍 Scanning {len(all_files)} files for complexity...{Style.RESET_ALL}")
    
    # Limit scan for demo speed (first 20 valid files)
    scan_limit = 20
    scanned = 0
    
    for file_path in all_files:
        if scanned >= scan_limit: break
        
        try:
            # Quick check: Only care about files > 1KB to avoid empty inits
            if os.path.getsize(file_path) < 1000: continue
            
            report = ReaperTools.analyze_complexity(file_path)
            # If we find complexity > 10 (B or C grade)
            if '"complexity": 1' not in report and '"complexity": 2' not in report: # Rudimentary filter for "interesting" files
                 priority_queue.append(file_path)
                 print(f"  Found Target: {os.path.basename(file_path)}")
            scanned += 1
        except:
            continue

    print(f"{Fore.RED}🎯 Targets Acquired: {len(priority_queue)} candidates.{Style.RESET_ALL}")
    
    if not priority_queue:
        print("No high-complexity files found in the scan limit. Try increasing scan_limit.")
        return

    # 4. EXECUTE SURGERY (On the first target)
    target_file = priority_queue[0] 
    print(f"\n{Fore.CYAN}--- INITIATING REFACTOR ON: {target_file} ---{Style.RESET_ALL}")

    # Generate the Shield (Novelty)
    constraints = graph.generate_constraints(target_file)
    print(f"{Fore.MAGENTA}🛡️ ACTIVATING DEPENDENCY SHIELD:\n{constraints}{Style.RESET_ALL}")
    
    surgeon = get_surgeon_agent()
    executioner = get_executioner_agent()
    
    # --- REFACTORING LOOP ---
    code_content = ReaperTools.read_file(target_file)
    
    prompt = f"""
    You are a Senior Architect. Refactor this code to reduce complexity and improve readability.
    
    {constraints}
    
    Original Code:
    {code_content}
    
    CRITICAL INSTRUCTIONS:
    1. Output ONLY raw Python code.
    2. Maintain all functionality.
    3. Add Type Hints.
    """
    
    print_step("Surgeon", "Generating optimized code...")
    new_code = surgeon.send_message(prompt).replace("```python", "").replace("```", "").strip()
    
    # Validate Syntax before saving
    valid, msg = ReaperTools.validate_syntax(new_code)
    if not valid:
        print(f"{Fore.RED}❌ Syntax Error generated. Aborting to protect repo.{Style.RESET_ALL}")
        return

    ReaperTools.write_file(target_file, new_code)
    print(f"{Fore.GREEN}✔ Code applied to disk.{Style.RESET_ALL}")
    
    # --- TEST GENERATION ---
    print_step("Executioner", "Generating Regression Tests...")
    test_prompt = f"""
    Write a pytest unit test for this code to ensure I didn't break logic.
    Use 'sys.path.append' to handle imports if needed.
    Output ONLY raw python code.
    
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
        # In full version, this triggers the retry loop

if __name__ == "__main__":
    main()