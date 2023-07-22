# GithubContributionVisualizer
Github 잔디깍기를 위한 Tool

[![프로필](http://githubdaily.kro.kr/contribution/sh0116/2000x650)](http://githubdaily.kro.kr/contribution/sh0116/2000x650)

# GitHub Contributions API

GitHub Contributions API는 Flask로 작성된 간단한 백엔드 API입니다. 이 API는 주어진 GitHub 사용자의 Contribution 기록을 크롤링하여 가시화하고, 이를 이미지로 반환합니다.

# Notion에서 사용하는 방법
관련 이슈를 링크로 걸어놨습니다.
[ISSUE](https://github.com/sh0116/GithubContributionVisualizer/issues/1#issue-1815367277)

# Github에서 사용하는 방법
마크다운 형식으로 아래 형식으로 삽입하면됩니다.
```
[![프로필](http://githubdaily.kro.kr/contribution/sh0116/2000x650)](http://githubdaily.kro.kr/contribution/sh0116/2000x650)
```
# GitHub Contributions API 사용하기

다음 DNS 주소를 통해 본인의 GitHub Contribution을 확인하실 수 있습니다:

```
http://githubdaily.kro.kr/contribution/<your-github-username>/2000x650
```

이 주소를 웹 브라우저의 주소창에 입력하면 됩니다. `<your-github-username>` 부분을 본인의 GitHub 사용자 이름으로 바꿔주시면 됩니다.

예를 들어, GitHub 사용자 이름이 "john"인 경우 다음과 같이 입력합니다:

```
http://githubdaily.kro.kr/contribution/sh0116/2000x650
해당 주소로 접속하면, GitHub 사용자 "sh0116"의 contribution 기록이 가시화된 이미지를 볼 수 있습니다. 이미지의 가로는 2000px, 세로는 650px 입니다.
```



## 엔드포인트

HTTP GET 요청을 사용하여 사용자의 contribution 기록을 크롤링하고 이미지로 반환하는 엔드포인트는 다음과 같습니다:

```bash
/contribution/<user>/int:widthxint:height
```


여기서 `<user>`는 GitHub 사용자 이름이며, `<int:width>`와 `<int:height>`는 이미지의 가로와 세로 크기입니다.

예를 들어, GitHub 사용자 이름이 "john"이고 가로 800, 세로 600의 이미지를 원한다면 다음과 같이 요청할 수 있습니다:

```bash
/contribution/john/800x600
```


## 실행 방법

아래와 같이 실행할 수 있습니다:

1. 소스 코드를 로컬 머신에 복사합니다.
2. 필요한 Python 라이브러리를 설치합니다: `requests`, `bs4`, `pandas`, `seaborn`, `matplotlib`, `PIL`, `flask`.
3. Flask 애플리케이션을 실행합니다. 아래의 명령어를 터미널에 입력하면 됩니다:

```bash
python app.py
```

## 배포
이 애플리케이션은 AWS EC2 인스턴스에서 동작하도록 설정되어 있습니다. Flask 애플리케이션은 0.0.0.0 호스트와 5000 포트에서 실행되도록 설정되어 있습니다.


이 코드를 README.md 파일에 추가하거나 GitHub 저장소의 설명에 추가하실 수 있습니다. 위의 마크다운 텍스트는 GitHub에서 정상적으로 렌더링됩니다.
