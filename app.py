import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="익스트림 핀볼 추첨", layout="wide")

st.title("🐍 익스트림 뱀파이어 핀볼 추첨")
st.write("공들이 뱀 모양 미로와 회전 바를 지나 10초간의 대여정을 시작합니다!")

# 사이드바에서 이름 입력
with st.sidebar:
    st.header("👤 참가자 설정")
    names = [st.text_input(f"{i+1}번 참가자", f"Player {i+1}", key=f"n_{i}") for i in range(10)]

# JavaScript 코드 (f-string 에러를 방지하기 위해 일반 문자열로 작성)
html_template = """
<div id="container" style="text-align:center;">
    <button id="start-btn" style="padding: 15px 30px; font-size: 20px; cursor: pointer; background: linear-gradient(45deg, #FF512F, #DD2476); color: white; border: none; border-radius: 50px; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">🔥 운명의 시작!</button>
    <div id="canvas-container"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
// 파이썬에서 넘겨준 이름 리스트를 안전하게 가져옴
const names = JSON_NAMES_PLACEHOLDER;
const colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#F3FF33', '#33FFF3', '#FFA500', '#800080', '#008080', '#A52A2A'];

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

    const maze = [];
    for(let i=0; i<5; i++) {
        let yPos = 250 + (i * 250);
        maze.push(Bodies.rectangle(150, yPos, 350, 10, { isStatic: true, angle: 0.2, render: { fillStyle: '#555' } }));
        maze.push(Bodies.rectangle(350, yPos + 120, 350, 10, { isStatic: true, angle: -0.2, render: { fillStyle: '#555' } }));
    }

    const spinners = [];
    for(let i=0; i<6; i++) {
        let s = Bodies.rectangle(250, 200 + (i * 230), 120, 10, { 
            isStatic: true, 
            render: { fillStyle:
