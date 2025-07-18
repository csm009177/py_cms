import socketserver          # 간단한 서버(문서를 나눠주는 기계)를 만들기 위한 라이브러리(기능덩어리)
import os                    # 파일이나 폴더 경로를 다룰 때 사용하는 도구
import json                  # JSON 형식의 파일을 읽고 쓸 수 있도록 도와주는 도구

# user_info.json 파일을 열어(open)서 그 안에 있는 데이터를 읽어옵니다.
# 읽은 데이터를 as를 사용하여 user_info_from_json 에 저장합니다
# 첫번째 인자 : 파일경로
# 두번째 인자 : 
#   'r'	    읽기 전용
#   'w'	    쓰기 전용
#   'a'	    추가 모드
#   'r+'	읽기 + 쓰기
#   'w+'	쓰기 + 읽기
with open('user_info.json', 'r', encoding='utf-8') as user_info_from_json:
    # JSON 파일의 내용을 파이썬 딕셔너리(뭐 : 뭐 라는 데이터 형태라고 생각합시다)로 바꿔서 저장합니다.
    user_info = json.load(user_info_from_json)

    
# 마이페이지 HTML 파일을 만들어주는 함수
def mypageMaker(file_name, page_title):
    page_title = "mypage"  # 페이지 제목을 "mypage"로 고정합니다.
    my_message = f"{user_info['name']}님의 마이페이지입니다!"  # 사용자 이름을 포함한 인사말을 만듭니다.
    file_name = page_title + ".html"  # 실제 저장할 파일 이름을 만듭니다. (예: mypage.html)

    # HTML 파일을 쓰기 모드(w)로 엽니다.
    file = open(file_name, "w", encoding='utf-8')

    # HTML 문서를 문자열로 작성해서 파일에 저장합니다.
    file.write(f"""<!DOCTYPE html> 
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{page_title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #f4f4f9;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 500px;
            margin: 50px auto;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 30px 40px;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f0f0f0;
            color: #555;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{page_title}</h1>
        <p style="text-align:center; color:#666;">{my_message}</p>
        <table>
            <tr><th>이름</th><td>{user_info['name']}</td></tr>
            <tr><th>나이</th><td>{user_info['age']}</td></tr>
            <tr><th>성별</th><td>{user_info['sex']}</td></tr>
            <tr><th>주소</th><td>{user_info['address']}</td></tr>
            <tr><th>전화번호</th><td>{user_info['phone']}</td></tr>
        </table>
    </div>
</body>
</html>
""")
    file.close()  # 파일을 저장하고 닫습니다.
    print("웹페이지가 만들어졌습니다!")  # 완료 메시지를 출력합니다.

# 인덱스 페이지(index.html)를 만들어주는 함수
def indexMaker(filename, title):
    # HTML 요소들을 변수로 만들어 조합합니다.
    doctype = "<!DOCTYPE html>"
    html_open = "<html>"
    head_open = "<head>"
    title_tag = f"<title>{title}</title>"
    head_close = "</head>"
    body_open = "<body>"
    h1_tag = f'<h1>welcome <a href="mypage.html">{user_info["name"]}</a></h1>'  # 마이페이지로 연결되는 링크 포함
    body_close = "</body>"
    html_close = "</html>"

    # 위에서 만든 HTML 요소들을 하나로 합칩니다.
    html_content = (
        doctype + "\n" + html_open + "\n" +
        head_open + "\n" +
        title_tag + "\n" +
        head_close + "\n" +
        body_open + "\n" +
        h1_tag + "\n" +
        body_close + "\n" +
        html_close + "\n"
    )

    # 완성된 HTML 문서를 파일로 저장합니다.
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print("생성완료")  # 완료 메시지 출력

# 위에서 만든 두 함수를 실행해서 HTML 파일을 생성합니다.
mypageMaker('mypage', '마이페이지')
indexMaker('index.html', 'welcome')

# 여기서부터는 간단한 웹서버를 만들어서 위에서 만든 HTML 파일들을 브라우저에서 볼 수 있도록 합니다.
import http.server

PORT = 8080  # 웹서버가 열릴 포트 번호입니다. 브라우저에서 http://localhost:8080 으로 접속합니다.
DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # 현재 파이썬 파일이 있는 폴더 경로를 가져옵니다.

# 웹 요청이 들어오면 파일을 보여주는 역할을 하는 핸들러(도우미)를 설정합니다.
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# 웹서버를 실행시킵니다.
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")  # 터미널에 서버 주소 출력
    httpd.serve_forever()  # 서버를 계속 실행시킵니다.
