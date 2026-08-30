from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.candidate import CandidateModel
from models.ballot import BallotModel
from models.election import ElectionModel

voter_bp = Blueprint('voter', __name__)

@voter_bp.route('/vote/<voter_id>')
def vote_page(voter_id):
    return render_template('voter_vote.html', voter_id=voter_id, candidates=CandidateModel.get_all(), status=ElectionModel.get_info()['status'])

@voter_bp.route('/vote/submit', methods=['POST'])
def submit_vote():
    voter_id = request.form.get('voter_id')
    try:
        BallotModel.submit_vote(voter_id, request.form.get('rank1'), request.form.get('rank2'), request.form.get('rank3'))
        flash("ลงคะแนนสำเร็จ!", "success")
        return redirect(url_for('main.index'))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('voter.vote_page', voter_id=voter_id))