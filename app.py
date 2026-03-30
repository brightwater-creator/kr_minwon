import streamlit as st
import google.generativeai as genai

# ==============================
# 1. 페이지 설정 및 보안 안내
# ==============================
st.set_page_config(page_title="민원 작성 도우미", page_icon="🏛️")

# 상단 제목
st.title("🏛️ 스마트 민원 작성 도우미")
st.info("💡 본 서비스는 입력하신 내용을 바탕으로 공식 민원 초안을 만들어 드립니다.")

# 개인정보 보호 안내 (사용자 안심용)
st.caption("🔒 **개인정보 보호 안내**: 입력하신 내용은 AI 모델 처리를 위해 전송되지만, 별도로 저장되지 않습니다. 이름, 상세 주소, 연락처 등 민감한 개인정보는 제외하고 상황 위주로 입력해 주세요.")

# ==============================
# 2. API 키 및 모델 설정
# ==============================
try:
    # Streamlit Secrets에서 키 가져오기
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 가장 범용적인 모델명 사용 (오류 방지를 위해 flash와 pro 혼용 설정)
        model = genai.GenerativeModel('gemini-1.5-flash') 
    else:
        st.error("⚠️ 설정 오류: Streamlit Secrets에 'GOOGLE_API_KEY'가 등록되지 않았습니다.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ 연결 오류: {str(e)}")
    st.stop()

# ==============================
# 3. 민원 생성 함수
# ==============================
def generate_complaint(user_input):
    prompt = f"""
    당신은 대한민국 공공기관 민원 작성 전문가입니다. 
    다음 불편 사항을 바탕으로 정중하고 논리적인 공식 민원 초안을 작성하세요.
    
    내용: "{user_input}"
    
    [작성 양식]
    1. 제목: (핵심을 담은 요약)
    2. 민원 요지: (어떤 문제인지 한 문장 정리)
    3. 현황 및 문제점: (현재 상태와 불편함/위험성 설명)
    4. 요청 사항: (기관에 바라는 구체적인 조치)
    
    문체는 '바랍니다', '요청드립니다'와 같은 공손한 격식체를 사용하세요.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI 생성 중 오류가 발생했습니다: {str(e)}"

# ==============================
# 4. 사용자 입력 및 결과 출력
# ==============================
user_text = st.text_area(
    "민원 내용을 자유롭게 적어주세요", 
    placeholder="예: 우리 동네 놀이터 그네가 끊어져서 아이들이 다칠 것 같아요. 빨리 고쳐주세요!",
    height=200
)

if st.button("민원 초안 생성하기 ✨"):
    if user_text.strip():
        with st.spinner('AI가 내용을 분석하여 초안을 작성 중입니다...'):
            result = generate_complaint(user_text)
            st.success("✅ 작성이 완료되었습니다!")
            st.divider()
            st.markdown(result)
            st.button("다시 작성하기")
    else:
        st.warning("내용을 입력해 주세요.")

# 하단 푸터
st.divider()
st.caption("© 2026 민원 작성 도우미 | Powered by Google Gemini")
