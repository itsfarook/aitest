import spacy
from .file_handlers import FileHandler
from .skills_extractor import SkillsExtractor
from .education_extractor import EducationExtractor
from .experience_extractor import ExperienceExtractor
from .role_classifier import RoleClassifier

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.file_handler = FileHandler()
        self.skills_extractor = SkillsExtractor()
        self.education_extractor = EducationExtractor(self.nlp)
        self.experience_extractor = ExperienceExtractor()
        self.role_classifier = RoleClassifier()

    def parse_file(self, file_path, file_extension):
        # Extract text based on file type
        if file_extension == 'pdf':
            text = self.file_handler.extract_text_from_pdf(file_path)
        elif file_extension == 'docx':
            text = self.file_handler.extract_text_from_docx(file_path)
        else:  # jpg, jpeg
            text = self.file_handler.extract_text_from_image(file_path)

        # Parse the extracted text
        return self._analyze_text(text)

    def _analyze_text(self, text):
        # Extract skills
        skills_by_category = self.skills_extractor.extract_skills(text)
        all_skills = [skill for category in skills_by_category.values() for skill in category]
        
        # Extract education
        education = self.education_extractor.extract_education(text)
        
        # Extract experience
        experience = self.experience_extractor.extract_experience(text)
        
        # Classify role
        role = self.role_classifier.classify_role(text, all_skills)
        
        return {
            'skills': skills_by_category,
            'education': education,
            'total_experience': experience,
            'role_category': role
        }