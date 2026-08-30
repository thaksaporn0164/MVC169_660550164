import sqlite3
import json

DB_CONNECTION = None

def get_db():
    global DB_CONNECTION
    if DB_CONNECTION is None:
        # เช้คว่าปิดละเปิดใหม่ได้จริงมั้ย
        DB_CONNECTION = sqlite3.connect(':memory:', check_same_thread=False)
        DB_CONNECTION.row_factory = sqlite3.Row
    return DB_CONNECTION

def init_db():
    db = get_db()
    cursor = db.cursor()
    

    cursor.executescript('''
        DROP TABLE IF EXISTS ballots;
        DROP TABLE IF EXISTS pattern_groups;
        DROP TABLE IF EXISTS officers;
        DROP TABLE IF EXISTS voters;
        DROP TABLE IF EXISTS candidates;
        DROP TABLE IF EXISTS election;
    ''')

    cursor.executescript('''
        CREATE TABLE election (
            id TEXT PRIMARY KEY,
            title TEXT,
            status TEXT NOT NULL,
            point_rank1 INTEGER,
            point_rank2 INTEGER,
            point_rank3 INTEGER,
            duplicate_threshold INTEGER
        );
        CREATE TABLE candidates (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE voters (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            has_voted INTEGER DEFAULT 0
        );
        CREATE TABLE officers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE pattern_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_str TEXT NOT NULL,
            status TEXT NOT NULL
        );
        CREATE TABLE ballots (
            id TEXT PRIMARY KEY,
            voter_id TEXT NOT NULL,
            rank1 TEXT NOT NULL,
            rank2 TEXT NOT NULL,
            rank3 TEXT NOT NULL,
            status TEXT NOT NULL,
            group_id INTEGER,
            FOREIGN KEY(voter_id) REFERENCES voters(id),
            FOREIGN KEY(group_id) REFERENCES pattern_groups(id)
        );
    ''')
    

    with open('seed_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    e = data['election']
    cursor.execute('''
        INSERT INTO election (id, title, status, point_rank1, point_rank2, point_rank3, duplicate_threshold)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (e['id'], e['title'], e['status'], e['ranking_points'][0], e['ranking_points'][1], e['ranking_points'][2], e['duplicate_pattern_threshold']))
    
    for o in data.get('officers', []):
        cursor.execute("INSERT INTO officers (id, name) VALUES (?, ?)", (o['id'], o['name']))
        
    for c in data['candidates']:
        cursor.execute("INSERT INTO candidates (id, name) VALUES (?, ?)", (c['id'], c['name']))
        
    for v in data['voters']:
        cursor.execute("INSERT INTO voters (id, name, active) VALUES (?, ?, ?)", 
                       (v['id'], v['name'], 1 if v['active'] else 0))
                       
    for b in data['ballots']:
        cursor.execute('''
            INSERT INTO ballots (id, voter_id, rank1, rank2, rank3, status)
            VALUES (?, ?, ?, ?, ?, 'SUBMITTED')
        ''', (b['id'], b['voter_id'], b['ranking'][0], b['ranking'][1], b['ranking'][2]))
        cursor.execute("UPDATE voters SET has_voted = 1 WHERE id = ?", (b['voter_id'],))
        
    db.commit()