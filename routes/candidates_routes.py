from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.candidate import CandidateModel
from utils.auth_decorators import login_required

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route('/')
@login_required
def index():
    min_skills = request.args.get('min_skills', type=float)
    min_experience = request.args.get('min_experience', type=int)
    min_score = request.args.get('min_score', type=float)
    max_score = request.args.get('max_score', type=float)
    sort_by = request.args.get('sort_by', 'rank')
    sort_order = request.args.get('sort_order', 'asc')
    
    candidates = CandidateModel.get_all_candidates(
        min_skills=min_skills,
        min_experience=min_experience,
        min_score=min_score,
        max_score=max_score,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return render_template('index.html', candidates=candidates)

@candidates_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_candidate():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        try:
            academic_score = float(request.form.get('academic_score', 0))
            skills_score = float(request.form.get('skills_score', 0))
            experience_years = int(request.form.get('experience_years', 0))
            test_score = float(request.form.get('test_score', 0))
            
            CandidateModel.add_candidate(
                name=name,
                email=email,
                academic_score=academic_score,
                skills_score=skills_score,
                experience_years=experience_years,
                test_score=test_score
            )
            flash('Candidate added successfully!', 'success')
            return redirect(url_for('candidates.index'))
        except Exception as e:
            flash(f'Error adding candidate: {str(e)}', 'error')
            
    return render_template('add_candidate.html')

@candidates_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_candidate(id):
    try:
        CandidateModel.delete_candidate(id)
        flash('Candidate deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting candidate: {str(e)}', 'error')
    return redirect(url_for('candidates.index'))
