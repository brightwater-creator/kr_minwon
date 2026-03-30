import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="핀볼 당첨자 뽑기", layout="centered")

st.title("🎡 핀볼 당첨자 뽑기")
st.write("10명의 참가자 중 단 한 명의 주인공을 뽑습니다! '게임 시작'을 눌러주세요.")

# 사용자 이름 입력 (선택 사항)
names = []
cols = st.columns(5)
for i in range(10):
    name = cols[i % 5].text_input(f"{i+1}번 이름", f"참가자 {i+1}", key=f"name_{i}")
    names.append(name)

# JavaScript 기반 물리 엔진 (Matter.js 사용)
pinball_html = f"""
<div id="container" style="text-align:center;">
    <button id="start-btn" style="padding: 10px 20px; font-size: 16px; cursor: pointer; background-color: #4CAF50; color: white; border: none; border-radius: 5px; margin-bottom: 10px;">🚀 게임 시작!</button>
    <div id="canvas-container"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
const names = {names};
const colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#F3FF33', '#33FFF3', '#FFA500', '#800080', '#008080', '#A52A2A'];

const {{ Engine, Render, Runner, Bodies, Composite, Events }} = Matter;

let engine, render, runner;
let winnerDeclared = false;

function initGame() {{
    const container = document.getElementById('canvas-container');
    container.innerHTML = ''; // 초기화
    
    engine = Engine.create();
    render = Render.create({{
        element: container,
        engine: engine,
        options: {{ width: 400, height: 600, wireframes: false, background: '#f9f9f9' }}
    }});

    // 벽 및 깔때기 설계
    const ground = Bodies.rectangle(200, 610, 410, 60, {{ isStatic: true }});
    const leftWall = Bodies.rectangle(-10, 300, 20, 600, {{ isStatic: true }});
    const rightWall = Bodies.rectangle(410, 300, 20, 600, {{ isStatic: true }});
    
    // 깔때기 (Funnel)
    const leftFunnel = Bodies.rectangle(100, 550, 250, 10, {{ isStatic: true, angle: Math.PI / 6 }});
    const rightFunnel = Bodies.rectangle(300, 550, 250, 10, {{ isStatic: true, angle: -Math.PI / 6 }});
    
    // 골인 지점 센서
    const sensor = Bodies.rectangle(200, 590, 40, 20, {{ isStatic: true, isSensor: true, render: {{ fillStyle: 'transparent' }} }});

    // 장애물 (Pins)
    const pins = [];
    for (let i = 0; i < 7; i++) {{
        for (let j = 0; j < (i % 2 === 0 ? 6 : 5); j++) {{
            pins.push(Bodies.circle(60 + j * 60 + (i % 2 === 0 ? 0 : 30), 150 + i * 50, 5, {{ isStatic: true, render: {{ fillStyle: '#444' }} }}));
        }}
    }}

    Composite.add(engine.world, [ground, leftWall, rightWall, leftFunnel, rightFunnel, sensor, ...pins]);

    // 공 생성
    const balls = names.map((name, i) => {{
        return Bodies.circle(200 + (Math.random() * 40 - 20), -i * 30, 12, {{
            restitution: 0.5,
            render: {{ fillStyle: colors[i] }},
            label: name
        }});
    }});

    Composite.add(engine.world, balls);
    
    // 충돌 감지 (승자 확인)
    Events.on(engine, 'collisionStart', (event) => {{
        event.pairs.forEach((pair) => {{
            if (!winnerDeclared && (pair.bodyA === sensor || pair.bodyB === sensor)) {{
                const ball = pair.bodyA === sensor ? pair.bodyB : pair.bodyA;
                if (ball.label && names.includes(ball.label)) {{
                    winnerDeclared = true;
                    alert("축하합니다! 당첨자는: " + ball.label);
                }}
            }}
        }});
    }});

    Render.run(render);
    runner = Runner.create();
    Runner.run(runner, engine);
}}

document.getElementById('start-btn').addEventListener('click', () => {{
    winnerDeclared = false;
    initGame();
}});
</script>
"""

components.html(pinball_html, height=700)

st.info("💡 각 공은 입력한 이름 순서대로 색상이 지정됩니다. 깔때기 맨 아래 구멍에 가장 먼저 도달하는 공이 승리합니다!")
