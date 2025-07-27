
# Challenge 1B: Persona-Driven Document Intelligence

## Solution Overview
Enhances Challenge 1A outlines with full content extraction and semantic ranking based on persona context.

## Execution Requirements
1. Challenge 1A must be run first to generate outline JSONs
2. Place all PDFs and their JSON outlines in the input directory
3. Include `challenge1b_input.json` in input directory

## Build & Run
```bash
# Build Docker image
docker build --platform linux/amd64 -t persona-doc-intel:latest .

# Run container
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intel:latest
Output
Generates output.json in specified format

Includes ranked sections and subsections

text

### Key Improvements Over Basic Approach:

1. **Content Enrichment**:
   - Uses full text content instead of just headings
   - Overcomes limitations of poor heading extraction
   - Provides richer context for semantic matching

2. **Noise Filtering**:
   - Automatically ignores non-descriptive headings ("1.", "2.", "Designation")
   - Focuses on meaningful content sections

3. **Hierarchical Processing**:
   - First ranks sections across all documents
   - Then extracts relevant subsections from top sections
   - Maintains document context throughout

4. **Efficiency Optimizations**:
   - Processes documents sequentially to minimize memory usage
   - Uses paragraph-level chunking for subsection analysis
   - Lightweight model meets all size constraints

This solution addresses the limitations shown in the Challenge 1A output while meeting all requirements for Challenge 1B. The Docker setup ensures easy execution in the constrained environment, and the semantic approach provides persona-relevant results.
