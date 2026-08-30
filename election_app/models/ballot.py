from database.db_manager import get_db
from models.election import ElectionModel
import uuid

class BallotModel:
    @staticmethod
    def submit_vote(voter_id, r1, r2, r3):
        if ElectionModel.get_info()['status'] != 'OPEN':
            raise Exception("การเลือกตั้งไม่ได้อยู่ในสถานะ OPEN (พยายามลงคะแนนหลังปิดรับคะแนน)")
            
        if len(set([r1, r2, r3])) != 3:
            raise Exception("ผู้สมัครในบัตรต้องแตกต่างกันทั้ง 3 อันดับ")
            
        db = get_db()
        cursor = db.cursor()
        voter = cursor.execute("SELECT has_voted, active FROM voters WHERE id = ?", (voter_id,)).fetchone()
        
        if not voter: raise Exception("ไม่พบข้อมูลผู้มีสิทธิ์")
        if voter['active'] == 0: raise Exception("ผู้มีสิทธิ์นี้ไม่ได้อยู่ในสถานะ Active")
        if voter['has_voted'] == 1: raise Exception("ผู้มีสิทธิ์นี้เคยลงคะแนนแล้ว (ห้ามลงซ้ำ)")
            
        new_id = f"B_{uuid.uuid4().hex[:6].upper()}"
        cursor.execute("INSERT INTO ballots (id, voter_id, rank1, rank2, rank3, status) VALUES (?, ?, ?, ?, ?, 'SUBMITTED')", 
                       (new_id, voter_id, r1, r2, r3))
        cursor.execute("UPDATE voters SET has_voted = 1 WHERE id = ?", (voter_id,))
        db.commit()