import flet as ft
import db_utils
from datetime import datetime

def main(page: ft.Page):
    # --- 1. 기본 환경 설정 ---
    page.title = "My Workout App"
    page.window_width = 360
    page.window_height = 800
    page.scroll = "auto"
    
    # 앱이 켜지자마자 새로운 세션을 시작합니다. (자동 로그인 개념)
    # 실제 앱에서는 '운동 시작' 버튼을 눌렀을 때 생성하는 것이 좋으나, 지금은 단순화를 위해 자동 생성합니다.
    current_session_id = db_utils.create_session(f"접속 시간: {datetime.now().strftime('%H:%M')}")

    # --- 2. 데이터 로드 (Data Fetching) ---
    # DB에 저장된 운동 목록을 가져옵니다.
    exercises_data = db_utils.get_exercises() # [(1, 'Squat', 'Barbell'), (2, 'Bench', ...)]
    
    # 가져온 데이터를 드롭다운 옵션으로 변환합니다.
    # key는 DB의 ID, text는 화면에 보일 이름입니다.
    exercise_options = [ft.dropdown.Option(key=str(ex[0]), text=f"{ex[1]} ({ex[2]})") for ex in exercises_data]

    # 만약 등록된 운동이 하나도 없다면 경고 옵션을 넣습니다.
    if not exercise_options:
        exercise_options.append(ft.dropdown.Option(key="-1", text="운동을 먼저 등록하세요"))

    # --- 3. [Tab 1] 운동 기록 UI 요소 ---
    dd_exercise = ft.Dropdown(label="운동 선택", options=exercise_options)
    txt_weight = ft.TextField(label="무게 (kg)", width=100, keyboard_type="number")
    txt_reps = ft.TextField(label="횟수 (reps)", width=100, keyboard_type="number")
    
    # 기록된 세트를 보여줄 리스트뷰 (차트)
    lv_history = ft.ListView(expand=True, spacing=10)

    def add_set_click(e):
        try:
            # 유효성 검사
            if not dd_exercise.value or dd_exercise.value == "-1":
                page.snack_bar = ft.SnackBar(ft.Text("운동을 선택해주세요!"))
                page.snack_bar.open = True
                page.update()
                return

            ex_id = int(dd_exercise.value)
            weight = float(txt_weight.value)
            reps = int(txt_reps.value)
            
            # DB에 저장 (신경 전달)
            # set_order는 편의상 1로 고정하거나 추후 로직 추가. 여기선 단순히 기록만.
            db_utils.add_set(current_session_id, ex_id, weight, reps, 1)

            # 화면(차트)에 한 줄 추가
            selected_text = [opt.text for opt in exercise_options if opt.key == dd_exercise.value][0]
            lv_history.controls.append(
                ft.Text(f"V {selected_text}: {weight}kg x {reps}회", size=16, weight="bold")
            )
            
            # 입력창 초기화 및 포커스 이동
            txt_reps.value = "" 
            txt_reps.focus()
            
            page.update()
            
        except ValueError:
            # 숫자가 아닌 것을 넣었을 때 에러 방지
            page.snack_bar = ft.SnackBar(ft.Text("무게와 횟수는 숫자여야 합니다."))
            page.snack_bar.open = True
            page.update()

    btn_record = ft.ElevatedButton("세트 기록", on_click=add_set_click)

    # Tab 1 레이아웃 조립
    tab_workout = ft.Container(
        content=ft.Column([
            ft.Text("오늘의 운동", size=20, weight="bold"),
            dd_exercise,
            ft.Row([txt_weight, txt_reps]),
            btn_record,
            ft.Divider(),
            ft.Text("기록 현황 (History)"),
            lv_history
        ]),
        padding=20
    )

    # --- 4. [Tab 2] 운동 종목 추가 UI (3단계 코드 재사용) ---
    txt_new_name = ft.TextField(label="새 운동 이름")
    txt_new_part = ft.TextField(label="부위")
    dd_new_eq = ft.Dropdown(label="장비", options=[
        ft.dropdown.Option("Barbell"), ft.dropdown.Option("Dumbbell"), ft.dropdown.Option("Machine")
    ])
    
    def add_exercise_click(e):
        if txt_new_name.value and dd_new_eq.value:
            db_utils.add_exercise(txt_new_name.value, txt_new_part.value, dd_new_eq.value)
            
            # 중요: 운동을 추가했으면 탭 1의 드롭다운도 갱신해줘야 함 (리로드 필요)
            page.snack_bar = ft.SnackBar(ft.Text("운동 등록 완료! 앱을 재실행하면 목록에 뜹니다."))
            page.snack_bar.open = True
            page.update()
            
            txt_new_name.value = ""

    btn_add_ex = ft.ElevatedButton("운동 등록", on_click=add_exercise_click)

    tab_manage = ft.Container(
        content=ft.Column([
            ft.Text("운동 종목 관리", size=20, weight="bold"),
            txt_new_name, txt_new_part, dd_new_eq, btn_add_ex
        ]),
        padding=20
    )

    # --- 5. 최종 탭 구성 ---
    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="운동 기록", content=tab_workout),
            ft.Tab(text="종목 관리", content=tab_manage),
        ],
        expand=1,
    )

    page.add(t)
ft.app(target=main)

