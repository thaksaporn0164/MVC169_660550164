from database.db_manager import get_db
from models.election import ElectionModel

class PatternGroupModel:
    @staticmethod
    def get_all_pending():
        return get_db().execute('''SELECT p.id, p.pattern_str, COUNT(b.id) as ballot_count 
                                   FROM pattern_groups p JOIN ballots b ON p.id = b.group_id 
                                   WHERE p.status = 'PENDING' GROUP BY p.id''').fetchall()

    @staticmethod
    def resolve_group(group_id, decision):
        db = get_db()
        cursor = db.cursor()
        
        if ElectionModel.get_info()['status'] == 'FINALIZED':
            raise Exception("พยายามแก้ผลหลังการเลือกตั้งสรุปผลแล้ว")
            
        group = cursor.execute("SELECT status FROM pattern_groups WHERE id = ?", (group_id,)).fetchone()
        if not group or group['status'] != 'PENDING':
            raise Exception("พยายามตรวจกลุ่มที่ไม่ได้อยู่ในสถานะรอตรวจสอบ")
            
        if decision not in ['APPROVED', 'REJECTED']:
            raise Exception("การตัดสินต้องเป็น รับรอง (APPROVED) หรือ ไม่นับ (REJECTED) เท่านั้น")
            
        cursor.execute("UPDATE pattern_groups SET status = ? WHERE id = ?", (decision, group_id))
        cursor.execute("UPDATE ballots SET status = ? WHERE group_id = ?", (decision, group_id))
        db.commit()
        
        ElectionModel.check_and_finalize()