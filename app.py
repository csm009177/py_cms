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
"""

app = Flask(__name__)
DB = 'cms.db'

# DB가 없으면 테이블 생성
if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE post (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)')
    conn.close()

# 글 목록
@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    posts = conn.execute('SELECT id, title FROM post ORDER BY id DESC').fetchall()
    conn.close()
    return render_template_string('''
        <h1>📄 글 목록</h1>
        <a href="/write">✍ 글쓰기</a><ul>
        {% for id, title in posts %}
            <li><a href="/view/{{ id }}">{{ title }}</a></li>
        {% endfor %}</ul>
    ''', posts=posts)

# 글 작성
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        conn = sqlite3.connect(DB)
        conn.execute('INSERT INTO post (title, content) VALUES (?, ?)',
                     (request.form['title'], request.form['content']))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template_string('''
        <h1>✍ 글쓰기</h1>
        <form method="post">
            제목: <input name="title"><br>
            내용:<br><textarea name="content"></textarea><br>
            <button type="submit">저장</button>
        </form>
    ''')

# 글 보기
@app.route('/view/<int:id>')
def view(id):
    conn = sqlite3.connect(DB)
    post = conn.execute('SELECT title, content FROM post WHERE id = ?', (id,)).fetchone()
    conn.close()
    if post:
        return render_template_string('''
            <h1>{{ post[0] }}</h1>
            <p>{{ post[1] }}</p>
            <a href="/edit/{{ id }}">✏ 수정</a>
            <a href="/delete/{{ id }}" onclick="return confirm('정말 삭제하시겠습니까?')">🗑 삭제</a>
            <br><a href="/">← 목록으로</a>
        ''', post=post, id=id)
    return '글을 찾을 수 없습니다.'

# 글 수정
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DB)
    if request.method == 'POST':
        conn.execute('UPDATE post SET title = ?, content = ? WHERE id = ?',
                     (request.form['title'], request.form['content'], id))
        conn.commit()
        conn.close()
        return redirect(f'/view/{id}')
    post = conn.execute('SELECT title, content FROM post WHERE id = ?', (id,)).fetchone()
    conn.close()
    if post:
        return render_template_string('''
            <h1>✏ 글 수정</h1>
            <form method="post">
                제목: <input name="title" value="{{ post[0] }}"><br>
                내용:<br><textarea name="content">{{ post[1] }}</textarea><br>
                <button type="submit">수정 완료</button>
            </form>
        ''', post=post)
    return '글을 찾을 수 없습니다.'

# 글 삭제
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB)
    conn.execute('DELETE FROM post WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)