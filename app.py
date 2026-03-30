import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="익스트림 핀볼 추첨", layout="wide")

st.title("🐍 익스트림 뱀파이어 핀볼 추첨")
st.write("공들이 뱀 모양 미로와 회전 바를 지나 10초간의 대여정을 시작합니다!")

# 사이드바에서 이름 입력 (화면을 넓게 쓰기 위해)
with st.sidebar:
    st.header("👤 참가자 설정")
    names = [st.text_input(f"{i+1}번 참가자", f"Player {i+1}", key=f"n_{i}") for i in range(10)]

# 게임 구현 (Matter.js)
pinball_html = f"""
<div id="container" style="text-align:center;">
    <button id="start-btn" style="padding: 15px 30px; font-size: 20px; cursor: pointer; background: linear-gradient(45deg, #FF512F, #DD2476); color: white; border: none; border-radius: 50px; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">🔥 운명의 시작!</button>
    <div id="canvas-container"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
const names = {names};
const colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#F3FF33', '#33FFF3', '#FFA500', '#800080', '#008080', '#A52A2A'];

const {{ Engine, Render, Runner, Bodies, Composite, Events, Body }} = Matter;

function initGame() {{
    const container = document.getElementById('canvas-container');
    container.innerHTML = '';
    
    const engine = Engine.create();
    const world = engine.world;
    
    // 화면 높이를 길게 설정 (약 10초 낙하를 유도하기 위해 1600px)
    const render = Render.create({{
        element: container,
        engine: engine,
        options: {{ width: 500, height: 1600, wireframes: false, background: '#1a1a1a' }}
    }});

    // 1. 외곽 벽
    const wallOpts = {{ isStatic: true, render: {{ fillStyle: '#333' }} }};
    const ground = Bodies.rectangle(250, 1590, 500, 20, wallOpts);
    const leftWall = Bodies.rectangle(0, 800, 20, 1600, wallOpts);
    const rightWall = Bodies.rectangle(500, 800, 20, 1600, wallOpts);

    // 2. 뱀 모양 가상 벽 (Zig-Zag)
    const maze = [];
    for(let i=0; i<5; i++) {{
        let yPos = 250 + (i * 250);
        // 왼쪽에서 나오는 벽
        maze.push(Bodies.rectangle(150, yPos, 350, 10, {{ isStatic: true, angle: 0.2, render: {{ fillStyle: '#555'
