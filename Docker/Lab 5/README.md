# Lab 5: Docker Image Vulnerability Scanning & Remediation with Trivy

This repository demonstrates security scanning of Docker container images using **Aqua Security Trivy**, analyzing detected vulnerabilities (CVEs), generating audit reports, and performing **vulnerability remediation** to achieve zero HIGH and CRITICAL vulnerabilities.

---

## 📌 Project Overview
- **Application:** Node.js Express REST API
- **Original Base Image:** `node:18-bullseye`
- **Security Scanner:** [Trivy](https://trivy.dev/)
- **Target:** Detect and remediate OS-level and application dependency vulnerabilities.

---

## 🚀 Lab Objectives & Tasks
1. Clone the vulnerable application repository.
2. Build the baseline Docker image tagged as `trivy-lab:v1`.
3. Install and verify **Trivy** vulnerability scanner.
4. Scan `trivy-lab:v1` and filter for **HIGH** and **CRITICAL** vulnerabilities.
5. Generate an interactive **HTML vulnerability report** (`report-v1.html`).
6. **Remediation (Bonus):**
   - Identify root causes of reported CVEs.
   - Upgrade the base image to an audited, minimal Alpine runtime (`node:20-alpine`).
   - Update vulnerable NPM dependencies in `package.json`.
   - Implement non-root user execution (`USER node`).
   - Rebuild image as `ivolve-app:v2` and generate `report-v2.html`.
   - Verify that **0 HIGH** and **0 CRITICAL** vulnerabilities remain.

---

## 🛠️ Step-by-Step Implementation

### Step 1: Clone the Application
```bash
git clone https://github.com/Ibrahim-Adel15/TrivyImage.git
cd TrivyImage

### Step 2: Build the Baseline Image (trivy-lab:v1)

Build the initial image using the provided Dockerfile:

```bash
docker build -t trivy-lab:v1 .
