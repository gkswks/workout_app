import sqlite3

def init_db():
    """
    데이터베이스 초기화 함수.
    앱 실행 시 가장 먼저 호출되어 테이블이 존재하는지 확인하고,
    없으면 생성(Create)합니다.
    """
    
    # 1. 연결 (Connection): workout.db라는 파일과 연결합니다.
    # 파일이 없으면 새로 생성합니다.
    conn = sqlite3.connect('workout.db')
    
    # 2. 커서 (Cursor): DB에 명령을 전달하는 도구(메스)입니다.
    cursor = conn.cursor()

    # --- 테이블 생성 쿼리 (SQL) ---

    # A. Exercises 테이블 (운동 종목)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            part TEXT,
            equipment TEXT
        )
    ''')

    # B. Sessions 테이블 (운동 세션 - 날짜 및 메모)
    # start_time은 자동으로 현재 시간이 입력되도록 설정했습니다.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT DEFAULT CURRENT_TIMESTAMP,
            memo TEXT
        )
    ''')

    # C. Sets 테이블 (실제 수행 데이터)
    # FOREIGN KEY: 다른 테이블의 id를 참조하여 관계를 맺습니다. (신경 연결)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            exercise_id INTEGER,
            set_order INTEGER,
            weight REAL,
            reps INTEGER,
            rest_seconds INTEGER,
            FOREIGN KEY(session_id) REFERENCES sessions(id),
            FOREIGN KEY(exercise_id) REFERENCES exercises(id)
        )
    ''')

    # 3. 저장 (Commit): 수술 부위를 봉합합니다. 이 단계가 없으면 저장되지 않습니다.
    conn.commit()
    
    # 4. 연결 종료 (Close)
    conn.close()
    print("System: Database initialized successfully. (workout.db created)")

if __name__ == "__main__":
    init_db()