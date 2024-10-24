import spacy
import json
import os

class SkillsExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skills_categories = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
                'swift', 'kotlin', 'go', 'rust'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'asp.net'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'cassandra'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
                'ansible', 'circleci', 'gitlab'
            ],
            'machine_learning': [
                'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'opencv',
                'pandas', 'numpy', 'matplotlib'
            ]
        }

    def extract_skills(self, text):
        doc = self.nlp(text.lower())
        found_skills = {category: [] for category in self.skills_categories}
        
        # Extract skills by category
        for token in doc:
            word = token.text.lower()
            for category, skills in self.skills_categories.items():
                if word in skills:
                    found_skills[category].append(word)
        
        # Remove duplicates and sort
        for category in found_skills:
            found_skills[category] = sorted(list(set(found_skills[category])))
        
        return found_skills