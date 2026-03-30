import streamlit as st
import google.generativeai as genai

# ==============================
# 1. API 키 설정 (구글 Gemini용)
# ==============================
# Streamlit Secrets에서 'GOOGLE_API_KEY'라는 이름의 키를 가져옵니다.
# (나중에 Streamlit 관리 화면 설정에서 이 키를 입력해야 합니다.)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # 모델 설정 (성능과 속도의 균형이 좋은 flash 모델 추천)
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    st.error("⚠️ API 키 설정이 필요합니다. 오른쪽 하단 [Settings] -> [Secrets]에 GOOGLE_API_KEY를 입력해 주세요.")
    st.stop() # 키가 없으면 앱 실행 중단

def generate_complaint_with_gemini(user_input):
    """사용자의 입력을 구글 Gemini를 활용해 공공기관 민원 서식으로 변환하는 함수"""
    
    # AI에게 주는 구체적인 역할과 형식 지침 (페르소나)
    prompt = f"""
    당신은 대한민국 공공기관 민원 처리 전문가이자, 민원인의 입장을 대변하는 전문 작가입니다.
    
    [미션]
    아래 [민원 내용]을 바탕으로 공공기관에 제출할 수 있는 정중하고, 논리적이며, 격식 있는 민원 초안을 작성하세요.
    
    [민원 내용] (시민의 하소연)
    "{user_input}"
    
    [작성 지침]
    1. **어조:** 매우 공손하고 격식 있는 '하십시오체' 또는 '해요체'를 사용하세요. (예: '요청합니다', '바랍니다')
    2. **구조:** 반드시 아래의 4단 구조를 따르세요.
       - **1. 제목:** 민원의 핵심 내용을 한 문장으로 요약한 명확한 제목.
       - **2. 민원 취지:** 본 민원을 제기하는 목적과 배경에 대한 간단한 설명.
       - **3. 현황 및 문제점:** 현재 상태와 이로 인해 발생하고 있는 구체적인 불편함이나 위험성.
       - **4. 요청 사항:** 해당 기관에 바라는 구체적이고 실현 가능한 조치 내용.
    3. **내용:** 사용자가 입력한 내용의 핵심을 놓치지 않으면서, 법적인 근거나 안전 문제를 언급하여 설득력을 높이세요.
    
    이제 위 지침에 따라 민원 초안을 Markdown 형식으로 깔끔하게 작성해 주세요.
    """

    try:
        # Gemini 모델에게 요청
        response = model.generate_content(prompt)
        
        # 결과 텍스트만 추출
        return response.text
    except Exception as e:
        return f"❌ AI 생성 중 오류가 발생했습니다: {str(e)}"

# ==============================
# 2. 웹 화면 구성 (Streamlit)
# ==============================
# 페이지 설정 (제목, 아이콘)
st.set_page_config(page_title="스마트 민원 도우미 (Gemini)", page_icon="🏛️")

# 메인 제목 및 설명
st.title("🏛️ 스마트 민원 작성 도우미 (무료)")
st.write("불편하신 내용을 편하게 적어주세요. 구글 Gemini AI가 공식 서식으로 무료로 다듬어 드립니다.")

# 입력 칸
user_text = st.text_area(
    "내용을 입력하세요", 
    placeholder="예: 집 앞 가로등이 일주일째 안 들어와서 밤에 너무 무서워요!! 층간 소음 때문에 잠을 못 자겠어요.",
    height=180
)

# 버튼 및 로직 실행
if st.button("민원 초안 만들기 ✨"):
    if not user_text:
        st.warning("내용을 입력해 주세요.")
    elif len(user_text) < 10:
        st.warning("조금 더 자세한 내용을 적어주셔야 정확한 초안이 나옵니다. (10자 이상)")
    else:
        # 로딩 애니메이션
        with st.spinner('구글 Gemini가 법적 용어를 섞어 예쁘게 다듬는 중입니다...'):
            result = generate_complaint_with_gemini(user_text)
            
            # 결과 출력
            st.success("작성이 완료되었습니다!")
            st.divider() # 구분선
            st.markdown(result) # Markdown 형식으로 결과 출력
            
            # (선택) 복사하기 유도
            st.caption("위 내용을 복사하여 국민신문고 등에 활용하세요.")

# 하단 정보
st.divider
