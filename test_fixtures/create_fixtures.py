import os
import zipfile
from pathlib import Path

fixtures_dir = Path('C:/Users/heman/.gemini/antigravity-ide/scratch/echo/test_fixtures')
fixtures_dir.mkdir(parents=True, exist_ok=True)

# 1. Full Stack Resume
(fixtures_dir / 'resume_fullstack.txt').write_text("""Hemanth Kumar
Full Stack Python & Cloud Engineer
Email: hemanth@example.com | Phone: +91 98765 43210
GitHub: https://github.com/developer/distributed-event-cache

SUMMARY
High-performance backend engineer with 4+ years of experience designing asynchronous microservices, distributed caching layers, and cloud infrastructure on AWS. Proficient in Python, FastAPI, PostgreSQL, Redis, and Docker.

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, SQL, Bash
Frameworks: FastAPI, Django, React, Celery, Pydantic, SQLAlchemy
Databases: PostgreSQL, Redis, MongoDB
DevOps & Cloud: Docker, Kubernetes, AWS, GitHub Actions, CI/CD, Linux

PROJECTS
1. Distributed Event Cache Engine (FastAPI & Redis)
- Engineered an event-driven pub/sub caching system with sub-15ms p99 response times.
- Designed idempotency middleware to eliminate duplicate webhooks under at-least-once delivery.
- Containerized microservices using Docker and orchestrated multi-region deployments.
""", encoding='utf-8')

# 2. ML Resume
(fixtures_dir / 'resume_ml.txt').write_text("""Aarav Sharma
Machine Learning & AI Engineer
Email: aarav.sharma@example.com
GitHub: https://github.com/ai-dev/multilingual-rag-pipeline

SUMMARY
Applied AI and Machine Learning Engineer specializing in multilingual NLP, vector retrieval architectures, and transformer fine-tuning.

TECHNICAL SKILLS
Core AI/ML: PyTorch, TensorFlow, Scikit-Learn, Hugging Face Transformers, LangChain, FAISS
Languages: Python, C++, SQL
Data & Cloud: Pandas, NumPy, FastAPI, Docker, GCP Vertex AI, MLflow

PROJECTS
1. Multilingual RAG Retrieval Pipeline
- Built an enterprise semantic search and question-answering pipeline supporting 5 Indian languages.
- Optimized vector embedding latency using FAISS indexing with hierarchical navigable small-world graphs.
""", encoding='utf-8')

# 3. DevOps Resume
(fixtures_dir / 'resume_devops.txt').write_text("""Priya Venkatesh
Site Reliability & DevOps Engineer
Email: priya.v@example.com
GitHub: https://github.com/ops-lead/k8s-multi-cluster-helm

SUMMARY
SRE with deep expertise in Kubernetes orchestration, infrastructure as code with Terraform, and highly resilient CI/CD pipelines.

TECHNICAL SKILLS
Infrastructure & Cloud: Kubernetes, Docker, Terraform, AWS, Helm, Linux, Ansible
Monitoring & SRE: Prometheus, Grafana, OpenTelemetry, ELK Stack
Languages: Python, Go, Shell Scripting

PROJECTS
1. Multi-Cluster Kubernetes Helm Automation
- Developed Helm charts and Terraform modules for multi-tenant EKS clusters with automated autoscaling.
- Implemented zero-downtime rolling upgrades and robust disaster recovery automation.
""", encoding='utf-8')

# 4. Create Project Zips
def make_zip(zip_name, files):
    z_path = fixtures_dir / zip_name
    with zipfile.ZipFile(z_path, 'w') as zf:
        for fname, content in files.items():
            zf.writestr(fname, content)
    print(f'Created {z_path.name} ({z_path.stat().st_size} bytes)')

make_zip('project_fullstack.zip', {
    'main.py': 'from fastapi import FastAPI\napp = FastAPI()\n@app.get("/health")\ndef health(): return {"status": "ok"}\n',
    'requirements.txt': 'fastapi==0.110.0\nuvicorn==0.28.0\nredis==5.0.3\npsycopg2-binary==2.9.9\n',
    'Dockerfile': 'FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nCMD ["uvicorn", "main:app"]\n'
})

make_zip('project_ml.zip', {
    'pipeline.py': 'import torch\ndef embed_text(text):\n    return [0.1, 0.2, 0.3]\n',
    'requirements.txt': 'torch==2.2.0\ntransformers==4.38.0\nfaiss-cpu==1.8.0\npandas==2.2.1\n',
    'model_config.json': '{"model_name": "multilingual-e5-base", "dimensions": 768}\n'
})

make_zip('project_devops.zip', {
    'Chart.yaml': 'apiVersion: v2\nname: microservice-helm\nversion: 1.0.0\n',
    'values.yaml': 'replicaCount: 3\nimage:\n  repository: company/api\n  tag: v1.4.2\n',
    'deployment.yaml': 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: core-api\n'
})

print('All fixtures successfully generated!')

