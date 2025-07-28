# /Users/shabdpatel/Documents/adobe/Challenge_1b/src/process_documents.py
import os
import time
import json
import re
import logging
import traceback
from ranker import SemanticRanker, SectionProcessor
from extractor import ContentExtractor
from utils import load_json, save_json, get_timestamp
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("processing.log")
    ]
)
logger = logging.getLogger(__name__)

def main():
    start_time = time.time()
    logger.info("========== STARTING CHALLENGE 1B PROCESSING ==========")
    
    try:
        # Verify input/output directories
        input_dir = Config.INPUT_PATH
        output_dir = Config.OUTPUT_PATH
        
        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Contents of input directory: {os.listdir(input_dir)}")
        
        # Create output directory if not exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Load input specification
        input_path = os.path.join(input_dir, "challenge1b_input.json")
        if not os.path.exists(input_path):
            logger.error(f"Missing input file: {input_path}")
            return
            
        logger.info(f"Loading input from: {input_path}")
        input_data = load_json(input_path)
        logger.info(f"Persona: {input_data['persona']['role']}")
        logger.info(f"Job: {input_data['job_to_be_done']['task']}")
        logger.info(f"Documents to process: {len(input_data['documents'])}")
        
        # Initialize components
        ranker = SemanticRanker()
        processor = SectionProcessor(ranker)
        
        # Process all documents
        all_sections = []
        for doc in input_data["documents"]:
            doc_filename = doc["filename"]
            logger.info(f"Processing document: {doc_filename}")
            
            # Get outline path
            doc_name = os.path.splitext(doc_filename)[0]
            outline_path = os.path.join(input_dir, f"{doc_name}.json")
            pdf_path = os.path.join(input_dir, doc_filename)
            
            logger.info(f"Outline path: {outline_path}")
            logger.info(f"PDF path: {pdf_path}")
            
            # Verify files exist
            if not os.path.exists(outline_path):
                logger.error(f"Outline not found: {outline_path}")
                continue
                
            if not os.path.exists(pdf_path):
                logger.error(f"PDF not found: {pdf_path}")
                continue
                
            # Load outline
            outline = load_json(outline_path)
            logger.info(f"Outline loaded: {len(outline.get('outline', []))} headings")
            
            # Process document
            sections = processor.process_document(
                pdf_path,
                outline,
                input_data["persona"]["role"],
                input_data["job_to_be_done"]["task"]
            )
            logger.info(f"Found {len(sections)} relevant sections")
            
            for section, score in sections:
                all_sections.append({
                    "document": doc_filename,
                    "section": section,
                    "score": score
                })
        
        # Rank all sections across documents
        all_sections.sort(key=lambda x: x["score"], reverse=True)
        top_sections = all_sections[:Config.TOP_SECTIONS]
        logger.info(f"Selected top {len(top_sections)} sections")
        
        # Prepare output
        output = {
            "metadata": {
                "input_documents": [doc["filename"] for doc in input_data["documents"]],
                "persona": input_data["persona"]["role"],
                "job_to_be_done": input_data["job_to_be_done"]["task"],
                "processing_timestamp": get_timestamp()
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        
        # Process top sections and extract subsections
        for rank, item in enumerate(top_sections, start=1):
            section = item["section"]
            doc_path = os.path.join(input_dir, item["document"])
            content = ContentExtractor.extract_section_content(
                doc_path,
                section["page"],
                section.get("end_page")
            )
            
            # Add to extracted sections
            output["extracted_sections"].append({
                "document": item["document"],
                "section_title": section["text"],
                "importance_rank": rank,
                "page_number": section["page"]
            })
            
            # Extract and add subsections
            subsections = processor.extract_subsections(
                section,
                content,
                input_data["persona"]["role"],
                input_data["job_to_be_done"]["task"]
            )
            
            # Add unique subsections
            seen_texts = set()
            added_count = 0
            for sub, score in subsections:
                if added_count >= Config.TOP_SUBSECTIONS:
                    break
                    
                # Clean text
                clean_text = re.sub(r'\s+', ' ', sub).strip()
                if clean_text and clean_text not in seen_texts:
                    seen_texts.add(clean_text)
                    output["subsection_analysis"].append({
                        "document": item["document"],
                        "refined_text": clean_text,
                        "page_number": section["page"]
                    })
                    added_count += 1
            
            logger.info(f"Extracted {added_count} subsections for '{section['text']}'")
        
        # Save output
        output_path = os.path.join(output_dir, "output.json")
        save_json(output, "output.json")
        logger.info(f"Output saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        duration = time.time() - start_time
        logger.info(f"Processing completed in {duration:.2f} seconds")

if __name__ == "__main__":
    main()