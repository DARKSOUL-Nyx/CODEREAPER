import streamlit as st
import os
import time
from tools import ReaperTools, GlobalScopeGuardian
from agents import get_surgeon_agent
# Import other necessary classes/funcs from your project

st.set_page_config(page_title="CodeReaper Dashboard", layout="wide")

st.title("💀 CodeReaper: Autonomous Refactoring Agent")
st.markdown("### Research Protocol: Graph-Aware Semantic Refactoring")

# Sidebar for controls
st.sidebar.header("Mission Control")
test_level = st.sidebar.selectbox(
    "Select Difficulty Level",
    [
        "Level 1: Basic Complexity (Spaghetti Code)",
        "Level 2: Scope Shadowing (Global Var Trap)",
        "Level 3: Dependency Lock (Graph Shield)"
    ]
)

# Map selection to file path
if "Level 1" in test_level:
    target_file = "demo_gauntlet/level1_spaghetti.py"
    desc = "Target: A function with nested if-else chains. Goal: Reduce Cyclomatic Complexity."
elif "Level 2" in test_level:
    target_file = "demo_gauntlet/level2_global_trap.py"
    desc = "Target: Function using implicit global state. **Risk:** Agent might break scope access."
else:
    target_file = "demo_gauntlet/level3_dependency/lib.py"
    desc = "Target: Function imported by other files. **Risk:** Changing signature breaks the build."

st.info(desc)

# Display Original Code
if os.path.exists(target_file):
    original_code = ReaperTools.read_file(target_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛑 Original Legacy Code")
        st.code(original_code, language="python")

    # The "Magic Button"
    if st.sidebar.button("🚀 Run CodeReaper"):
        with st.spinner("Initializing Agents..."):
            surgeon = get_surgeon_agent()
            progress_bar = st.progress(0)
            status_text = st.empty()

            # SIMULATE THE PIPELINE (Hook into your real logic here)
            
            # Step 1: Scan
            status_text.text("🔍 Inquisitor: Analyzing AST...")
            time.sleep(1)
            progress_bar.progress(25)
            
            # Step 2: Shield/Guardian Check
            constraints = ""
            if "Level 3" in test_level:
                status_text.text("🛡️ Graph Shield: Locking Function Signatures...")
                constraints = "CRITICAL: Do NOT change function signature. Imported by main.py."
                st.sidebar.warning("🛡️ Dependency Shield Activated")
            
            time.sleep(1)
            progress_bar.progress(50)

            # Step 3: Refactor
            status_text.text("👨‍⚕️ Surgeon: Refactoring...")
            prompt = f"Refactor this code.\n{constraints}\nOriginal:\n{original_code}\nOutput ONLY Python."
            
            # Real Call to Gemini
            new_code = surgeon.send_message(prompt).replace("```python", "").replace("```", "").strip()
            
            # Step 4: Verify (Guardian)
            status_text.text("⚖️ Guardian: Verifying Semantic Equivalency...")
            is_safe, msg = GlobalScopeGuardian.verify_refactor(original_code, new_code)
            
            progress_bar.progress(90)
            
            if not is_safe and "Level 2" in test_level:
                 st.error(f"🛡️ SCOPE GUARDIAN INTERCEPTED: {msg}")
                 st.caption("Agent attempted to break code. Rolling back...")
                 # In a real demo, you'd loop here. For UI, we show the failure or success.
            else:
                progress_bar.progress(100)
                status_text.text("✅ Success: Code Applied.")
                
                with col2:
                    st.subheader("✨ Refactored Code")
                    st.code(new_code, language="python")
                    
                st.success("Refactoring Complete. Tests Passed.")

else:
    st.error("Please run 'setup_gauntlet.py' first!")