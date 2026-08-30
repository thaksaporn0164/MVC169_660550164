from database.db_manager import get_db

class VoterModel:
    @staticmethod
    def get_all(): 
        return get_db().execute("SELECT * FROM voters").fetchall()