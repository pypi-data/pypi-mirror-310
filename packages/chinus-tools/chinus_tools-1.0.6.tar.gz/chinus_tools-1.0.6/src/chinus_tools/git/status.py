import subprocess


def get_modified_items() -> list:
    """
    Git 상태를 확인하여 수정된 최상위 폴더 또는 파일의 목록을 공백으로 구분된 문자열로 반환합니다.

    Returns:
        list: 수정된 최상위 폴더 또는 파일들 리스트
    """
    # 'git status --porcelain'으로 변경 사항이 있는지 확인
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

    # 결과 파싱
    modified_items = set()
    for line in result.stdout.strip().splitlines():
        # 변경된 파일 경로는 세 번째 컬럼부터 나옴
        file_path = line[3:].strip()
        # 최상위 폴더 또는 파일 추출
        top_level_item = file_path.split('/')[0]
        modified_items.add(top_level_item)

    # 공백으로 구분된 문자열로 변환
    return list(modified_items)