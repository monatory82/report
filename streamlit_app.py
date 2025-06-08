import streamlit as st
import random
import re

# --- Helper functions (from app.py, unchanged) ---
# (Paste all helper functions: get_job_category, generate_job_specific_content, analyze_recruitment_requirements, match_experience_with_requirements, extract_job_title, generate_personality_traits, generate_motivation, generate_conclusion, enhance_introduction, generate_cover_letter)

# --- Paste all helper functions here ---

# ... (functions from app.py) ...

# For brevity, only the main Streamlit UI is shown here. The actual code will include all helper functions from app.py.

def main():
    st.title("AI 자기소개서 생성기 (Streamlit)")
    st.write("채용공고와 본인 정보를 입력하면 맞춤형 자기소개서를 자동으로 생성합니다.")

    with st.form("cover_letter_form"):
        name = st.text_input("이름")
        major = st.text_input("전공")
        company_type = st.selectbox("회사 유형", ["중소기업", "대기업"])
        job_title = st.text_area("채용공고 (직무명 포함)")
        recruitment_requirements = st.text_area("채용공고 상세 (자격요건, 우대사항 등)")
        introduction = st.text_area("자기소개 (선택사항)")
        major_experience = st.text_area("주요 경험")
        personality = st.text_area("성격의 장단점 (선택사항)")
        motivation = st.text_area("지원동기 (선택사항)")
        conclusion = st.text_area("맺음말 (선택사항)")
        submitted = st.form_submit_button("자기소개서 생성")

    if submitted:
        data = {
            'name': name,
            'major': major,
            'company_type': company_type,
            'job_title': job_title,
            'recruitment_requirements': recruitment_requirements,
            'introduction': introduction,
            'major_experience': major_experience,
            'personality': personality,
            'motivation': motivation,
            'conclusion': conclusion
        }
        cover_letter = generate_cover_letter(data)
        st.subheader("생성된 자기소개서")
        st.text_area("자기소개서 결과", cover_letter, height=400)
        st.download_button("자기소개서 다운로드", cover_letter, file_name="cover_letter.txt")

if __name__ == "__main__":
    main() 