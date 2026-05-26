from jobpulse.config import INCLUSION_KEYWORDS, EXCLUSION_KEYWORDS

def is_relevant_job(title: str) -> bool:
    title_lower = title.lower()
    
    # Exclusion check
    for word in EXCLUSION_KEYWORDS:
        if word in title_lower:
            return False
            
    # Inclusion check
    for word in INCLUSION_KEYWORDS:
        if word in title_lower:
            return True
            
    return False
