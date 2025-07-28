# /Users/shabdpatel/Documents/adobe/Challenge_1b/src/config.py
class Config:
    # Model settings
    EMBEDDING_MODEL = "/app/models/local-model"
    MAX_SECTION_LENGTH = 512
    TOP_SECTIONS = 5
    TOP_SUBSECTIONS = 5
    MIN_HEADING_LENGTH = 5
    MAX_SUBSECTION_LENGTH = 1000  # Increased to accommodate paragraphs
    
    # Paths
    INPUT_PATH = "/app/input"
    OUTPUT_PATH = "/app/output"