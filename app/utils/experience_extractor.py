import re
from datetime import datetime

class ExperienceExtractor:
    def __init__(self):
        self.experience_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'(?:worked|working)\s+(?:for|since)\s+(\d{4})',
            r'(\d{4})\s*-\s*(?:present|current|now|\d{4})',
        ]

    def extract_experience(self, text):
        text = text.lower()
        total_years = 0
        
        # Direct year mentions
        for pattern in self.experience_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                if match.group(1).isdigit():
                    if len(match.group(1)) == 4:  # Year format
                        year = int(match.group(1))
                        current_year = datetime.now().year
                        if year <= current_year:
                            total_years = max(total_years, current_year - year)
                    else:  # Direct year mention
                        total_years = max(total_years, int(match.group(1)))
        
        return float(total_years) if total_years > 0 else 0.0