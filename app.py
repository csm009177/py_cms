
#! 모듈 불러오기
from flask import Flask, request, redirect, render_template_string
import sqlite3, os
""" 이 모듈은 Flask 웹 애플리케이션을 위한 초기 설정을 포함합니다.

- Flask: 웹 서버 및 라우팅을 위한 Flask 프레임워크의 핵심 클래스입니다. 
    # Flask 객체를 생성하여 웹 애플리케이션의 진입점을 만듭니다.

- request: 클라이언트의 HTTP 요청 데이터를 다루는 객체입니다.
    # 폼 데이터, 쿼리 스트링, 파일 업로드 등 요청 관련 정보를 처리할 때 사용합니다.

- redirect: 다른 URL로 사용자를 리디렉션(이동)시키는 함수입니다.
    # 예를 들어, 폼 제출 후 목록 페이지로 이동할 때 사용합니다.

- render_template_string: 문자열로 정의된 HTML 템플릿을 렌더링하는 함수입니다.
    # 외부 템플릿 파일 없이 Python 코드 내에서 직접 HTML을 생성할 때 사용합니다.

- sqlite3: 파이썬 내장 SQLite 데이터베이스 모듈입니다.
    # 데이터베이스 연결 및 쿼리 실행을 통해 데이터 저장 및 조회를 처리합니다.

- os: 운영체제와 상호작용하는 파이썬 내장 모듈입니다.
    # 파일 시스템 작업, 환경 변수 접근 등에 사용합니다.
    # 이 코드에서는 데이터베이스 파일 존재 여부를 확인하는 용도로 사용됩니다.
"""


#! 데이터 베이스 연결
# Flask 애플리케이션 정보덩어리(인스턴스)를 만들어서 app이라는 공간에 넣습니다
# __name__라는 파이썬 내장 변수를 사용해서 현재 파일의 이름을 반환합니다
app = Flask(__name__)

# 데이터베이스 파일명 상수 정의
# 생성될 SQLite 데이터베이스 파일의 경로
DB = 'sqlite_db/cms.db'

# 데이터베이스 초기화 및 테이블 생성
# 애플리케이션 최초 실행 시 DB가 없으면 자동으로 생성
if not os.path.exists(DB):
    # SQLite 데이터베이스 연결 생성
    conn = sqlite3.connect(DB)
    
    # post 테이블 생성
    # id: 자동 증가하는 기본키 (PRIMARY KEY AUTOINCREMENT)
    # title: 글 제목을 저장하는 텍스트 필드
    # content: 글 내용을 저장하는 텍스트 필드
    conn.execute('CREATE TABLE post (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)')
    
    # 데이터베이스 연결 종료
    conn.close()



#! 메인 페이지 라우트 - 글 목록 표시
@app.route('/')
def index():
    """
    홈페이지(/) 접속 시 실행되는 함수
    데이터베이스에서 모든 글의 목록을 조회하여 표시
    """
    # 데이터베이스 연결
    conn = sqlite3.connect(DB)
    
    # 모든 글의 id와 title을 최신순(id 내림차순)으로 조회
    # fetchall()로 모든 결과를 리스트로 가져옴
    posts = conn.execute('SELECT id, title FROM post ORDER BY id DESC').fetchall()
    
    # 데이터베이스 연결 종료
    conn.close()
    
    # HTML 템플릿을 문자열로 정의하고 렌더링
    # Jinja2 템플릿 엔진을 사용하여 posts 데이터를 동적으로 삽입
    return render_template_string('''
        <h1>📄 글 목록</h1>
        <a href="/write">✍ 글쓰기</a><ul>
        {% for id, title in posts %}
            <li><a href="/view/{{ id }}">{{ title }}</a></li>
        {% endfor %}</ul>
    ''', posts=posts)


#! 글 작성 페이지 및 처리 라우트
@app.route('/write', methods=['GET', 'POST'])
def write():
    """
    글 작성 페이지 표시 및 글 작성 처리
    GET 요청: 글 작성 폼 표시
    POST 요청: 새 글을 데이터베이스에 저장
    """
    if request.method == 'POST':
        # POST 요청 처리 - 새 글 저장
        
        # 데이터베이스 연결
        conn = sqlite3.connect(DB)
        
        # 폼에서 전송된 제목과 내용을 데이터베이스에 삽입
        # ?를 사용한 매개변수 바인딩으로 SQL 인젝션 방지
        conn.execute('INSERT INTO post (title, content) VALUES (?, ?)',
                     (request.form['title'], request.form['content']))
        
        # 변경사항을 데이터베이스에 반영
        conn.commit()
        
        # 데이터베이스 연결 종료
        conn.close()
        
        # 글 저장 후 메인 페이지로 리디렉션
        return redirect('/')
    
    # GET 요청 처리 - 글 작성 폼 표시
    return render_template_string('''
        <h1>✍ 글쓰기</h1>
        <form method="post">
            제목: <input name="title"><br>
            내용:<br><textarea name="content"></textarea><br>
            <button type="submit">저장</button>
        </form>
    ''')


#! 글 상세보기 페이지 라우트
@app.route('/view/<int:id>')
def view(id):
    """
    특정 글의 상세 내용을 표시
    URL 경로에서 글의 id를 정수로 받아 해당 글을 조회
    """
    # 데이터베이스 연결
    conn = sqlite3.connect(DB)
    
    # 특정 id의 글 제목과 내용을 조회
    # fetchone()으로 단일 결과만 가져옴
    post = conn.execute('SELECT title, content FROM post WHERE id = ?', (id,)).fetchone()
    
    # 데이터베이스 연결 종료
    conn.close()
    
    if post:
        # 글이 존재하는 경우 상세 내용 표시
        # 수정, 삭제 링크도 함께 제공
        return render_template_string('''
            <h1>{{ post[0] }}</h1>
            <p>{{ post[1] }}</p>
            <a href="/edit/{{ id }}">✏ 수정</a>
            <a href="/delete/{{ id }}" onclick="return confirm('정말 삭제하시겠습니까?')">🗑 삭제</a>
            <br><a href="/">← 목록으로</a>
        ''', post=post, id=id)
    
    # 글이 존재하지 않는 경우 에러 메시지 표시
    return '글을 찾을 수 없습니다.'


#! 글 수정 페이지 및 처리 라우트
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """
    글 수정 페이지 표시 및 글 수정 처리
    GET 요청: 기존 글 내용이 채워진 수정 폼 표시
    POST 요청: 수정된 내용을 데이터베이스에 업데이트
    """
    # 데이터베이스 연결
    conn = sqlite3.connect(DB)
    
    if request.method == 'POST':
        # POST 요청 처리 - 글 수정 저장
        
        # 특정 id의 글 제목과 내용을 업데이트
        conn.execute('UPDATE post SET title = ?, content = ? WHERE id = ?',
                     (request.form['title'], request.form['content'], id))
        
        # 변경사항을 데이터베이스에 반영
        conn.commit()
        
        # 데이터베이스 연결 종료
        conn.close()
        
        # 수정 완료 후 해당 글의 상세보기 페이지로 리디렉션
        return redirect(f'/view/{id}')
    
    # GET 요청 처리 - 수정 폼 표시
    # 기존 글 내용을 조회하여 폼에 미리 채워넣기
    post = conn.execute('SELECT title, content FROM post WHERE id = ?', (id,)).fetchone()
    
    # 데이터베이스 연결 종료
    conn.close()
    
    if post:
        # 글이 존재하는 경우 기존 내용이 채워진 수정 폼 표시
        return render_template_string('''
            <h1>✏ 글 수정</h1>
            <form method="post">
                제목: <input name="title" value="{{ post[0] }}"><br>
                내용:<br><textarea name="content">{{ post[1] }}</textarea><br>
                <button type="submit">수정 완료</button>
            </form>
        ''', post=post)
    
    # 글이 존재하지 않는 경우 에러 메시지 표시
    return '글을 찾을 수 없습니다.'

# 글 삭제 처리 라우트
@app.route('/delete/<int:id>')
def delete(id):
    """
    특정 글을 데이터베이스에서 삭제
    삭제 후 메인 페이지로 리디렉션
    """
    # 데이터베이스 연결
    conn = sqlite3.connect(DB)
    
    # 특정 id의 글을 삭제
    conn.execute('DELETE FROM post WHERE id = ?', (id,))
    
    # 변경사항을 데이터베이스에 반영
    conn.commit()
    
    # 데이터베이스 연결 종료
    conn.close()
    
    # 삭제 완료 후 메인 페이지로 리디렉션
    return redirect('/')

# 애플리케이션 실행부
if __name__ == '__main__':
    """
    이 스크립트가 직접 실행될 때만 Flask 개발 서버를 시작
    다른 모듈에서 import할 때는 실행되지 않음
    debug=True로 설정하여 개발 모드에서 실행
    - 코드 변경 시 자동 재시작
    - 에러 발생 시 상세한 디버그 정보 표시
    """
    app.run(debug=True)