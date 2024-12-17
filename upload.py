import base64
import requests
import json

def upload_file_to_github(file_path, repo_owner, repo_name, token, target_path):
    """
    GitHub에 파일을 업로드하는 함수.
    :param file_path: 업로드할 파일의 로컬 경로
    :param repo_owner: GitHub 리포지토리 소유자
    :param repo_name: GitHub 리포지토리 이름
    :param token: GitHub Personal Access Token
    :param target_path: 리포지토리 내 업로드할 파일의 경로
    :return: 성공 여부
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{target_path}"

    # 파일을 읽어서 base64로 인코딩
    with open(file_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    # 업로드할 파일에 대한 정보 준비
    data = {
        "message": "Add file",  # 커밋 메시지
        "content": content,     # base64로 인코딩된 파일 콘텐츠
    }

    # 헤더에 인증 토큰 추가
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 요청 보내기
    response = requests.put(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print(f"File '{file_path}' uploaded successfully to GitHub.")
    else:
        print(f"Error uploading file: {response.status_code}")
        print(response.json())
