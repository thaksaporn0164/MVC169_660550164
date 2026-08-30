from flask import Blueprint, render_template
from models.candidate import CandidateModel
from models.voter import VoterModel
from models.election import ElectionModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', election=ElectionModel.get_info())

@main_bp.route('/candidates')
def candidate_list():
    return render_template('candidate_list.html', candidates=CandidateModel.get_all())

@main_bp.route('/voter_login')
def voter_login():
    return render_template('voter_login.html', voters=VoterModel.get_all())

@main_bp.route('/public_status')
def public_status():
    election = ElectionModel.get_info()
    scores = ElectionModel.calculate_scores() if election['status'] != 'OPEN' else {}
    return render_template('public_status.html', election=election, stats=ElectionModel.get_stats(), scores=scores)