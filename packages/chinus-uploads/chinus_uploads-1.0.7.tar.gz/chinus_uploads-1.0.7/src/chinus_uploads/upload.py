import sys
from typing import Literal
from chinus_tools import get_modified_items
from chinus_uploads.__uploads import upload_to_github, upload_package, update_package_version, clean_dist, build_package



def upload(
        git=True,
        pypi=True,
        version: Literal['major', 'minor', 'patch'] = 'patch',
        git_commit: str = 'Build and upload package'
):

    """
    github와 pypi에 자동으로 패키지를 업로드 합니다
    :param git:
    :param pypi:
    :param version:
    :param git_commit:
    :return None:
    """
    # 변경 사항이 존재 and pypi 업로드 Ture인 경우
    if get_modified_items() and pypi:
        update_package_version(version)  # project.toml version 업데이트
        clean_dist()  # dist 디렉토리 삭제

    else:
        print("변경 사항이 존재하지 않습니다.")
        sys.exit(0)

    if build_package():  # 빌드 성공 시 업로드 실행
        upload_package()

    else:
        print("빌드 실패! 업로드를 실행하지 않습니다.")
        sys.exit(0)

    if git:  # 깃허브 업로드
        upload_to_github(git_commit)


if __name__ == "__main__":
    upload()
