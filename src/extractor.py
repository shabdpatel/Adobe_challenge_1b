import fitz
import re
import logging
from config import Config

logger = logging.getLogger(__name__)

class ContentExtractor:
    @staticmethod
    def get_total_pages(pdf_path):
        """Get total number of pages in PDF"""
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            doc.close()
            return total_pages
        except Exception as e:
            logger.error(f"Error getting page count for {pdf_path}: {str(e)}")
            return 0

    @staticmethod
    def extract_section_content(pdf_path, start_page, end_page=None):
        """Extract content between start_page and end_page"""
        try:
            doc = fitz.open(pdf_path)
            if end_page is None:
                end_page = start_page
                
            content = []
            for page_num in range(start_page-1, min(end_page, len(doc))):
                page = doc.load_page(page_num)
                text = page.get_text("text", sort=True)
                content.append(text)
            
            doc.close()
            return "\n\n".join(content)
        except Exception as e:
            logger.error(f"Error extracting content from {pdf_path}: {str(e)}")
            return ""

    @staticmethod
    def extract_meaningful_headings(outline, pdf_path):
        headings = []
        total_pages = ContentExtractor.get_total_pages(pdf_path)

        # Add title as special section
        headings.append({
            "text": outline.get("title", "Untitled"),
            "level": "H0",
            "page": 1
        })

        # Less aggressive filtering
        for item in outline.get("outline", []):
            text = item.get("text", "").strip()
            if len(text) < Config.MIN_HEADING_LENGTH:
                continue

            # Keep headings that start with bullet points (common in outlines)
            if text.startswith(('•', '-', '*')):
                text = text[1:].strip()  # Remove bullet but keep text

            headings.append({
                "text": text,
                "level": item.get("level", "H1"),
                "page": item.get("page", 1)
            })

        # Add end pages for section content extraction
        for i in range(len(headings)):
            if i < len(headings) - 1:
                headings[i]["end_page"] = headings[i+1]["page"] - 1
            else:
                headings[i]["end_page"] = total_pages

        return headings  # REMOVED THE EXTRA DOT HERE