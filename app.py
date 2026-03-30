import streamlit as st
from openai import OpenAI

# 1. API 키 설정 (본인의 키를 입력하세요)
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def generate_complaint(user_input):
    """사용자의 입력을 공공기관 민원 서식으로 변환하는 함수"""
    prompt = f"""
    당신은 공공기관 민원 작성 전문가입니다. 
    다음은 시민의 불편 사항입니다: "{user_input}"
    
    위 내용을 바탕으로 아래 양식에 맞춰 정중하고 논리적인 민원 초안을 작성하세요.
    1. 제목: (핵심을 담은 요약)
    2. 민원 요지: (어떤 문제인지 한 문장 정리)
    3. 현황 및 문제점: (현재 상태와 이로 인한 불편사항)
    4. 요청 사항: (기관에 바라는 구체적인 조치)
    
    문체는 '했습니다', '바랍니다'와 같은 공손한 격식체를 사용하세요.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 2. 웹 화면 구성 (Streamlit)
st.title("🏛️ 스마트 민원 작성 도우미")
st.write("불편하신 내용을 편하게 적어주세요. AI가 공식 서식으로 바꿔드립니다.")

user_text = st.text_area("내용을 입력하세요 (예: 집 앞 가로등이 일주일째 안 들어와서 밤에 너무 무서워요!!)", height=150)

if st.button("민원 초안 만들기"):
    if user_text:
        with st.spinner('AI가 법적 용어를 섞어 예쁘게 다듬는 중입니다...'):
            result = generate_complaint(user_text)
            st.success("작성이 완료되었습니다!")
            st.divider()
            st.markdown(result)
    else:
        st.warning("내용을 입력해 주세요.")
