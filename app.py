계속되는 SyntaxError 때문에 정말 답답하시죠? 파이썬에서 긴 문자열(HTML/JS)을 다룰 때, 따옴표 하나만 어긋나도 전체가 깨지기 때문입니다.

특히 깃허브나 웹 에디터에서 복사할 때 줄바꿈이 생기거나 따옴표가 잘리는 경우가 많습니다. 이번에는 에러를 물리적으로 방지하기 위해, 아예 HTML 부분을 별도의 변수로 분리하고 가장 안전한 방식으로 코드를 다시 작성했습니다.

이 코드를 파일의 첫 줄부터 마지막 줄까지 전체 선택해서 한 번에 덮어씌워 보세요.

🛠️ 최종 해결 버전 (app.py)
Python
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
        # 기본 이름 설정
        p_name = st.text_input(f"{i+1}번 참가자", f"참가자 {i+1}", key=f"p_{i}")
        player_names.append(p_name)

# 3. HTML/JS 템플릿 (가장 안전한 일반 문자열 방식)
# 아래 문자열 내부에는 파이썬 변수를 넣지 않고, 나중에 replace로 치환합니다.
html_template = """
<div id="container" style="text-align:center;">
    <button id="start-btn" style="padding: 15px 30px; font-size: 20px; cursor: pointer; background: linear-gradient(45deg, #FF512F, #DD2476); color: white; border: none; border-radius: 50px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">🚀 게임 시작!</button>
    <div id="canvas-container"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
// 데이터 주입 포인트
const names = NAMES_DATA_PLACEHOLDER;
const colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#F3FF33", "#33FFF3", "#FFA500", "#800080", "#008080", "#A52A2A"];

const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;

function initGame() {
    const container = document.getElementById("canvas-container");
    container.innerHTML = "";
    
    const engine = Engine.create();
    const world = engine.world;
    
    // 캔버스 높이를 2400으로 설정하여 약 15초 낙하 유도
    const render = Render.create({
        element: container,
        engine: engine,
        options: { width: 500, height: 2400, wireframes: false, background: "#0f0f0f" }
    });

    const wallOpts = { isStatic: true, render: { fillStyle: "#333" } };
    const ground = Bodies.rectangle(250, 2390, 500, 20, wallOpts);
    const leftWall = Bodies.rectangle(0, 1200, 20, 2400, wallOpts);
    const rightWall = Bodies.rectangle(500, 1200, 20, 2400, wallOpts);

    // 뱀 모양 미로 (지그재그)
    const maze = [];
    for(let i=0; i<10; i++) {
        let yPos = 350 + (i * 200);
        maze.push(Bodies.rectangle(130, yPos, 300, 15, { isStatic: true, angle: 0.2, render: { fillStyle: "#444" } }));
        maze.push(Bodies.rectangle(370, yPos + 100, 300, 15, { isStatic: true, angle: -0.2, render: { fillStyle: "#444" } }));
    }

    // 회전하는 바 (Spinners)
    const spinners = [];
    for(let i=0; i<8; i++) {
        let s = Bodies.rectangle(250, 250 + (i * 260), 150, 12, {
            isStatic: true, render: { fillStyle: "#FFD700" }, label: "spinner"
        });
        spinners.push(s);
    }

    // 하단 깔때기
    const lF = Bodies.rectangle(150, 2300, 350, 15, { isStatic: true, angle: 0.8 });
    const rF = Bodies.rectangle(350, 2300, 350, 15, { isStatic: true, angle: -0.8 });
    const sensor = Bodies.rectangle(250, 2380, 50, 20, { isStatic: true, isSensor: true, render: { fillStyle: "transparent" } });

    Composite.add(world, [ground, leftWall, rightWall, lF, rF, sensor, ...maze, ...spinners]);

    // 공 생성
    const balls = names.map((name, i) => {
        return Bodies.circle(250 + (Math.random()*40 - 20), -i * 60, 12, {
            restitution: 0.6, friction: 0.1, frictionAir: 0.012,
            render: { fillStyle: colors[i % colors.length], strokeStyle: "#fff", lineWidth: 2 },
            label: name
        });
    });
    Composite.add(world, balls);

    let winnerDeclared = false;
    Events.on(engine, "beforeUpdate", () => {
        spinners.forEach((s, idx) => { 
            Body.rotate(s, idx % 2 === 0 ? 0.1 : -0.1); 
        });
    });

    // 충돌 시 번쩍이는 효과 및 승자 체크
    Events.on(engine, "collisionStart", (event) => {
        event.pairs.forEach(pair => {
            const a = pair.bodyA;
            const b = pair.bodyB;
            if (a.circleRadius || b.circleRadius) {
                const ball = a.circleRadius ? a : b;
                const c = ball.render.fillStyle;
                ball.render.fillStyle = "#fff";
                setTimeout(() => { if(ball.render) ball.render.fillStyle = c; }, 70);
            }
            if (!winnerDeclared && (a === sensor || b === sensor)) {
                const ball = a === sensor ? b : a;
                if (ball.label) {
                    winnerDeclared = true;
                    alert("🏆 당첨자: " + ball.label);
                }
            }
        });
    });

    Render.run(render);
    Runner.run(Runner.create(), engine);
}
document.getElementById("start-btn").addEventListener("click", initGame);
</script>
"""

# 4. 데이터 주입 및 출력
final_html = html_template.replace("NAMES_DATA_PLACEHOLDER", json.dumps(player_names))
components.html(final_html, height=2500, scrolling=True)
