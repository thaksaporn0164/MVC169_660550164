from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.election import ElectionModel
from models.pattern_group import PatternGroupModel

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff')
def dashboard():
    # 1. ดึงข้อมูลจาก Model
    election = ElectionModel.get_info()
    status = election['status'] # ดึง status ออกมาส่งให้ View ชัดเจน
    stats = ElectionModel.get_stats()
    scores = ElectionModel.calculate_scores()
    

    pending_groups = PatternGroupModel.get_all_pending() if status == 'CLOSED' else []
    
    # ส่งข้อลูมไปฟาView
    return render_template(
        'staff_dashboard.html', 
        election=election, 
        status=status, 
        stats=stats, 
        scores=scores, 
        pending_groups=pending_groups
    )

@staff_bp.route('/staff/close', methods=['POST'])
def close_voting():
    try:
        ElectionModel.close_voting()
        flash("ปิดรับคะแนนสำเร็จ ระบบตรวจรูปแบบบัตรเรียบร้อย", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('staff.dashboard'))

@staff_bp.route('/staff/review/<int:group_id>', methods=['POST'])
def review_group(group_id):
    try:
        decision = request.form.get('decision')
        PatternGroupModel.resolve_group(group_id, decision)
        flash("บันทึกการตัดสินกลุ่มสำเร็จ", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('staff.dashboard'))