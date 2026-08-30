from database.db_manager import get_db

class ElectionModel:
    @staticmethod
    def get_info():
        return get_db().execute("SELECT * FROM election LIMIT 1").fetchone()

    @staticmethod
    def close_voting():
        db = get_db()
        cursor = db.cursor()
        election = ElectionModel.get_info()
        
        if election['status'] != 'OPEN':
            raise Exception("การเลือกตั้งไม่ได้เปิดอยู่")
            
        cursor.execute("UPDATE election SET status = 'CLOSED' WHERE id = ?", (election['id'],))
        
        threshold = election['duplicate_threshold']
        cursor.execute("SELECT rank1, rank2, rank3, COUNT(*) as c FROM ballots WHERE status = 'SUBMITTED' GROUP BY rank1, rank2, rank3")
        patterns = cursor.fetchall()
        
        for p in patterns:
            if p['c'] >= threshold:
                pattern_str = f"{p['rank1']} > {p['rank2']} > {p['rank3']}"
                cursor.execute("INSERT INTO pattern_groups (pattern_str, status) VALUES (?, 'PENDING')", (pattern_str,))
                group_id = cursor.lastrowid
                cursor.execute('''UPDATE ballots SET status = 'PENDING_REVIEW', group_id = ? 
                                  WHERE rank1 = ? AND rank2 = ? AND rank3 = ? AND status = 'SUBMITTED'
                               ''', (group_id, p['rank1'], p['rank2'], p['rank3']))
            else:
                cursor.execute('''UPDATE ballots SET status = 'APPROVED'
                                  WHERE rank1 = ? AND rank2 = ? AND rank3 = ? AND status = 'SUBMITTED'
                               ''', (p['rank1'], p['rank2'], p['rank3']))
        db.commit()
        ElectionModel.check_and_finalize() # เผื่อปิดหีบแล้วไม่มีกลุ่มทุจริตเลยให้จบเลย

    @staticmethod
    def check_and_finalize():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT count(*) as c FROM pattern_groups WHERE status = 'PENDING'")
        if cursor.fetchone()['c'] == 0:
            cursor.execute("UPDATE election SET status = 'FINALIZED'")
        db.commit()

    @staticmethod
    def calculate_scores():
        db = get_db()
        cursor = db.cursor()
        election = ElectionModel.get_info()
        p1, p2, p3 = election['point_rank1'], election['point_rank2'], election['point_rank3']
        
        cursor.execute("SELECT id, name FROM candidates")
        scores = {row['id']: {'name': row['name'], 'score': 0} for row in cursor.fetchall()}
        
        cursor.execute("SELECT rank1, rank2, rank3 FROM ballots WHERE status = 'APPROVED'")
        for b in cursor.fetchall():
            if b['rank1'] in scores: scores[b['rank1']]['score'] += p1
            if b['rank2'] in scores: scores[b['rank2']]['score'] += p2
            if b['rank3'] in scores: scores[b['rank3']]['score'] += p3
            
        return dict(sorted(scores.items(), key=lambda item: item[1]['score'], reverse=True))

    @staticmethod
    def get_stats():
        db = get_db()
        return {
            'total_received': db.execute("SELECT count(*) FROM ballots").fetchone()[0],
            'total_approved': db.execute("SELECT count(*) FROM ballots WHERE status = 'APPROVED'").fetchone()[0],
            'total_rejected': db.execute("SELECT count(*) FROM ballots WHERE status = 'REJECTED'").fetchone()[0],
            'total_pending': db.execute("SELECT count(*) FROM ballots WHERE status = 'PENDING_REVIEW'").fetchone()[0]
        }