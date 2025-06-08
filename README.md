# AI 자기소개서 생성기

채용공고를 분석하여 맞춤형 자기소개서를 생성하는 웹 애플리케이션입니다.

## 주요 기능

- 채용공고 분석 및 자동 매칭
- 직무별 맞춤형 자기소개서 생성
- 회사 유형(대기업/중소기업)에 따른 차별화된 내용
- 기술 스택 및 소프트 스킬 자동 분석
- 산업별 특화 표현 자동 생성

## 로컬 실행 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 애플리케이션 실행:
```bash
python app.py
```

3. 웹 브라우저에서 접속:
```
http://localhost:5000
```

## 배포 방법 (PythonAnywhere)

1. PythonAnywhere 계정 생성 (https://www.pythonanywhere.com)

2. Files 탭에서 프로젝트 파일 업로드:
   - app.py
   - requirements.txt
   - templates/index.html
   - static/style.css

3. Web 탭에서 새 웹 앱 생성:
   - Flask 프레임워크 선택
   - Python 3.8 이상 버전 선택
   - 프로젝트 경로 지정

4. 가상환경 설정:
```bash
pip install -r requirements.txt
```

5. WSGI 설정 파일 수정:
```python
import sys
path = '/home/yourusername/yourproject'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

6. 웹 앱 재시작

## 사용 방법

1. 채용공고 입력
2. 개인정보 입력 (이름, 전공)
3. 회사 유형 선택
4. 자기소개 입력 (선택사항)
5. 주요 경험 입력
6. 생성 버튼 클릭

## 주의사항

- 채용공고는 자격요건과 우대사항을 포함해야 합니다.
- 주요 경험은 구체적인 성과와 함께 작성하면 더 좋은 결과를 얻을 수 있습니다.
- 생성된 자기소개서는 참고용으로만 사용하고, 필요에 따라 수정하여 사용하세요.

## 기술 스택

- Python
- Flask
- HTML/CSS
- JavaScript 