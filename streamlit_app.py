import streamlit as st
import random
import re

# --- Helper functions (from app.py, unchanged) ---
# (Paste all helper functions: get_job_category, generate_job_specific_content, analyze_recruitment_requirements, match_experience_with_requirements, extract_job_title, generate_personality_traits, generate_motivation, generate_conclusion, enhance_introduction, generate_cover_letter)

# --- Paste all helper functions here ---

# ... (functions from app.py) ...

# For brevity, only the main Streamlit UI is shown here. The actual code will include all helper functions from app.py.
def generate_cover_letter(data):
    # 각 항목이 비어있을 수도 있으니 get()으로 안전하게 접근
    name = data.get('name', '')
    major = data.get('major', '')
    company_type = data.get('company_type', '')
    job_title = data.get('job_title', '')
    recruitment_requirements = data.get('recruitment_requirements', '')
    introduction = data.get('introduction', '')
    major_experience = data.get('major_experience', '')
    personality = data.get('personality', '')
    motivation = data.get('motivation', '')
    conclusion = data.get('conclusion', '')

    # 자기소개서 템플릿
    cover_letter = f"""안녕하세요, {name}입니다.

저는 {major}을(를) 전공하며 {introduction if introduction else '성실함과 책임감을 갖고 있습니다.'}라는 강점을 가지고 있습니다.

{company_type}의 {job_title} 직무에 지원하게 된 이유는 {motivation if motivation else '해당 직무에 큰 관심과 열정이 있기 때문입니다.'}

학업 및 다양한 경험을 통해 {major_experience if major_experience else '여러 프로젝트와 활동'}의 소중함을 배웠고, 이를 바탕으로 지원한 직무에 큰 기여를 할 수 있다고 생각합니다.

저의 성격적 장점은 {personality if personality else '적극적이고 협업을 잘하는 점'}입니다.

채용공고에서 요구하는 {recruitment_requirements if recruitment_requirements else '역량'}을 갖추기 위해 꾸준히 노력해왔습니다.

마지막으로, {conclusion if conclusion else '귀사에서 성장하며 함께 발전하고 싶습니다.'}

감사합니다.
"""
    return cover_letter
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
