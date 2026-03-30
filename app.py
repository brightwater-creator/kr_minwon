import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="익스트림 핀볼", layout="wide")

st.title("🎲 예측불가! 비연속 핀볼 추첨")
st.write("바가 작아지고 장애물이 흩어졌습니다. 공이 어디로 튈지 모릅니다!")

# 2. 참가자 설정 (사이드바)
with st.sidebar:
    st.header("👥 참가자 명단")
    p_names = []
    for i in range(10):
        val = st.text_input(f"{i+1}번", f"참가자 {i+1}", key=f"user_{i}")
        p_names.append(val)

# 3. JS 코드를 한 줄씩 리스트로 관리 (에러 방지)
js_parts = [
    '<div id="root" style="text-align:center;">',
    '<button id="start" style="padding:15px 35px;font-size:20px;border-radius:50px;background:#00d2ff;color:white;border:none;cursor:pointer;font-weight:bold;box-shadow:0 4px 15px rgba(0,210,255,0.4);">🏁 경기 시작!</button>',
    '<div id="game-area" style="margin-top:20px;"></div>',
    '</div>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>',
    '<script>',
    'const users = ' + json.dumps(p_names) + ';',
    'const colors = ["#ff5733","#33ff57","#3357ff","#f333ff","#f3ff33","#33fff3","#ffa500","#800080","#008080","#a52a2a"];',
    'const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;',
    'function runGame() {',
    '  const area = document.getElementById("game-area"); area.innerHTML = "";',
    '  const engine = Engine.create();',
    '  const render = Render.create({ element: area, engine: engine, options: { width: 500, height: 2600, wireframes: false, background: "#0a0a0a" } });',
    '  const walls = [ Bodies.rectangle(250, 2590, 500, 20, { isStatic: true }), Bodies.rectangle(0, 1300, 20, 2600, { isStatic: true }), Bodies.rectangle(500, 1300, 20, 2600, { isStatic: true }) ];',
    '',
    '  // 비연속적인 장애물 (Maze) - 짧고 무작위 배치',
    '  const obstacles = [];',
    '  for(let i=0; i<40; i++) {',
    '    let x = Math.random() * 400 + 50;',
    '    let y = 300 + i * 50;',
    '    let w = Math.random() * 60 + 40; // 바 길이를 40~100 사이로 짧게',
    '    let ang = (Math.random() - 0.5) * 1.5;',
    '    obstacles.append = Bodies.rectangle(x, y, w, 8, { isStatic: true, angle: ang, render: {fillStyle:"#444"} });',
    '    obstacles.push(obstacles.append);',
    '  }',
    '',
    '  // 더 작아진 회전 바 (Spinners) - 크기 140 -> 60으로 축소',
    '  const spinners = [];',
    '  for(let i=0; i<12; i++) {',
    '    let sx = Math.random() * 300 + 100;',
    '    let sy = 400 + i * 180;',
    '    spinners.push(Bodies.rectangle(sx, sy, 60, 8, { isStatic: true, render: {fillStyle: "#ffd700"} }));',
    '  }',
    '',
    '  const goal = Bodies.rectangle(250, 2575, 40, 20, { isStatic: true, isSensor: true, render: {visible: false} });',
    '  const balls = users.map((n, i) => Bodies.circle(250 + (Math.random()*40-20), -i*70, 10, { restitution: 0.7, frictionAir: 0.012, label: n, render: { fillStyle: colors[i % 10], strokeStyle:"#fff", lineWidth:2 } }));',
    '',
    '  Composite.add(engine.world, [...walls, ...obstacles, ...spinners, goal, ...balls]);',
    '',
    '  let done = false;',
    '  Events.on(engine, "beforeUpdate", () => { spinners.forEach((s, i) => Body.rotate(s, i % 2 === 0 ? 0.15 : -0.15)); });',
    '',
    '  Events.on(engine, "collisionStart", (ev) => {',
    '    ev.pairs.forEach(p => {',
    '      const a = p.bodyA, b = p.bodyB;',
    '      if (a.circleRadius || b.circleRadius) { ',
    '        const ball = a.circleRadius ? a : b;',
    '        const oldC = ball.render.fillStyle; ball.render.fillStyle = "#fff";',
    '        setTimeout(() => { if(ball.render) ball.render.fillStyle = oldC; }, 80);',
    '      }',
    '      if (!done && (a === goal || b === goal)) {',
    '        const ball = a === goal ? b : a;',
    '        if (ball.label) { done = true; alert("🏆 최종 당첨자: " + ball.label); }',
    '      }',
    '    });',
    '  });',
    '  Render.run(render); Runner.run(Runner.create(), engine);',
    '}',
    'document.getElementById("start").onclick = runGame;',
    '</script>'
]

# 결합 및 출력
final_html = "".join(js_parts)
components.html(final_html, height=2700, scrolling=True)
