import sqlite3
import datetime

# 우리가 만든 데이터베이스 파일 이름
DB_NAME = 'workout.db'

# --- 1. 신경 전달 보조 함수 (Helper) ---
def run_query(query, parameters=()):
    """
    DB에 SQL 명령을 전달하고 저장을 수행하는 함수입니다.
    반복되는 연결(Connect) -> 실행(Execute) -> 저장(Commit) 과정을 자동화합니다.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()
        return cursor

# --- 2. 운동 종목 관리 (Exercises) ---
def add_exercise(name, part, equipment):
    """
    새로운 운동 종목을 등록합니다. (예: 벤치프레스)
    """
    query = "INSERT INTO exercises (name, part, equipment) VALUES (?, ?, ?)"
    run_query(query, (name, part, equipment))
    print(f"System: [{name}] 운동이 등록되었습니다.")

def get_exercises():
    """
    등록된 모든 운동 목록을 가져옵니다.
    나중에 앱 화면에서 선택 리스트를 만들 때 사용됩니다.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, equipment FROM exercises")
        return cursor.fetchall() # 모든 결과를 리스트 형태로 반환

# --- 3. 운동 세션 관리 (Sessions) ---
def create_session(memo=""):
    """
    운동 시작을 알립니다.
    반환값: 새로 생성된 세션의 고유 ID (이 ID가 있어야 세트를 기록할 수 있습니다)
    """
    query = "INSERT INTO sessions (memo) VALUES (?)"
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (memo,))
        conn.commit()
        new_id = cursor.lastrowid # 방금 만들어진 ID 추출
        print(f"System: 새로운 운동 세션(ID: {new_id})이 시작되었습니다.")
        return new_id

# --- 4. 세트 기록 관리 (Sets) ---
def add_set(session_id, exercise_id, weight, reps, set_order, rest_seconds=60):
    """
    실제 운동 수행(세트)을 기록합니다.
    """
    query = '''
        INSERT INTO sets (session_id, exercise_id, weight, reps, set_order, rest_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    run_query(query, (session_id, exercise_id, weight, reps, set_order, rest_seconds))
    print(f"System: 기록 완료 -> {weight}kg x {reps}회 ({set_order}세트)")

# --- [테스트 구역] ---
# 이 파일이 직접 실행될 때만 작동하는 코드입니다.
if __name__ == "__main__":
    print("--- 임상 실험 시작 (Simulation Start) ---")
    
    # 1. 운동 종목 등록 (처음 한 번만 필요하지만 테스트를 위해 실행)
    add_exercise("Squat", "Legs", "Barbell")
    add_exercise("Bench Press", "Chest", "Barbell")
    
    # 2. 운동 종목 잘 들어갔는지 확인 (Read)
    exercises = get_exercises()
    print(f"등록된 운동 목록: {exercises}")
    
    # 3. 오늘 운동 시작 (세션 생성)
    # 가정: 목록의 첫 번째 운동(Squat)을 한다고 가정
    today_session_id = create_session("컨디션 좋음, 무릎 주의")
    squat_id = exercises[0][0] # 스쿼트의 ID (보통 1번)
    
    # 4. 세트 기록 (1세트: 100kg 5회)
    add_set(today_session_id, squat_id, 100, 5, 1, 180)
    
    # 5. 세트 기록 (2세트: 100kg 5회)
    add_set(today_session_id, squat_id, 100, 5, 2, 180)
    
    print("--- 임상 실험 종료 (Simulation End) ---")