import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="핀볼 게임", layout="wide")

st.title("🐍 핀볼 당첨자 뽑기 (익스트림)")
st.write("15초의 승부! 뱀 모양 미로와 회전 바를 통과하세요.")

# 2. 참가자 설정
with st.sidebar:
    st.header("참가자 설정")
    p_names = []
    for i in range(10):
        val = st.text_input(f"{i+1}번", f"참가자 {i+1}", key=f"user_{i}")
        p_names.append(val)

# 3. JS 코드를 한 줄씩 리스트로 관리 (따옴표 에러 방지)
js_lines = [
    '<div id="main" style="text-align:center;">',
    '<button id="btn" style="padding:15px 30px;font-size:20px;border-radius:50px;background:#ff4b4b;color:white;border:none;cursor:pointer;">🚀 레이스 시작!</button>',
    '<div id="area" style="margin-top:20px;"></div>',
    '</div>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>',
    '<script>',
    'const users = ' + json.dumps(p_names) + ';',
    'const colors = ["#ff5733","#33ff57","#3357ff","#f333ff","#f3ff33","#33fff3","#ffa500","#800080","#008080","#a52a2a"];',
    'const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;',
    'function start() {',
    '  const area = document.getElementById("area"); area.innerHTML = "";',
    '  const engine = Engine.create();',
    '  const render = Render.create({ element: area, engine: engine, options: { width: 500, height: 2200, wireframes: false, background: "#000" } });',
    '  const walls = [ Bodies.rectangle(250, 2190, 500, 20, { isStatic: true }), Bodies.rectangle(0, 1100, 20, 2200, { isStatic: true }), Bodies.rectangle(500, 1100, 20, 2200, { isStatic: true }) ];',
    '  const maze = [];',
    '  for(let i=0; i<12; i++) {',
    '    maze.push(Bodies.rectangle(130, 300+i*160, 320, 10, { isStatic: true, angle: 0.2, render: {fillStyle:"#333"} }));',
    '    maze.push(Bodies.rectangle(370, 380+i*160, 320, 10, { isStatic: true, angle: -0.2, render: {fillStyle:"#333"} }));',
    '  }',
    '  const spinners = [];',
    '  for(let i=0; i<7; i++) { spinners.push(Bodies.rectangle(250, 250+i*280, 140, 10, { isStatic: true, render: {fillStyle:"#ffd700"} })); }',
    '  const goal = Bodies.rectangle(250, 2175, 50, 20, { isStatic: true, isSensor: true, render: {visible: false} });',
    '  const balls = users.map((n, i) => Bodies.circle(250 + (Math.random()*20-10), -i*50, 11, { restitution: 0.6, frictionAir: 0.015, label: n, render: { fillStyle: colors[i % 10] } }));',
    '  Composite.add(engine.world, [...walls, ...maze, ...spinners, goal, ...balls]);',
    '  let finished = false;',
    '  Events.on(engine, "beforeUpdate", () => { spinners.forEach((s, i) => Body.rotate(s, i % 2 === 0 ? 0.1 : -0.1)); });',
    '  Events.on(engine, "collisionStart", (ev) => {',
    '    ev.pairs.forEach(p => {',
    '      const a = p.bodyA, b = p.bodyB;',
    '      if (a.circleRadius || b.circleRadius) { const ball = a.circleRadius ? a : b; const old = ball.render.fillStyle; ball.render.fillStyle = "#fff"; setTimeout(() => { if(ball.render) ball.render.fillStyle = old; }, 100); }',
    '      if (!finished && (a === goal || b === goal)) { const ball = a === goal ? b : a; if (ball.label) { finished = true; alert("🏆 당첨자: " + ball.label); } }',
    '    });',
    '  });',
    '  Render.run(render); Runner.run(Runner.create(), engine);',
    '}',
    'document.getElementById("btn").onclick = start;',
    '</script>'
]

# 리스트를 문자열로 합쳐서 출력
final_html = "".join(js_lines)
components.html(final_html, height=2300, scrolling=True)
