import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="익스트림 핀볼 추첨", layout="wide")

st.title("🐍 익스트림 뱀파이어 핀볼 추첨")
st.write("뱀 모양 미로와 회전하는 바를 통과하세요! 약 10~15초의 대여정이 시작됩니다.")

# 2. 참가자 이름 입력 (사이드바)
with st.sidebar:
    st.header("👤 참가자 설정")
    player_names = []
    for i in range(10):
        p_name = st.text_input(f"{i+1}번 참가자", f"참가자 {i+1}", key=f"p_{i}")
        player_names.append(p_name)

# 3. 안전한 HTML/JS 조립 방식 (리스트 조인)
# 따옴표 세 개 대신 리스트를 사용하여 구문 오류를 방지합니다.
html_parts = [
    '<div id="container" style="text-align:center;">',
    '    <button id="start-btn" style="padding: 15px 30px; font-size: 20px; cursor: pointer; background: linear-gradient(45deg, #FF512F, #DD2476); color: white; border: none; border-radius: 50px; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">🚀 운명의 시작!</button>',
    '    <div id="canvas-container"></div>',
    '</div>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>',
    '<script>',
    'const names = ' + json.dumps(player_names) + ';',
    'const colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#F3FF33", "#33FFF3", "#FFA500", "#800080", "#008080", "#A52A2A"];',
    'const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;',
    '',
    'function initGame() {',
    '    const container = document.getElementById("canvas-container");',
    '    container.innerHTML = "";',
    '    const engine = Engine.create();',
    '    const world = engine.world;',
    '    // 10초 낙하를 위해 높이를 2200px로 대폭 확장',
    '    const render = Render.create({',
    '        element: container,',
    '        engine: engine,',
    '        options: { width: 500, height: 2200, wireframes: false, background: "#0f0f0f" }',
    '    });',
    '',
    '    // 벽 설정',
    '    const wallOpts = { isStatic: true, render: { fillStyle: "#333" } };',
    '    const ground = Bodies.rectangle(250, 2190, 500, 20, wallOpts);',
    '    const leftWall = Bodies.rectangle(0, 1100, 20, 2200, wallOpts);',
    '    const rightWall = Bodies.rectangle(500, 1100, 20, 2200, wallOpts);',
    '',
    '    // 뱀 모양 미로 (Zig-Zag Maze)',
    '    const maze = [];',
    '    for(let i=0; i<8; i++) {',
    '        let yPos = 300 + (i * 220);',
    '        maze.push(Bodies.rectangle(140, yPos, 320, 15, { isStatic: true, angle: 0.25, render: { fillStyle: "#444" } }));',
    '        maze.push(Bodies.rectangle(360, yPos + 110, 320, 15, { isStatic: true, angle: -0.25, render: { fillStyle: "#444" } }));',
    '    }',
    '',
    '    // 회전하는 바 (Spinners) - 공을 위로 쳐올리도록 회전 방향 조절',
    '    const spinners = [];',
    '    for(let i=0; i<7; i++) {',
    '        let s = Bodies.rectangle(250, 200 + (i * 280), 140, 12, {',
    '            isStatic: true, render: { fillStyle: "#FFD700" }, label: "spinner"',
    '        });',
    '        spinners.push(s);',
    '    }',
    '',
    '    // 하단 깔때기 및 골인 센서',
    '    const lF = Bodies.rectangle(150, 2100, 350, 10, { isStatic: true, angle: Math.PI/4 });',
    '    const rF = Bodies.rectangle(350, 2100, 350, 10, { isStatic: true, angle: -Math.PI/4 });',
    '    const sensor = Bodies.rectangle(250, 2180, 40, 20, { isStatic: true, isSensor: true, render: { fillStyle: "transparent" } });',
    '',
    '    Composite.add(world, [ground, leftWall, rightWall, lF, rF, sensor, ...maze, ...spinners]);',
    '',
    '    // 공 생성 (속도 조절을 위해 frictionAir 추가)',
    '    const balls = names.map((name, i) => {',
    '        return Bodies.circle(250 + (Math.random()*30 - 15), -i * 60, 11, {',
    '            restitution: 0.6, friction: 0.1, frictionAir: 0.015,',
    '            render: { fillStyle: colors[i % colors.length], strokeStyle: "#fff", lineWidth: 2 },',
    '            label: name',
    '        });',
    '    });',
    '    Composite.add(world, balls);',
    '',
    '    let winnerDeclared = false;',
    '    Events.on(engine, "beforeUpdate", () => {',
    '        spinners.forEach((s, idx) => { ',
    '            // 홀수/짝수 바의 회전 방향을 다르게 하여 공을 흔듦',
    '            Body.rotate(s, idx % 2 === 0 ? 0.12 : -0.12); ',
    '        });',
    '    });',
    '',
    '    // 충돌 이벤트 (폭탄 효과 및 승자
