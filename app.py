import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="익스트림 핀볼", layout="wide")

st.title("🎲 비연속·불규칙 핀볼 추첨기")
st.info("왼쪽 사이드바에서 이름을 입력하고 '레이스 시작' 버튼을 누르세요!")

# 2. 참가자 설정 (사이드바)
with st.sidebar:
    st.header("👥 참가자 명단")
    p_names = []
    for i in range(10):
        val = st.text_input(f"{i+1}번", f"참가자 {i+1}", key=f"u_{i}")
        p_names.append(val)

# 3. HTML/JS 통합 코드 (가장 안전한 방식)
# 파이썬 변수를 직접 넣지 않고 마지막에 replace로 주입합니다.
html_content = """
<div style="text-align:center; font-family: sans-serif;">
    <h1 id="winner-display" style="color: #FFD700; height: 50px;"></h1>
    <button id="start-btn" style="padding:15px 40px; font-size:22px; border-radius:50px; background:linear-gradient(45deg, #00d2ff, #3a7bd5); color:white; border:none; cursor:pointer; font-weight:bold; box-shadow:0 4px 15px rgba(0,0,0,0.3);">🚀 레이스 시작!</button>
    <div id="canvas-holder" style="margin-top:20px;"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
const playerNames = NAMES_JSON;
const colors = ["#ff5733","#33ff57","#3357ff","#f333ff","#f3ff33","#33fff3","#ffa500","#800080","#008080","#a52a2a"];

const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;

document.getElementById('start-btn').onclick = function() {
    const holder = document.getElementById("canvas-holder");
    const display = document.getElementById("winner-display");
    
    // 초기화
    holder.innerHTML = "";
    display.innerText = "경주 중...";
    
    const engine = Engine.create();
    const render = Render.create({
        element: holder,
        engine: engine,
        options: { width: 500, height: 2600, wireframes: false, background: "#0f0f12" }
    });
    
    // 외곽 벽
    const walls = [
        Bodies.rectangle(250, 2590, 500, 20, { isStatic: true, render: {fillStyle: "#333"} }),
        Bodies.rectangle(0, 1300, 20, 2600, { isStatic: true, render: {fillStyle: "#333"} }),
        Bodies.rectangle(500, 1300, 20, 2600, { isStatic: true, render: {fillStyle: "#333"} })
    ];

    // 비연속적 작은 바 (무작위 배치)
    const obstacles = [];
    for(let i=0; i<50; i++) {
        let x = Math.random() * 440 + 30;
        let y = 300 + i * 45;
        let w = Math.random() * 50 + 30; // 30~80 사이의 아주 작은 바
        let ang = (Math.random() - 0.5) * 2;
        obstacles.push(Bodies.rectangle(x, y, w, 8, { 
            isStatic: true, 
            angle: ang, 
            render: { fillStyle: "#444" } 
        }));
    }

    // 작아진 회전 바 (중간중간 배치)
    const spinners = [];
    for(let i=0; i<10; i++) {
        let sx = Math.random() * 300 + 100;
        let sy = 450 + i * 200;
        spinners.push(Bodies.rectangle(sx, sy, 50, 8, { 
            isStatic: true, 
            render: { fillStyle: "#FFD700" } 
        }));
    }

    // 도착 센서
    const goal = Bodies.rectangle(250, 2570, 60, 20, { isStatic: true, isSensor: true, render: {visible: false} });

    // 공 생성
    const balls = playerNames.map((name, i) => {
        return Bodies.circle(250 + (Math.random()*40 - 20), -i * 50, 11, {
            restitution: 0.6,
            frictionAir: 0.015,
            label: name,
            render: { fillStyle: colors[i % 10], strokeStyle: "#fff", lineWidth: 2 }
        });
    });

    Composite.add(engine.world, [...walls, ...obstacles, ...spinners, goal, ...balls]);

    let finished = false;
    
    // 애니메이션 (회전 바 돌리기)
    Events.on(engine, "beforeUpdate", () => {
        spinners.forEach((s, idx) => {
            Body.rotate(s, idx % 2 === 0 ? 0.12 : -0.12);
        });
    });

    // 충돌 감지
    Events.on(engine, "collisionStart", (event) => {
        event.pairs.forEach(pair => {
            const { bodyA, bodyB } = pair;
            
            // 번쩍이는 효과
            if (bodyA.circleRadius || bodyB.circleRadius) {
                const ball = bodyA.circleRadius ? bodyA : bodyB;
                const oldC = ball.render.fillStyle;
                ball.render.fillStyle = "#fff";
                setTimeout(() => { if(ball.render) ball.render.fillStyle = oldC; }, 80);
            }

            // 도착 판정
            if (!finished && (bodyA === goal || bodyB === goal)) {
                const ball = bodyA === goal ? bodyB : bodyA;
                if (ball.label) {
                    finished = true;
                    display.innerText = "🏆 당첨자: " + ball.label + "!";
                    display.style.fontSize = "30px";
                    // 승자 공만 강조
                    ball.render.lineWidth = 10;
                    ball.render.strokeStyle = "#FFD700";
                }
            }
        });
    });

    Render.run(render);
    Runner.run(Runner.create(), engine);
};
</script>
"""

# 데이터 주입
final_html = html_content.replace("NAMES_JSON", json.dumps(p_names))

# 출력
components.html(final_html, height=2800, scrolling=True)
