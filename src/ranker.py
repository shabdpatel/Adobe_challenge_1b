import logging
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import Config

logger = logging.getLogger(__name__)

class SemanticRanker:
    def __init__(self):
        logger.info(f"Loading model from: {Config.EMBEDDING_MODEL}")
        try:
            self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
            logger.info(f"Model loaded: {self.model.get_sentence_embedding_dimension()} dimensions")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise

    def create_context_embedding(self, persona, job):
        context = f"As a {persona}, {job}"
        return self.model.encode([context])
    
    def rank_items(self, query_embed, items, text_fn):
        """Generic ranking function for sections/subsections"""
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
        """Process a single document's outline"""
        headings = ContentExtractor.extract_meaningful_headings(outline, doc_path)
        if not headings:
            logger.warning(f"No meaningful headings found in {doc_path}")
            return []
        
        context_embed = self.ranker.create_context_embedding(persona, job)
        
        try:
            # Rank headings with their content
            ranked_headings = self.ranker.rank_items(
                context_embed, 
                headings,
                lambda h: f"{h['text']}: {ContentExtractor.extract_section_content(doc_path, h['page'], h.get('end_page'))[:300]}"
            )
            return ranked_headings
        except Exception as e:
            logger.error(f"Error processing document {doc_path}: {str(e)}")
            return []
    
    def extract_subsections(self, section, content, persona, job):
        """Extract relevant subsections from section content"""
        if not content:
            return []
            
        # Split content into meaningful chunks
        chunks = []
        current_chunk = ""
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                continue
                
            # Start new chunk for bullet points or numbered lists
            if re.match(r'^(\d+\.\s|\•\s|\*\s|-)', line):
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            # Start new chunk for headings (all caps or title case)
            elif line.isupper() or line.istitle():
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += " " + line if current_chunk else line
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # Filter out short chunks
        chunks = [chunk for chunk in chunks if len(chunk) > 30 and len(chunk) < Config.MAX_SUBSECTION_LENGTH]
        
        if not chunks:
            return []
        
        context_embed = self.ranker.create_context_embedding(persona, job)
        
        try:
            ranked_chunks = self.ranker.rank_items(
                context_embed,
                chunks,
                lambda c: c
            )
            return ranked_chunks
        except Exception as e:
            logger.error(f"Error extracting subsections: {str(e)}")
            return []