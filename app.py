import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="핀볼 당첨자 뽑기", layout="wide")

st.title("🐍 익스트림 뱀파이어 핀볼")
st.write("약 15초간의 대여정! 끝까지 살아남아 깔대기를 통과하는 공이 승리합니다.")

# 2. 참가자 이름 입력 (사이드바)
with st.sidebar:
    st.header("👤 참가자 설정")
    player_names = []
    for i in range(10):
        p_name = st.text_input(f"{i+1}번 참가자", f"참가자 {i+1}", key=f"p_{i}")
        player_names.append(p_name)

# 3. HTML/JS 템플릿
html_template = """
<div id="container" style="text-align:center;">
    <button id="start-btn" style="padding: 15px 30px; font-size: 20px; cursor: pointer; background: linear-gradient(45deg, #FF512F, #DD2476); color: white; border: none; border-radius: 50px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">🚀 게임 시작!</button>
    <div id="canvas-container"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
const names = NAMES_DATA_PLACEHOLDER;
const colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#F3FF33", "#33FFF3", "#FFA500", "#800080", "#008080", "#A52A2A"];

const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;

function initGame() {
    const container = document.getElementById("canvas-container");
    container.innerHTML = "";
    
    const engine = Engine.create();
    const world = engine.world;
    
    const render = Render.create({
        element: container,
        engine: engine,
        options: { width: 500, height: 2400, wireframes: false, background: "#0f0f0f" }
    });

    const wallOpts = { isStatic: true, render: { fillStyle: "#333" } };
    const ground = Bodies.rectangle(250, 2390, 500, 20, wallOpts);
    const leftWall = Bodies.rectangle(0, 1200, 20, 2400, wallOpts);
    const rightWall = Bodies.rectangle(500, 1200, 20, 2400, wallOpts);

    const maze = [];
    for(let i=0; i<10; i++) {
        let yPos = 350 + (i * 200);
        maze.push(Bodies.rectangle(130, yPos, 300, 15, { isStatic: true, angle: 0.2, render: { fillStyle: "#444" } }));
        maze.push(Bodies.rectangle(370, yPos + 100, 300, 15, { isStatic: true, angle: -0.2, render: { fillStyle: "#444" } }));
    }

    const spinners = [];
    for(let i=0; i<8; i++) {
        let s = Bodies.rectangle(250, 250 + (i * 260), 150, 12, {
            isStatic: true, render: { fillStyle: "#FFD700" }, label: "spinner"
        });
        spinners.push(s);
    }

    const lF = Bodies.rectangle(150, 2300, 350, 15, { isStatic: true, angle: 0.8 });
    const rF = Bodies.rectangle(350, 2300, 350, 15, { isStatic: true, angle: -0.8 });
    const sensor = Bodies.rectangle(250, 2380, 50, 20, { isStatic: true, isSensor: true, render: { fillStyle: "transparent" } });

    Composite.add(world, [ground, leftWall, rightWall, lF, rF, sensor, ...maze, ...spinners]);

    const balls = names.map((name, i) => {
        return Bodies.circle(250 + (Math.random()*40 - 20), -i * 60, 12, {
            restitution: 0.6, friction: 0.1, frictionAir: 0.012,
            render: { fillStyle: colors
