from datetime import datetime
from app import db

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Yet to Review')
    role_category = db.Column(db.String(50))
    total_experience = db.Column(db.Float)
    skills = db.Column(db.JSON)
    education = db.Column(db.JSON)
    feedback = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'upload_date': self.upload_date.isoformat(),
            'status': self.status,
            'role_category': self.role_category,
            'total_experience': self.total_experience,
            'skills': self.skills,
            'education': self.education,
            'feedback': self.feedback
        }