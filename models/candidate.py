import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class CandidateModel:
    @staticmethod
    def _calculate_total_score(academic, skills, experience, test):
        # Normalize to 0-100 scale before weighting
        norm_academic = max(0, min(float(academic), 100))
        norm_skills = max(0, min(float(skills), 100))
        norm_test = max(0, min(float(test), 100))
        
        # Normalize experience: 20 years = 100 score
        norm_exp = max(0, min(int(experience) * 5, 100))
        
        # Weightings: academic_score (30%), skills_score (30%), experience (20%), test_score (20%)
        total = (norm_academic * 0.30) + (norm_skills * 0.30) + (norm_exp * 0.20) + (norm_test * 0.20)
        return total

    @staticmethod
    def get_all_candidates(min_skills=None, min_experience=None, min_score=None, max_score=None, sort_by='rank', sort_order='asc'):
        conn = get_db_connection()
        query = "SELECT * FROM candidates WHERE 1=1"
        params = []
        
        if min_skills is not None:
            query += " AND skills_score >= ?"
            params.append(min_skills)
        if min_experience is not None:
            query += " AND experience_years >= ?"
            params.append(min_experience)
        if min_score is not None:
            query += " AND total_score >= ?"
            params.append(min_score)
        if max_score is not None:
            query += " AND total_score <= ?"
            params.append(max_score)
            
        valid_sort_columns = ['rank', 'name', 'academic_score', 'skills_score', 'experience_years', 'test_score', 'total_score']
        if sort_by not in valid_sort_columns:
            sort_by = 'rank'
            
        sort_order = "DESC" if str(sort_order).lower() == 'desc' else "ASC"
        
        query += f" ORDER BY {sort_by} {sort_order}"
        
        candidates = conn.execute(query, tuple(params)).fetchall()
        conn.close()
        
        cands_dict = [dict(ix) for ix in candidates]
        
        # Dynamically calculate ML predictive scoring
        from ml.model import predictor
        predictor.train_model(cands_dict)
        
        for c in cands_dict:
            ml_pred = predictor.predict(c['academic_score'], c['skills_score'], c['experience_years'], c['test_score'])
            c['ml_score'] = round(ml_pred, 2) if ml_pred is not None else "N/A"
            
        return cands_dict

    @staticmethod
    def get_candidate_by_id(candidate_id):
        conn = get_db_connection()
        candidate = conn.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,)).fetchone()
        conn.close()
        return dict(candidate) if candidate else None

    @staticmethod
    def add_candidate(name, email, academic_score, skills_score, experience_years, test_score):
        total_score = CandidateModel._calculate_total_score(academic_score, skills_score, experience_years, test_score)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO candidates (name, email, academic_score, skills_score, experience_years, test_score, total_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, academic_score, skills_score, experience_years, test_score, total_score))
            new_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError("Candidate with this email already exists.")
        conn.close()
        
        # After adding, recalculate ranks
        CandidateModel.recalculate_ranks()
        return CandidateModel.get_candidate_by_id(new_id)

    @staticmethod
    def update_candidate(candidate_id, data):
        conn = get_db_connection()
        cursor = conn.cursor()

        current = CandidateModel.get_candidate_by_id(candidate_id)
        if not current:
            conn.close()
            return None

        update_fields = []
        params = []

        if 'name' in data:
            update_fields.append("name = ?")
            params.append(data['name'])
        if 'email' in data:
            update_fields.append("email = ?")
            params.append(data['email'])

        update_scores = False
        
        # Check if we need to update score metrics
        score_keys = ['academic_score', 'skills_score', 'experience_years', 'test_score']
        if any(k in data for k in score_keys):
            try:
                academic_score = float(data.get('academic_score', current['academic_score']))
                skills_score = float(data.get('skills_score', current['skills_score']))
                experience_years = int(data.get('experience_years', current['experience_years']))
                test_score = float(data.get('test_score', current['test_score']))
            except ValueError:
                conn.close()
                raise ValueError("Invalid score inputs. Must be numbers.")

            total_score = CandidateModel._calculate_total_score(academic_score, skills_score, experience_years, test_score)
            
            update_fields.append("academic_score = ?")
            params.append(academic_score)
            update_fields.append("skills_score = ?")
            params.append(skills_score)
            update_fields.append("experience_years = ?")
            params.append(experience_years)
            update_fields.append("test_score = ?")
            params.append(test_score)
            update_fields.append("total_score = ?")
            params.append(total_score)
            update_scores = True

        if not update_fields:
            conn.close()
            return current

        query = f"UPDATE candidates SET {', '.join(update_fields)} WHERE id = ?"
        params.append(candidate_id)

        try:
            cursor.execute(query, tuple(params))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError("Email already exists")
            
        conn.close()

        if update_scores:
            CandidateModel.recalculate_ranks()

        return CandidateModel.get_candidate_by_id(candidate_id)

    @staticmethod
    def delete_candidate(candidate_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM candidates WHERE id = ?', (candidate_id,))
        conn.commit()
        conn.close()
        
        # After deleting, recalculate ranks
        CandidateModel.recalculate_ranks()

    @staticmethod
    def recalculate_ranks():
        conn = get_db_connection()
        # Get all candidates sorted by total_score descending
        candidates = conn.execute('SELECT id, total_score FROM candidates ORDER BY total_score DESC').fetchall()
        
        current_rank = 1
        previous_score = None
        
        # Update rank handling ties appropriately (Standard Competition Ranking)
        for index, candidate in enumerate(candidates):
            if candidate['total_score'] != previous_score:
                current_rank = index + 1
                
            conn.execute('UPDATE candidates SET rank = ? WHERE id = ?', (current_rank, candidate['id']))
            previous_score = candidate['total_score']
            
        conn.commit()
        conn.close()
