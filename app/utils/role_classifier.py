class RoleClassifier:
    def __init__(self):
        self.role_patterns = {
            'Developer': {
                'keywords': [
                    'software engineer', 'developer', 'programmer', 'full stack',
                    'backend', 'frontend', 'web developer', 'mobile developer'
                ],
                'skills': [
                    'python', 'java', 'javascript', 'react', 'angular', 'node.js',
                    'django', 'spring'
                ]
            },
            'Designer': {
                'keywords': [
                    'ui designer', 'ux designer', 'product designer', 'web designer',
                    'graphic designer', 'visual designer'
                ],
                'skills': [
                    'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
                    'indesign', 'ui/ux'
                ]
            },
            'Data Scientist': {
                'keywords': [
                    'data scientist', 'machine learning', 'ai engineer',
                    'data analyst', 'research scientist'
                ],
                'skills': [
                    'python', 'r', 'tensorflow', 'pytorch', 'scikit-learn',
                    'pandas', 'numpy'
                ]
            },
            'Manager': {
                'keywords': [
                    'project manager', 'team lead', 'engineering manager',
                    'technical lead', 'product manager'
                ],
                'skills': [
                    'leadership', 'management', 'agile', 'scrum', 'team building',
                    'strategy'
                ]
            }
        }

    def classify_role(self, text, skills):
        text = text.lower()
        role_scores = {role: 0 for role in self.role_patterns}
        
        # Score based on keywords
        for role, patterns in self.role_patterns.items():
            for keyword in patterns['keywords']:
                if keyword.lower() in text:
                    role_scores[role] += 2
            
            for skill in patterns['skills']:
                if any(s.lower() == skill for s in skills):
                    role_scores[role] += 1
        
        # Get the role with highest score
        max_score = max(role_scores.values())
        if max_score > 0:
            return max(role_scores.items(), key=lambda x: x[1])[0]
        
        return "Other"