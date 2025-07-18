from flask import Flask, render_template, request, redirect, url_for
import sqlite3
"""
이 모듈은 Flask 웹 애플리케이션을 위한 초기 설정을 포함합니다.

- Flask: 웹 서버 및 라우팅을 위한 Flask 프레임워크의 핵심 클래스입니다. 
    # Flask 객체를 생성하여 웹 애플리케이션의 진입점을 만듭니다.

- render_template: HTML 템플릿 렌더링을 위한 함수입니다.
    # 사용자가 요청한 페이지에 동적으로 데이터를 전달하여 HTML 파일을 반환할 때 사용합니다.

- request: 클라이언트의 HTTP 요청 데이터를 다루는 객체입니다.
    # 폼 데이터, 쿼리 스트링, 파일 업로드 등 요청 관련 정보를 처리할 때 사용합니다.

- redirect: 다른 URL로 사용자를 리디렉션(이동)시키는 함수입니다.
    # 예를 들어, 폼 제출 후 목록 페이지로 이동할 때 사용합니다.

- url_for: 라우트 함수의 이름을 기반으로 URL을 생성하는 함수입니다.
    # 하드코딩 없이 동적으로 URL을 생성할 수 있어 유지보수에 용이합니다.

- sqlite3: 파이썬 내장 SQLite 데이터베이스 모듈입니다.
    # 데이터베이스 연결 및 쿼리 실행을 통해 데이터 저장 및 조회를 처리합니다.
"""

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('db/cms.db')
    conn.row_factory = sqlite3.Row
    return conn