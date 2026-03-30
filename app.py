import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="익스트림 핀볼 추첨", layout="wide")

st.title("🐍 익스트림 뱀파이어 핀볼 추첨")
st.write("공들이 뱀 모양 미로와 회전 바를 지나 10초간의 대여정을 시작합니다!")

# 2. 사이드바 이름 입력
with st.sidebar:
    st.header("👤 참가자 설정")
    player_names = []
    for i in range(10):
        name = st.text_input(f"{i+1}번 참가자", f"Player {i+1}", key=f"player_{i}")
        player_names.append(name)

# 3. JavaScript 코드 (문자열 내부에 파이썬 변수 삽입을 피하기 위해 분리)
# 여기서 중요한 점은 JS 내부의 중괄호가 파이썬 f-string과 충돌하지 않게 f를 붙이지 않는 것입니다.
html_code = """
<div id="container" style="text-align:center;">
    <button id="start-btn" style="padding: 15px 30px; font-size: 20px; cursor: pointer; background: linear-gradient(45deg, #FF512F, #DD2476); color: white; border: none; border-radius: 50px; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">🔥 운명의 시작!</button>
    <div id="canvas-container"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
// 파이썬에서 전달할 데이터를 받을 변수
var names = []; 

const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;

function initGame() {
    const container = document.getElementById('canvas-container');
    container.innerHTML = '';
    
    const engine = Engine.create();
    const world = engine.world;
    
    const render = Render.create({
        element: container,
        engine: engine,
        options: { width: 500, height: 1600, wireframes: false, background: '#1a1a1a' }
    });

    const wallOpts = { isStatic: true, render: { fillStyle: '#333' } };
    const ground = Bodies.rectangle(250, 1590, 500, 20, wallOpts);
    const leftWall = Bodies.rectangle(0, 800, 20, 1600, wallOpts);
    const rightWall = Bodies.rectangle(500, 800, 20, 1600, wallOpts);

    const maze =
