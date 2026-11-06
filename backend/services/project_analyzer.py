"""
ECHO — Project Intelligence Service
Analyzes uploaded project ZIP archives and GitHub repository URLs.
Strict security rules:
- NEVER execute any uploaded code.
- Prevent Zip Slip / path traversal vulnerabilities.
- Ignore node_modules, .git, __pycache__, .venv, and binary files.
"""

import os
import zipfile
import json
import urllib.request
from typing import Dict, Any, List

IGNORED_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", ".idea", ".vscode", "target"
}

IGNORED_EXTENSIONS = {
    ".exe", ".dll", ".so", ".dylib", ".bin", ".pyc", ".class",
    ".jar", ".war", ".png", ".jpg", ".jpeg", ".mp4", ".zip", ".tar", ".gz"
}

class ProjectAnalyzer:
    @staticmethod
    def analyze_zip(file_bytes: bytes) -> Dict[str, Any]:
        """Safely inspect a ZIP archive in memory without executing code"""
        import io
        zip_buffer = io.BytesIO(file_bytes)

        files_summary = []
        detected_tech = set()
        readme_snippet = ""
        total_files = 0
        total_size = 0

        project_name = ""
        with zipfile.ZipFile(zip_buffer, 'r') as zf:
            for info in zf.infolist():
                total_files += 1
                total_size += info.file_size

                # Security Guard: Limit archive footprint
                if total_files > 500 or total_size > 50 * 1024 * 1024:
                    break

                # Security Guard: Prevent Zip Slip path traversal
                norm_path = os.path.normpath(info.filename)
                if norm_path.startswith("..") or os.path.isabs(norm_path):
                    continue

                parts = norm_path.split(os.sep)
                if any(p in IGNORED_DIRS for p in parts):
                    continue

                if not project_name and parts and parts[0] and parts[0] not in [".", ".."]:
                    project_name = parts[0].replace("_", " ").replace("-", " ").title()

                ext = os.path.splitext(norm_path)[1].lower()
                if ext in IGNORED_EXTENSIONS:
                    continue

                # Add to file list if reasonable
                if not info.is_dir():
                    files_summary.append(norm_path)

                # Extension-based language hints
                if ext in [".py", ".pyw"]:
                    detected_tech.add("Python")
                elif ext in [".ts", ".tsx"]:
                    detected_tech.add("TypeScript")
                elif ext in [".js", ".jsx"]:
                    detected_tech.add("JavaScript")
                elif ext in [".java"]:
                    detected_tech.add("Java")
                elif ext in [".go"]:
                    detected_tech.add("Go")
                elif ext in [".rs"]:
                    detected_tech.add("Rust")
                elif ext in [".cpp", ".hpp", ".c"]:
                    detected_tech.add("C/C++")
                elif ext in [".sql"]:
                    detected_tech.add("SQL / Database")

                # Inspect manifest files for tech detection
                filename = os.path.basename(norm_path).lower()
                if filename == "package.json":
                    try:
                        content = zf.read(info.filename).decode('utf-8', errors='ignore')
                        pkg = json.loads(content)
                        if pkg.get("name"):
                            project_name = pkg.get("name").replace("_", " ").replace("-", " ").title()
                        deps = list(pkg.get("dependencies", {}).keys()) + list(pkg.get("devDependencies", {}).keys())
                        for d in deps[:15]:
                            detected_tech.add(d)
                    except Exception:
                        pass
                elif filename == "requirements.txt":
                    try:
                        content = zf.read(info.filename).decode('utf-8', errors='ignore')
                        for line in content.splitlines():
                            req = line.strip().split("==")[0].split(">=")[0].split("<")[0].strip()
                            if req and not req.startswith("#"):
                                detected_tech.add(req)
                    except Exception:
                        pass
                elif filename in ["dockerfile", "docker-compose.yml", "docker-compose.yaml"]:
                    detected_tech.add("Docker")
                elif filename in ["readme.md", "readme.txt"]:
                    try:
                        content = zf.read(info.filename).decode('utf-8', errors='ignore')
                        readme_snippet = content[:800].strip()
                    except Exception:
                        pass

        if not project_name:
            project_name = "Custom Project"

        return {
            "project_name": project_name,
            "total_files_inspected": len(files_summary),
            "sample_files": files_summary[:20],
            "detected_technologies": list(detected_tech)[:20],
            "readme_summary": readme_snippet or "No README file detected.",
            "status": "analyzed_safely"
        }

    @staticmethod
    def analyze_github_url(url: str) -> Dict[str, Any]:
        """Inspect a public GitHub repository using the GitHub REST API"""
        clean_url = url.strip().rstrip("/")
        parts = clean_url.split("github.com/")
        if len(parts) < 2:
            return {"error": "Invalid GitHub URL format."}

        repo_path = parts[1]
        repo_parts = repo_path.split("/")
        if len(repo_parts) < 2:
            return {"error": "Expected URL format: https://github.com/owner/repository"}

        owner, repo = repo_parts[0], repo_parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "ECHO-Interview-Platform"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {
                    "repo_name": data.get("name"),
                    "full_name": data.get("full_name"),
                    "description": data.get("description") or "No description provided.",
                    "primary_language": data.get("language") or "General",
                    "stars": data.get("stargazers_count", 0),
                    "topics": data.get("topics", []),
                    "html_url": data.get("html_url")
                }
        except Exception as err:
            return {
                "repo_name": repo,
                "owner": owner,
                "description": f"Repository reference captured: {owner}/{repo}",
                "note": f"Live GitHub API query skipped ({str(err)}). Saved for interview context."
            }
