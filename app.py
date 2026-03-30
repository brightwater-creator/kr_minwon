import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="민원 작성 도우미", page_icon="🏛️")

st.title("🏛️ 스마트 민원 작성 도우미")
st.info("💡 입력하신 내용을 바탕으로 공식 민원 초안을 만들어 드립니다.")
st.caption("🔒 개인정보 보호: 이름, 상세 주소 등은 제외하고 상황 위주로 입력해 주세요.")

# 2. API 키 및 모델 설정
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # [수정 포인트] 최신 표준 모델명인 gemini-1.5-pro를 사용합니다.
        model = genai.GenerativeModel('gemini-1.5-pro') 
    else:
        st.error("⚠️ 설정 오류: Streamlit Secrets에 'GOOGLE_API_KEY'가 없습니다.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ 연결 오류: {str(e)}")
    st.stop()

# 3. 민원 생성 함수
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
        # 모델 생성을 시도합니다.
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        else:
            return "❌ AI가 답변을 생성하지 못했습니다. 내용을 더 자세히 적어주세요."
    except Exception as e:
        # 만약 404 에러가 나면 다른 모델로 한 번 더 시도합니다.
        if "404" in str(e):
            try:
                alt_model = genai.GenerativeModel('gemini-1.5-flash')
                response = alt_model.generate_content(prompt)
                return response.text
            except:
                return "❌ 현재 구글 API에서 사용할 수 있는 모델이 없습니다. API 키 설정을 확인해 주세요."
        return f"❌ 오류 발생: {str(e)}"

# 4. 사용자 입력 및 결과 출력
user_text = st.text_area(
    "민원 내용을 적어주세요", 
    placeholder="예: 우리 동네 놀이터 그네가 끊어져 있어요. 수리 부탁드려요.",
    height=200
)

if st.button("민원 초안 생성하기 ✨"):
    if user_text.strip():
        with st.spinner('AI가 분석 중입니다...'):
            result = generate_complaint(user_text)
            st.success("✅ 작성이 완료되었습니다!")
            st.divider()
            st.markdown(result)
    else:
        st.warning("내용을 입력해 주세요.")

st.divider()
st.caption("© 2026 민원 작성 도우미 | Powered by Google Gemini")
