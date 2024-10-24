import re
from spacy.matcher import Matcher

class EducationExtractor:
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab)
        
        # Add education patterns
        self.education_patterns = [
            [{'LOWER': {'IN': ['bachelor', 'bachelors', 'bs', 'ba', 'b.s', 'b.a']}}],
            [{'LOWER': {'IN': ['master', 'masters', 'ms', 'ma', 'm.s', 'm.a']}}],
            [{'LOWER': {'IN': ['phd', 'ph.d', 'doctorate']}}],
            [{'LOWER': 'degree'}]
        ]
        
        for pattern in self.education_patterns:
            self.matcher.add('EDUCATION', [pattern])

    def extract_education(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        education_info = []
        for match_id, start, end in matches:
            # Get the sentence containing the education mention
            sent = next(sent for sent in doc.sents 
                       if start >= sent.start and end <= sent.end)
            education_info.append(sent.text.strip())
        
        return list(set(education_info))  # Remove duplicates