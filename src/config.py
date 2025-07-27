class Config:
    # Model settings
    EMBEDDING_MODEL = "/app/models/local-model"
    MAX_SECTION_LENGTH = 512
    TOP_SECTIONS = 5
    TOP_SUBSECTIONS = 5
    MIN_HEADING_LENGTH = 5  # Filter out short/non-descriptive headings
    MAX_SUBSECTION_LENGTH = 300  # Character limit for subsections
    
    # Paths
    INPUT_PATH = "/app/input"
    OUTPUT_PATH = "/app/output"