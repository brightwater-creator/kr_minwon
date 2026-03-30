import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 기본 설정
st.set_page_config(page_title="핀볼 게임", layout="wide")

st.title("🐍 핀볼 당첨자 뽑기 (익스트림 모드)")
st.write("약 15초의 레이스! 뱀 모양 미로와 회전 바를 통과해야 합니다.")

# 2. 참가자 이름 리스트 생성 (사이드바)
with st.sidebar:
    st.header("참가자 설정")
    player_names = []
    for i in range(10):
        name = st.text_input(f"{i+1}번 참가자", f"참가자 {i+1}", key=f"player_{i}")
        player_names.append(name)

# 3. HTML 및 JavaScript 조각들 (따옴표 에러 방지를 위해 결합 방식 사용)
h1 = '<div id="box" style="text-align:center;">'
h2 = '<button id="go" style="padding:15px 30px;font-size:20px;border-radius:50px;background:red;color:white;cursor:pointer;border:none;">🚀 시작하기</button>'
h3 = '<div id="game"></div></div>'
h4 = '<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>'

# JS 로직 (파이썬의 f-string 충돌을 피하기 위해 분리)
js_logic = """
<script>
const playerNames = NAMES_JSON;
const colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#F3FF33", "#33FFF3", "#FFA500", "#800080", "#008080", "#A52A2A"];
const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;

function play() {
    const container = document.getElementById("game");
    container.innerHTML = "";
    const engine = Engine.create();
    const render = Render.create({
        element: container,
        engine: engine,
        options: { width: 500, height: 2200, wireframes: false, background: "#111" }
    });
    
    // 벽 생성
    const walls = [
        Bodies.rectangle(250, 2190, 500, 20, { isStatic: true }),
        Bodies.rectangle(0, 1100, 20, 2200, { isStatic: true }),
        Bodies.rectangle(500, 1100, 20, 2200, { isStatic: true })
    ];

    // 뱀 모양 미로
    const maze = [];
    for(let i=0; i<10; i++) {
        maze.push(Bodies.rectangle(130, 300+i*180, 300, 12, { isStatic: true, angle: 0.2, render: {fillStyle: "#444"} }));
        maze.push(Bodies.rectangle(370, 390+i*180, 300, 12, { isStatic: true, angle: -0.2, render: {fillStyle: "#444"} }));
    }

    // 회전 바
    const spinners = [];
    for(let i=0; i<6; i++) {
        spinners.push(Bodies.rectangle(250, 250+i*300, 140, 10, { isStatic: true, label: "spin
