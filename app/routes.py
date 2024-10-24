from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from app.models import Resume
from app.utils.resume_parser import ResumeParser
from app import db

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/api/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{str(uuid.uuid4())}.{file_extension}"
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Parse resume
        parser = ResumeParser()
        parsed_data = parser.parse_file(file_path, file_extension)
        
        # Create resume record
        resume = Resume(
            filename=unique_filename,
            original_filename=filename,
            file_type=file_extension,
            role_category=parsed_data['role_category'],
            total_experience=parsed_data['total_experience'],
            skills=parsed_data['skills'],
            education=parsed_data['education']
        )
        
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'resume_id': resume.id,
            'parsed_data': parsed_data
        }), 201
    
    return jsonify({'error': 'File type not allowed'}), 400

@main.route('/api/resumes', methods=['GET'])
def get_resumes():
    resumes = Resume.query.all()
    return jsonify([resume.to_dict() for resume in resumes])

@main.route('/api/resume/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    return jsonify(resume.to_dict())

@main.route('/api/resume/<int:resume_id>/status', methods=['PUT'])
def update_resume_status(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    data = request.get_json()
    
    if 'status' in data:
        resume.status = data['status']
    if 'feedback' in data:
        resume.feedback = data['feedback']
    
    db.session.commit()
    return jsonify(resume.to_dict())

@main.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    total_resumes = Resume.query.count()
    status_breakdown = db.session.query(
        Resume.status, db.func.count(Resume.id)
    ).group_by(Resume.status).all()
    
    role_distribution = db.session.query(
        Resume.role_category, db.func.count(Resume.id)
    ).group_by(Resume.role_category).all()
    
    return jsonify({
        'total_resumes': total_resumes,
        'status_breakdown': dict(status_breakdown),
        'role_distribution': dict(role_distribution)
    })