import os
import ast
import git
import shutil
import logging

class RepoManager:
    def __init__(self, repo_url, local_dir="temp_repo"):
        self.repo_url = repo_url
        self.local_dir = local_dir
        self.repo = None

    def clone_repo(self):
        if os.path.exists(self.local_dir):
            try:
                shutil.rmtree(self.local_dir)
            except PermissionError:
                print("⚠ Warning: Could not delete temp_repo. Using existing one.")
        
        if not os.path.exists(self.local_dir):
            print(f"📦 Cloning {self.repo_url}...")
            self.repo = git.Repo.clone_from(self.repo_url, self.local_dir)
        else:
             self.repo = git.Repo(self.local_dir)
        return self.local_dir

    def get_all_python_files(self):
        py_files = []
        for root, dirs, files in os.walk(self.local_dir):
            if ".git" in root: continue
            for file in files:
                if file.endswith(".py") and "test" not in file:
                    py_files.append(os.path.join(root, file))
        return py_files

class DependencyGraph:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        # map: {'filename.py': ['importer1.py', 'importer2.py']}
        self.adjacency_list = {} 
        self._build_graph()

    def _build_graph(self):
        """Scans imports to build the dependency graph."""
        file_map = {}
        # 1. Index all files
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    file_map[file] = full_path

        # 2. Parse imports
        for filename, full_path in file_map.items():
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    imported_name = None
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            imported_name = n.name
                    elif isinstance(node, ast.ImportFrom):
                        imported_name = node.module

                    if imported_name:
                        # Simple heuristic for demo: check if module name matches a filename
                        # (Real production code would need full python path resolution)
                        potential_match = f"{imported_name}.py"
                        target_path = file_map.get(potential_match)
                        
                        if target_path:
                            if target_path not in self.adjacency_list:
                                self.adjacency_list[target_path] = []
                            if full_path not in self.adjacency_list[target_path]:
                                self.adjacency_list[target_path].append(full_path)
            except Exception:
                continue

    def get_dependents(self, file_path):
        """Returns list of files that import the given file."""
        return self.adjacency_list.get(file_path, [])

    def generate_constraints(self, target_file):
        """
        THE RESEARCH NOVELTY:
        Generates a text block explaining what NOT to break.
        """
        dependents = self.get_dependents(target_file)
        if not dependents:
            return "No external dependencies found. You have full freedom to refactor."

        constraint_msg = [f"CRITICAL: This file is imported by {len(dependents)} other files."]
        constraint_msg.append("You MUST preserve the following potential interfaces:")
        
        # In a full research implementation, we would inspect the *call sites* in dependents.
        # For this Hackathon/Capstone, we list the files to simulate "Graph Awareness".
        for dep in dependents:
            constraint_msg.append(f"- Imported by: {os.path.basename(dep)}")
        
        constraint_msg.append("DO NOT change public function names or class names.")
        constraint_msg.append("DO NOT change argument order in public functions.")
        
        return "\n".join(constraint_msg)