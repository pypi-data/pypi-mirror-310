import subprocess


def has_modified_files() -> bool:
    """
    Git 상태를 확인하여 변경 사항의 존재 유무에 따라 True/False를 반환합니다
    """
    try:
        # 'git status --porcelain'으로 변경 사항이 있는지 확인
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
        # 출력 결과가 있으면 True (변경 사항 있음), 없으면 False (변경 사항 없음)
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        # Git 명령 실행 실패 시 예외 처리
        print(f"Git 명령 실행 중 오류 발생: {e}")
        return False
    except FileNotFoundError:
        # Git 명령이 없는 경우 예외 처리
        print("Git이 설치되어 있지 않거나 경로에 없습니다.")
        return False
