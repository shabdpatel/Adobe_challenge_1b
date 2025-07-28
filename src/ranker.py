# /Users/shabdpatel/Documents/adobe/Challenge_1b/src/ranker.py
import logging
import re
import numpy as np
from extractor import ContentExtractor
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import Config
import sys

logger = logging.getLogger(__name__)

class SemanticRanker:
    def __init__(self):
        self.model = self.load_model_with_fallback()
        
    def load_model_with_fallback(self):
        """Load model with multiple fallback strategies"""
        try:
            logger.info(f"Loading model from: {Config.EMBEDDING_MODEL}")
            return SentenceTransformer(Config.EMBEDDING_MODEL)
        except Exception as e:
            logger.error(f"Custom model loading failed: {str(e)}")
            try:
                logger.info("Loading fallback model: all-MiniLM-L6-v2")
                return SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as fallback_error:
                logger.critical(f"Fallback model failed: {str(fallback_error)}")
                sys.exit(1)

    def create_context_embedding(self, persona, job):
        context = f"As a {persona}, {job}"
        return self.model.encode([context])
    
    def rank_items(self, query_embed, items, text_fn):
        if not items:
            return []
            
        item_texts = [text_fn(item) for item in items]
        item_embeddings = self.model.encode(item_texts)
        
        similarities = cosine_similarity(query_embed, item_embeddings)[0]
        ranked_indices = np.argsort(similarities)[::-1]
        
        return [(items[i], float(similarities[i])) for i in ranked_indices]

class SectionProcessor:
    def __init__(self, ranker):
        self.ranker = ranker
        
    def process_document(self, doc_path, outline, persona, job):
        headings = ContentExtractor.extract_meaningful_headings(outline, doc_path)
        if not headings:
            return []
        
        context_embed = self.ranker.create_context_embedding(persona, job)
        
        try:
            # Use heading text + first 50 chars of content
            ranked_headings = self.ranker.rank_items(
                context_embed, 
                headings,
                lambda h: f"{h['text']} {ContentExtractor.extract_section_content(doc_path, h['page'], h['page'])[:50]}"
            )
            return ranked_headings
        except Exception as e:
            logger.error(f"Error processing document {doc_path}: {str(e)}")
            return []
        
    def extract_subsections(self, section, content, persona, job):
        if not content:
            return []
            
        # Improved paragraph splitting
        paragraphs = []
        current_para = ""
        
        for line in content.split('\n'):
            stripped = line.strip()
            if not stripped:
                if current_para:
                    paragraphs.append(current_para)
                    current_para = ""
                continue
                
            # Start new paragraph for:
            # - Bullet points
            # - Numbered lists
            # - All-caps lines (potential headings)
            if (re.match(r'^(\d+\.\s|\•\s|\*\s|-)', stripped) 
                or stripped.isupper() 
                or (current_para and len(current_para) > 200)):
                if current_para:
                    paragraphs.append(current_para)
                current_para = stripped
            else:
                current_para += " " + stripped if current_para else stripped
        
        if current_para:
            paragraphs.append(current_para)
        
        # Filter paragraphs
        valid_paras = [
            p for p in paragraphs 
            if 50 < len(p) < Config.MAX_SUBSECTION_LENGTH
            and not any(term in p.lower() for term in ['copyright', 'page', 'confidential'])
        ]
        
        if not valid_paras:
            return []
        
        context_embed = self.ranker.create_context_embedding(persona, job)
        
        try:
            ranked_chunks = self.ranker.rank_items(
                context_embed,
                valid_paras,
                lambda c: c
            )
            return ranked_chunks
        except Exception as e:
            logger.error(f"Error extracting subsections: {str(e)}")
            return []