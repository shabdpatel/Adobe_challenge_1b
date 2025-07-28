# Challenge 1B: Persona-Driven Document Intelligence

## 🚀 Solution Overview

This solution builds upon the output of **Challenge 1A**, extracting **full content** from PDFs and using **semantic ranking** to identify the most relevant sections and subsections based on a defined **persona** and their **job-to-be-done**.

---

## 📂 Execution Requirements

1. ✅ **Run Challenge 1A first** to generate outline `.json` files.
2. 📁 Place the following inside the `/input` directory:

   * All input PDFs
   * Their corresponding outline `.json` files
   * A `challenge1b_input.json` file containing persona and job description

---

## 🐳 Build & Run Instructions

```bash
# Build Docker image (for AMD64 platform)
docker build -t persona-doc-intel:latest .

# Run the container

docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intel:latest
```

---

## 📤 Output

* A single `output.json` file in `/output` directory
* Output Format Includes:

  * ✅ Metadata: input files, persona, job-to-be-done, timestamp
  * ✅ Extracted `sections`: ranked by semantic similarity
  * ✅ Extracted `subsections`: paragraph-level insights

---

## 🔍 Key Improvements Over Basic Outline Approach

### 1. **Content Enrichment**

* Uses **full section content**, not just titles
* Improves matching when headings are missing or generic
* Allows **contextual understanding** of PDF structure

### 2. **Noise Filtering**

* Ignores non-informative headings like:

  * "1.", "2.", "Designation", etc.
* Focuses on **meaningful and descriptive** sections

### 3. **Hierarchical Semantic Processing**

* **Stage 1**: Ranks complete sections across all documents
* **Stage 2**: Splits top sections into paragraphs → ranks them as subsections
* Retains full document + page reference for traceability

### 4. **Efficiency Optimizations**

* Lightweight model (\~80MB) embedded for persona/context matching
* CPU-only processing compliant with hackathon constraints
* Runs under 60 seconds for up to 10 documents

---

## ✅ Challenge Compliance Summary

| Constraint          | Status                           |
| ------------------- | -------------------------------- |
| 🧠 Model Size       | ✅ 330MB (< 1GB limit)             |
| ⚙️ CPU-only Runtime | ✅ Yes                            |
| 🌐 Network-Free     | ✅ Fully offline                  |
| ⏱️ Runtime          | ✅ <60 seconds (tested on 5 docs) |
| 📁 Output Format    | ✅ Matches expected spec          |

---

## 📎 Deliverables

* [x] Dockerfile (in project root)
* [x] `README.md` with clear build/run instructions
* [x] Self-contained solution with all dependencies
* [x] `approach_explanation.md` for methodology (300–500 words)

---

## 📘 Use Cases Supported

| Test Case       | Persona                      | Job-to-be-Done                                               |
| --------------- | ---------------------------- | ------------------------------------------------------------ |
| **Academic**    | PhD in Computational Biology | Literature review on GNNs in Drug Discovery                  |
| **Business**    | Investment Analyst           | Analyze R\&D and revenue trends in tech annual reports       |
| **Educational** | Chemistry Undergrad          | Extract key topics for exam prep from organic chemistry PDFs |

---

## 🔗 Inspired by the Challenge Theme

> "Connect what matters — for the user who matters."

This solution rethinks passive reading by surfacing knowledge tailored to the reader’s purpose — making document exploration truly intelligent.

