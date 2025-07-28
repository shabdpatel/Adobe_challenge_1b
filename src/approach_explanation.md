# Enhanced Persona-Driven Document Intelligence

## 🧠 Methodology

### 1. Content-Aware Processing
- Leverages the hierarchical outline structure from Challenge 1A as anchors.
- Extracts full section-wise text content using precise text segmentation.
- Automatically filters out non-descriptive or purely numeric headings (e.g., "1.", "2.") to improve semantic quality.

### 2. Hierarchical Relevance Ranking
- Creates a detailed semantic prompt:  
  _"As a [persona], your job is to [job-to-be-done]"_
- Generates contextual embeddings using a lightweight **Sentence-BERT** model (~80MB).
- Scores each section by combining heading and content similarity to the persona context.
- Dives deeper into ranked sections by performing paragraph-level semantic similarity checks.

### 3. Cross-Document Analysis
- Processes **all PDFs** in the input directory.
- Compares and ranks sections across document boundaries.
- Selects the **top 5 semantically relevant sections** from the entire collection.

### 4. Subsection Extraction
- Breaks down each selected section into coherent paragraphs.
- Re-ranks paragraphs within each section based on persona relevance.
- Outputs the **top 5 most relevant subsections** as a final step.

---

## 🚀 Key Enhancements

- **✅ Content Enrichment**  
  Goes beyond headings—extracts and understands full section content.

- **🚫 Noise Filtering**  
  Automatically skips headings with low semantic value (e.g., short or numeric).

- **🔍 Contextual Understanding**  
  Persona + Job prompt boosts semantic relevance.

- **⚡ Lightweight & Efficient**  
  - Embedding model size: **80MB**  
  - Fast processing: **< 60 seconds** for 10 documents

---

## 🔒 Compliance with Hackathon Constraints

| Constraint               | Status                          |
|--------------------------|----------------------------------|
| ❌ Internet access       | Not required (offline mode)      |
| 🧠 Model size            | 330MB (**< 1GB limit**)           |
| 🖥️ CPU-only execution   | Fully compatible                 |
| ⏱️ Time limit            | < 60 seconds for 10 documents    |
| 📄 Output format         | Matches JSON spec **exactly**    |

---

## 📁 Output Structure

The final `output/result.json` contains:

```json
{
  "persona": "...",
  "job_to_be_done": "...",
  "documents": [
    {
      "document_name": "sample.pdf",
      "sections": [
        {
          "section_title": "...",
          "section_content": "...",
          "subsections": [
            "Subsection paragraph 1",
            "Subsection paragraph 2",
            ...
          ]
        },
        ...
      ]
    }
  ]
}
