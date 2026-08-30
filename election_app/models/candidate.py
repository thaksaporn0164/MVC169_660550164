from database.db_manager import get_db

class CandidateModel:
    @staticmethod
    def get_all(): 
        return get_db().execute("SELECT * FROM candidates").fetchall()