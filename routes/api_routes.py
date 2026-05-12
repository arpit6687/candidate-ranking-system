from flask import Blueprint, request, jsonify
from models.candidate import CandidateModel
from utils.auth_decorators import login_required

api_bp = Blueprint('api_candidates', __name__, url_prefix='/api/candidates')

@api_bp.route('', methods=['GET'])
@login_required
def get_candidates():
    try:
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
        return jsonify({"status": "success", "data": candidates}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/<int:candidate_id>', methods=['GET'])
@login_required
def get_candidate(candidate_id):
    try:
        candidate = CandidateModel.get_candidate_by_id(candidate_id)
        if candidate:
            return jsonify({"status": "success", "data": candidate}), 200
        else:
            return jsonify({"status": "error", "message": "Candidate not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('', methods=['POST'])
@login_required
def add_candidate():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400

    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400

    try:
        academic_score = float(data.get('academic_score', 0))
        skills_score = float(data.get('skills_score', 0))
        experience_years = int(data.get('experience_years', 0))
        test_score = float(data.get('test_score', 0))

        new_candidate = CandidateModel.add_candidate(
            name=data['name'],
            email=data['email'],
            academic_score=academic_score,
            skills_score=skills_score,
            experience_years=experience_years,
            test_score=test_score
        )
        return jsonify({"status": "success", "message": "Candidate created", "data": new_candidate}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/<int:candidate_id>', methods=['PUT', 'PATCH'])
@login_required
def update_candidate(candidate_id):
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400

    try:
        updated_candidate = CandidateModel.update_candidate(candidate_id, data)
        if updated_candidate:
            return jsonify({"status": "success", "message": "Candidate updated", "data": updated_candidate}), 200
        else:
            return jsonify({"status": "error", "message": "Candidate not found"}), 404
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/<int:candidate_id>', methods=['DELETE'])
@login_required
def delete_candidate(candidate_id):
    try:
        candidate = CandidateModel.get_candidate_by_id(candidate_id)
        if not candidate:
            return jsonify({"status": "error", "message": "Candidate not found"}), 404
            
        CandidateModel.delete_candidate(candidate_id)
        return jsonify({"status": "success", "message": f"Candidate {candidate_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
