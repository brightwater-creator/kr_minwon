import streamlit as st
import google.generativeai as genai

# ==============================
# 1. 페이지 설정 및 보안 안내
# ==============================
st.set_page_config(page_title="민원 작성 도우미", page_icon="🏛️")

st.title("🏛️ 스마트 민원 작성 도우미")
st.info("💡 본 서비스는 입력하신 내용을 바탕으로 공식 민원 초안을 만들어 드립니다.")
st.caption("🔒 **개인정보 보호 안내**: 입력하신 내용은 별도로 저장되지 않습니다. 이름, 상세 주소 등 민감한 개인정보는 제외하고 입력해 주세요.")

# ==============================
# 2. API 키 및 모델 설정 (수정된 부분)
# ==============================
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 'gemini-1.5-flash' 대신 가장 안정적인 'gemini-pro'를 사용합니다.
        model = genai.GenerativeModel('gemini-pro') 
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
        # 안전한 생성을 위한 설정 추가
        response = model.generate_content(prompt)
        
        # 만약 결과가 비어있다면 오류 메시지 반환
        if response and response.text:
            return response.text
        else:
            return "❌ AI가 답변을 생성하지 못했습니다. 내용을 조금 더 자세히 적어주세요."
            
    except Exception as e:
        # 상세 오류 메시지 출력 (디버깅용)
        return f"❌ AI 생성 중 오류가 발생했습니다: {str(e)}"

# ==============================
# 4. 사용자 입력 및 결과 출력
# ==============================
user_text = st.text_area(
    "민원 내용을 자유롭게 적어주세요", 
    placeholder="예: 우리 동네 가로등이 꺼져서 밤길이 너무 어두워요. 조치 부탁드려요.",
    height=200
)

if st
