from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

def get_job_category(job_title):
    # 직무 카테고리 매핑
    job_categories = {
        # 개발 직군
        "백엔드 개발자": "개발자",
        "프론트엔드 개발자": "개발자",
        "풀스택 개발자": "개발자",
        "웹 개발자": "개발자",
        "모바일 개발자": "개발자",
        "시스템 개발자": "개발자",
        "임베디드 개발자": "개발자",
        "AI 개발자": "개발자",
        
        # 마케팅 직군
        "디지털 마케터": "마케팅",
        "콘텐츠 마케터": "마케팅",
        "브랜드 마케터": "마케팅",
        "퍼포먼스 마케터": "마케팅",
        "마케팅 기획자": "마케팅",
        
        # 영업 직군
        "영업 관리자": "영업",
        "영업 대표": "영업",
        "해외 영업": "영업",
        "국내 영업": "영업",
        "영업 기획": "영업",
        
        # 디자인 직군
        "UI/UX 디자이너": "디자인",
        "그래픽 디자이너": "디자인",
        "웹 디자이너": "디자인",
        "브랜드 디자이너": "디자인",
        "모바일 디자이너": "디자인",
        
        # 기획 직군
        "서비스 기획자": "기획",
        "제품 기획자": "기획",
        "사업 기획자": "기획",
        "전략 기획자": "기획",
        "프로젝트 기획자": "기획"
    }
    
    return job_categories.get(job_title, "기타")

def generate_job_specific_content(job_title, experience, company_type="중소기업"):
    # 직무별 핵심 역량 키워드와 문구
    job_keywords = {
        "개발자": {
            "keywords": ["문제 해결 능력", "코딩 실력", "기술 스택", "프로젝트 경험", "협업 능력", "알고리즘", "시스템 설계", "코드 품질"],
            "phrases": [
                "기술적 도전을 즐기며 지속적인 성장을 추구합니다",
                "최신 기술 트렌드를 파악하고 적용하는 것을 즐깁니다",
                "효율적인 코드 작성과 시스템 설계에 관심이 많습니다",
                "사용자 중심의 서비스를 개발하는 것을 목표로 합니다"
            ],
            "sme_phrases": [
                "다양한 역할을 수행하며 폭넓은 경험을 쌓아왔습니다",
                "제한된 리소스 내에서도 효율적인 개발을 수행할 수 있습니다",
                "빠른 의사결정과 실행력으로 신속한 개발이 가능합니다",
                "다양한 기술 스택을 활용한 문제 해결 능력을 보유하고 있습니다"
            ]
        },
        "마케팅": {
            "keywords": ["시장 분석", "브랜딩", "소비자 인사이트", "데이터 분석", "전략 수립", "콘텐츠 제작", "캠페인 기획"],
            "phrases": [
                "데이터 기반의 마케팅 전략 수립에 강점이 있습니다",
                "소비자의 니즈를 정확히 파악하고 해결책을 제시합니다",
                "창의적인 브랜딩과 마케팅 전략을 수립합니다",
                "효과적인 마케팅 캠페인을 기획하고 실행합니다"
            ],
            "sme_phrases": [
                "제한된 예산 내에서도 효과적인 마케팅을 수행할 수 있습니다",
                "다양한 채널을 활용한 통합 마케팅 전략을 수립합니다",
                "빠른 시장 대응과 유연한 전략 수정이 가능합니다",
                "소규모 팀에서도 큰 성과를 만들어낼 수 있습니다"
            ]
        },
        "영업": {
            "keywords": ["고객 관계 관리", "매출 달성", "협상 능력", "시장 이해도", "네트워킹", "영업 전략", "고객 만족도"],
            "phrases": [
                "고객의 니즈를 정확히 파악하고 해결책을 제시합니다",
                "지속적인 매출 성장을 위한 전략을 수립합니다",
                "효과적인 고객 관계 구축과 유지에 강점이 있습니다",
                "시장 트렌드를 분석하고 영업 기회를 창출합니다"
            ],
            "sme_phrases": [
                "제한된 리소스 내에서도 효과적인 영업 활동을 수행합니다",
                "다양한 고객층과의 관계 구축에 강점이 있습니다",
                "빠른 의사결정으로 신속한 고객 대응이 가능합니다",
                "소규모 팀에서도 큰 매출을 달성할 수 있습니다"
            ]
        },
        "디자인": {
            "keywords": ["창의성", "시각적 표현", "사용자 경험", "트렌드 파악", "디자인 툴 활용", "브랜드 아이덴티티", "UI/UX"],
            "phrases": [
                "사용자 중심의 직관적인 디자인을 추구합니다",
                "트렌드를 선도하는 창의적인 디자인을 제시합니다",
                "브랜드 아이덴티티를 강화하는 디자인을 합니다",
                "사용자 경험을 고려한 디자인 솔루션을 제공합니다"
            ],
            "sme_phrases": [
                "제한된 리소스 내에서도 고품질 디자인을 제공합니다",
                "다양한 디자인 작업을 효율적으로 수행할 수 있습니다",
                "빠른 디자인 수정과 대응이 가능합니다",
                "소규모 팀에서도 전문적인 디자인 결과물을 만들어냅니다"
            ]
        },
        "기획": {
            "keywords": ["전략적 사고", "분석력", "의사소통", "프로젝트 관리", "문제 해결", "데이터 분석", "사업 기획"],
            "phrases": [
                "데이터 기반의 전략적 의사결정을 합니다",
                "효율적인 프로젝트 관리와 리더십을 발휘합니다",
                "창의적인 문제 해결 능력을 보유하고 있습니다",
                "사업 성장을 위한 혁신적인 기획을 제시합니다"
            ],
            "sme_phrases": [
                "제한된 리소스 내에서도 효율적인 기획을 수행합니다",
                "다양한 역할을 수행하며 폭넓은 경험을 쌓아왔습니다",
                "빠른 의사결정과 실행력으로 신속한 프로젝트 진행이 가능합니다",
                "소규모 팀에서도 큰 성과를 만들어낼 수 있습니다"
            ]
        }
    }
    
    # 기본 키워드와 문구 (직무가 매칭되지 않을 경우)
    default_content = {
        "keywords": ["문제 해결 능력", "의사소통 능력", "팀워크", "책임감", "성장 의지", "전문성", "리더십"],
        "phrases": [
            "지속적인 성장과 발전을 추구합니다",
            "효율적인 문제 해결 능력을 보유하고 있습니다",
            "팀워크를 통한 시너지 창출을 목표로 합니다",
            "전문성을 바탕으로 가치 있는 성과를 만들어냅니다"
        ],
        "sme_phrases": [
            "다양한 역할을 수행하며 폭넓은 경험을 쌓아왔습니다",
            "제한된 리소스 내에서도 효율적인 업무 수행이 가능합니다",
            "빠른 의사결정과 실행력으로 신속한 업무 처리가 가능합니다",
            "소규모 팀에서도 큰 성과를 만들어낼 수 있습니다"
        ]
    }
    
    # 직무 카테고리 확인
    job_category = get_job_category(job_title)
    
    # 직무에 맞는 키워드와 문구 선택
    job_content = job_keywords.get(job_category, default_content)
    keywords = job_content["keywords"]
    phrases = job_content["phrases"]
    sme_phrases = job_content["sme_phrases"]
    
    # 중소기업 특화 문구 선택
    selected_phrases = sme_phrases if company_type == "중소기업" else phrases
    
    # 경험 기반 내용 생성
    experience_content = f"""
저는 {experience}의 경험을 통해 {random.choice(keywords)}을(를) 향상시켰습니다. 
특히 {random.choice(keywords)}에 대한 깊은 이해를 바탕으로 {random.choice(keywords)}을(를) 발전시켜 왔습니다.
{random.choice(selected_phrases)}. 이러한 경험과 역량을 바탕으로 귀사의 {job_title} 직무에서 큰 가치를 창출할 수 있을 것으로 확신합니다.
"""
    return experience_content

def analyze_recruitment_requirements(requirements_text):
    """채용공고의 자격요건과 우대사항을 더 정교하게 분석합니다."""
    requirements = {
        'qualifications': [],
        'preferred': [],
        'keywords': set(),
        'company_type': '중소기업',  # 기본값
        'industry': None,
        'tech_stack': set(),
        'soft_skills': set()
    }
    
    # 회사 유형 분석
    if any(keyword in requirements_text for keyword in ['대기업', '그룹사', '글로벌']):
        requirements['company_type'] = '대기업'
    
    # 산업 분야 분석
    industry_keywords = {
        'IT': ['IT', '소프트웨어', '개발', '프로그래밍', '시스템'],
        '금융': ['금융', '은행', '보험', '증권', '투자'],
        '제조': ['제조', '생산', '공장', '설비'],
        '서비스': ['서비스', '유통', '물류', '운송'],
        '미디어': ['미디어', '방송', '출판', '콘텐츠']
    }
    
    for industry, keywords in industry_keywords.items():
        if any(keyword in requirements_text for keyword in keywords):
            requirements['industry'] = industry
            break
    
    # 기술 스택 분석
    tech_keywords = {
        '프론트엔드': ['React', 'Vue', 'Angular', 'JavaScript', 'TypeScript', 'HTML', 'CSS'],
        '백엔드': ['Java', 'Spring', 'Python', 'Django', 'Node.js', 'PHP', 'MySQL', 'PostgreSQL'],
        '모바일': ['Android', 'iOS', 'Flutter', 'React Native'],
        '데이터': ['Python', 'R', 'SQL', 'Hadoop', 'Spark', 'TensorFlow'],
        '클라우드': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes']
    }
    
    for tech_type, keywords in tech_keywords.items():
        for keyword in keywords:
            if keyword in requirements_text:
                requirements['tech_stack'].add(keyword)
    
    # 소프트 스킬 분석
    soft_skill_keywords = {
        '의사소통': ['의사소통', '커뮤니케이션', '발표', '협상'],
        '리더십': ['리더십', '팀장', '프로젝트 관리', '멘토링'],
        '문제해결': ['문제해결', '분석', '전략', '기획'],
        '창의성': ['창의성', '혁신', '아이디어', '기획'],
        '적응력': ['적응력', '유연성', '스트레스 관리']
    }
    
    for skill_type, keywords in soft_skill_keywords.items():
        if any(keyword in requirements_text for keyword in keywords):
            requirements['soft_skills'].add(skill_type)
    
    # 자격요건과 우대사항 추출
    qual_pattern = r'자격요건[:\s]*([^우대사항]+)'
    pref_pattern = r'우대사항[:\s]*([^자격요건]+)'
    
    qual_match = re.search(qual_pattern, requirements_text)
    pref_match = re.search(pref_pattern, requirements_text)
    
    if qual_match:
        qualifications = qual_match.group(1).strip()
        requirements['qualifications'] = [q.strip() for q in qualifications.split('\n') if q.strip()]
    
    if pref_match:
        preferred = pref_match.group(1).strip()
        requirements['preferred'] = [p.strip() for p in preferred.split('\n') if p.strip()]
    
    # 키워드 추출
    all_text = ' '.join(requirements['qualifications'] + requirements['preferred'])
    words = re.findall(r'\w+', all_text)
    requirements['keywords'] = set(words)
    
    return requirements

def match_experience_with_requirements(experience, requirements):
    """경험과 자격요건을 더 정교하게 매칭합니다."""
    matched_points = []
    
    # 경험을 문장 단위로 분리
    experience_sentences = re.split(r'[.!?]+', experience)
    
    # 각 문장에 대한 점수 계산
    for sentence in experience_sentences:
        if not sentence.strip():
            continue
            
        score = 0
        matched_keywords = set()
        
        # 기술 스택 매칭
        for tech in requirements['tech_stack']:
            if tech in sentence:
                score += 3
                matched_keywords.add(tech)
        
        # 소프트 스킬 매칭
        for skill in requirements['soft_skills']:
            if skill in sentence:
                score += 2
                matched_keywords.add(skill)
        
        # 자격요건 키워드 매칭
        for keyword in requirements['keywords']:
            if keyword in sentence:
                score += 1
                matched_keywords.add(keyword)
        
        # 산업 관련 경험 매칭
        if requirements['industry'] and requirements['industry'] in sentence:
            score += 2
            matched_keywords.add(requirements['industry'])
        
        if score > 0:
            matched_points.append({
                'sentence': sentence.strip(),
                'score': score,
                'matched_keywords': matched_keywords
            })
    
    # 점수순으로 정렬
    matched_points.sort(key=lambda x: x['score'], reverse=True)
    
    # 상위 3개 경험 선택
    top_experiences = matched_points[:3]
    
    # 매칭된 경험을 자연스러운 문장으로 구성
    result = []
    for exp in top_experiences:
        sentence = exp['sentence']
        if not sentence.endswith('.'):
            sentence += '.'
        result.append(sentence)
    
    return '\n\n'.join(result)

def extract_job_title(recruitment_notice):
    """채용공고 제목에서 직무를 추출합니다."""
    # 직무 키워드 매핑
    job_keywords = {
        "개발": ["개발자", "개발", "프로그래머", "엔지니어", "소프트웨어"],
        "마케팅": ["마케터", "마케팅", "브랜드", "콘텐츠", "퍼포먼스"],
        "영업": ["영업", "세일즈", "영업관리", "해외영업"],
        "디자인": ["디자이너", "디자인", "UI/UX", "그래픽"],
        "기획": ["기획자", "기획", "서비스기획", "제품기획", "사업기획"]
    }
    
    # 채용공고 제목에서 직무 추출
    for job_type, keywords in job_keywords.items():
        for keyword in keywords:
            if keyword in recruitment_notice:
                return job_type
    
    return "일반"  # 직무를 찾지 못한 경우

def generate_personality_traits(recruitment_notice, requirements, company_type="중소기업"):
    """성격의 장단점을 더 정교하게 생성합니다."""
    job_title = extract_job_title(recruitment_notice)
    traits = []
    
    # 직무별 적합한 성격 특성
    job_traits = {
        "개발": {
            "장점": [
                "논리적 사고와 문제 해결 능력이 뛰어납니다",
                "새로운 기술을 배우는 것을 좋아합니다",
                "꼼꼼하고 정확한 업무 처리를 추구합니다",
                "팀원들과의 원활한 소통을 중요시합니다",
                "지속적인 자기계발을 통해 전문성을 키워나가고 있습니다"
            ],
            "단점": [
                "때로는 완벽주의적 성향이 업무 속도를 늦출 수 있습니다",
                "새로운 기술에 대한 관심이 많아 한 가지에 집중하기 어려울 때가 있습니다",
                "문제 해결에 집중하다 보니 휴식 시간을 놓치기 쉽습니다",
                "기술적 완성도에 집착하는 경향이 있습니다"
            ]
        },
        "마케팅": {
            "장점": [
                "창의적인 아이디어를 잘 떠올립니다",
                "트렌드에 대한 감각이 뛰어납니다",
                "적극적이고 활발한 성격으로 팀 분위기를 이끌어갑니다",
                "데이터 분석과 전략 수립에 관심이 많습니다",
                "고객의 니즈를 정확히 파악하는 능력이 있습니다"
            ],
            "단점": [
                "너무 많은 아이디어를 동시에 추진하려는 경향이 있습니다",
                "때로는 감성적인 판단을 할 수 있습니다",
                "빠른 변화를 추구하다 보니 인내심이 부족할 때가 있습니다",
                "데이터와 직관 사이에서 균형을 잡기 어려울 때가 있습니다"
            ]
        },
        "영업": {
            "장점": [
                "적극적이고 도전적인 성격입니다",
                "목표 지향적이고 성과를 중요시합니다",
                "대인관계가 원만하고 친화력이 좋습니다",
                "스트레스 관리 능력이 뛰어납니다",
                "고객의 니즈를 정확히 파악하는 능력이 있습니다"
            ],
            "단점": [
                "때로는 너무 적극적이어서 부담을 줄 수 있습니다",
                "목표 달성에 집중하다 보니 세부사항을 놓칠 수 있습니다",
                "빠른 의사결정을 선호하여 신중함이 부족할 때가 있습니다",
                "단기 성과에 집중하는 경향이 있습니다"
            ]
        }
    }
    
    # 기본 성격 특성
    default_traits = {
        "장점": [
            "책임감이 강하고 성실합니다",
            "적극적이고 도전적인 성격입니다",
            "팀워크를 중요시하고 협동심이 좋습니다",
            "새로운 것을 배우는 것을 좋아합니다",
            "문제 해결 능력이 뛰어납니다"
        ],
        "단점": [
            "때로는 완벽을 추구하다 보니 시간이 오래 걸릴 수 있습니다",
            "너무 많은 일을 동시에 진행하려는 경향이 있습니다",
            "스트레스 상황에서 인내심이 부족할 때가 있습니다",
            "때로는 너무 적극적이어서 주변의 의견을 놓칠 수 있습니다"
        ]
    }
    
    # 직무별 특성 선택
    selected_traits = job_traits.get(job_title, default_traits)
    
    # 소프트 스킬 기반 특성 추가
    if requirements['soft_skills']:
        soft_skill_traits = {
            '의사소통': "원활한 의사소통 능력을 바탕으로 팀 협업을 이끌어갑니다",
            '리더십': "책임감 있는 리더십으로 팀의 목표 달성을 이끌어갑니다",
            '문제해결': "창의적인 문제 해결 능력으로 새로운 해결책을 제시합니다",
            '창의성': "독창적인 아이디어로 혁신적인 결과를 만들어냅니다",
            '적응력': "빠른 환경 변화에 유연하게 대응합니다"
        }
        
        for skill in requirements['soft_skills']:
            if skill in soft_skill_traits:
                selected_traits["장점"].append(soft_skill_traits[skill])
    
    # 장점 2개, 단점 1개 선택
    traits.append("장점:")
    traits.extend([f"- {trait}" for trait in selected_traits["장점"][:2]])
    traits.append("\n단점:")
    traits.extend([f"- {trait}" for trait in selected_traits["단점"][:1]])
    
    # 회사 유형에 따른 특성 추가
    if company_type == "중소기업":
        traits.append("- 유연한 환경에서 빠르게 적응하고 새로운 역할을 수행할 수 있습니다")
        traits.append("- 창의적인 문제 해결 능력으로 실질적인 가치를 창출할 수 있습니다")
    else:
        traits.append("- 체계적인 시스템 속에서 전문성을 키워나갈 수 있습니다")
        traits.append("- 대규모 프로젝트에서의 협업 경험을 바탕으로 시너지를 만들어낼 수 있습니다")
    
    return "\n".join(traits)

def generate_motivation(recruitment_notice, major, experience, requirements, company_type="중소기업"):
    """지원동기를 더 자연스럽게 생성합니다."""
    job_title = extract_job_title(recruitment_notice)
    motivation = []
    
    # 직무 관련성 강조
    motivation.append(f"{recruitment_notice}에 지원하게 된 것은 제가 가진 {major} 전공 지식과 다양한 경험을 바탕으로 귀사에 실질적인 기여를 하고 싶기 때문입니다.")
    
    # 경험과 요구사항 연계
    if requirements['qualifications']:
        key_qual = requirements['qualifications'][0]
        motivation.append(f"특히 {key_qual}에 대한 저의 경험과 역량이 귀사의 요구사항과 잘 부합한다고 생각합니다.")
    
    # 우대사항 반영
    if requirements['preferred']:
        key_pref = requirements['preferred'][0]
        motivation.append(f"{key_pref}에 대한 저의 관심과 열정은 대학 시절부터 시작되었으며, 이를 실무에서도 큰 성과로 이어갈 수 있을 것이라 확신합니다.")
    
    # 기술 스택 언급
    if requirements['tech_stack']:
        tech_list = ', '.join(list(requirements['tech_stack'])[:3])
        motivation.append(f"{tech_list} 등 관련 기술에 대한 실무 경험을 바탕으로 빠르게 적응하고 기여할 수 있을 것입니다.")
    
    # 소프트 스킬 언급
    if requirements['soft_skills']:
        skill_list = ', '.join(list(requirements['soft_skills']))
        motivation.append(f"또한 {skill_list} 능력을 바탕으로 팀의 시너지를 높이고 실질적인 성과를 창출할 수 있을 것입니다.")
    
    # 회사 유형별 맞춤 표현
    if company_type == "중소기업":
        motivation.append("중소기업의 유연하고 창의적인 환경에서 빠르게 성장하며, 실질적인 가치를 창출하고 싶습니다.")
        motivation.append("다양한 역할을 수행할 수 있는 다재다능한 역량을 바탕으로 귀사의 성장에 기여하고 싶습니다.")
    else:
        motivation.append("대기업의 체계적인 시스템과 전문성을 갖춘 환경에서 더욱 성장하고 싶습니다.")
        motivation.append("체계적인 업무 수행 능력과 전문성을 바탕으로 귀사의 비전 실현에 기여하고 싶습니다.")
    
    # 산업별 특화 표현
    if requirements['industry']:
        industry_expressions = {
            'IT': "혁신적인 기술 솔루션을 통해 디지털 트랜스포메이션을 이끌어가고 싶습니다.",
            '금융': "금융 서비스의 혁신과 고객 가치 창출에 기여하고 싶습니다.",
            '제조': "제조업의 디지털화와 스마트 팩토리 구현에 기여하고 싶습니다.",
            '서비스': "고객 중심의 서비스 혁신과 경험 개선에 기여하고 싶습니다.",
            '미디어': "차별화된 콘텐츠와 서비스로 새로운 가치를 창출하고 싶습니다."
        }
        if requirements['industry'] in industry_expressions:
            motivation.append(industry_expressions[requirements['industry']])
    
    # 직무별 특화 표현
    if job_title == "개발":
        motivation.append("기술적 역량을 바탕으로 혁신적인 솔루션을 제공하고, 지속적인 학습을 통해 최신 기술 트렌드를 선도하는 개발자가 되겠습니다.")
    elif job_title == "마케팅":
        motivation.append("데이터 기반의 전략적 마케팅으로 실질적인 성과를 창출하고, 트렌드 분석과 창의적인 아이디어로 브랜드 가치를 높이는데 기여하겠습니다.")
    elif job_title == "영업":
        motivation.append("고객 중심의 영업 전략으로 실적을 창출하고, 장기적인 파트너십을 구축하는데 기여하겠습니다.")
    elif job_title == "디자인":
        motivation.append("사용자 중심의 디자인으로 제품의 가치를 높이고, 브랜드 아이덴티티를 강화하는데 기여하겠습니다.")
    elif job_title == "기획":
        motivation.append("전략적인 기획력으로 비즈니스 성장을 이끌고, 혁신적인 서비스 개발에 기여하겠습니다.")
    
    return "\n\n".join(motivation)

def generate_conclusion(recruitment_notice, requirements, company_type="중소기업"):
    """맺음말을 더 자연스럽게 생성합니다."""
    job_title = extract_job_title(recruitment_notice)
    conclusion = []
    
    # 핵심 역량 강조
    if requirements['qualifications']:
        key_qual = requirements['qualifications'][0]
        conclusion.append(f"{key_qual}에 대한 저의 역량과 열정을 바탕으로 귀사의 성장에 기여하고 싶습니다.")
    
    # 기술 스택 언급
    if requirements['tech_stack']:
        tech_list = ', '.join(list(requirements['tech_stack'])[:3])
        conclusion.append(f"{tech_list} 등 관련 기술에 대한 전문성을 바탕으로 실질적인 가치를 창출하겠습니다.")
    
    # 소프트 스킬 언급
    if requirements['soft_skills']:
        skill_list = ', '.join(list(requirements['soft_skills']))
        conclusion.append(f"{skill_list} 능력을 바탕으로 팀의 시너지를 높이고 성과를 창출하겠습니다.")
    
    # 미래 비전
    if company_type == "중소기업":
        conclusion.append("창의적이고 유연한 환경에서 빠르게 성장하며, 실질적인 가치를 창출하는 인재가 되겠습니다.")
    else:
        conclusion.append("체계적인 시스템과 전문성을 갖춘 환경에서 지속적으로 성장하며, 회사의 비전 실현에 기여하는 인재가 되겠습니다.")
    
    # 산업별 특화 표현
    if requirements['industry']:
        industry_expressions = {
            'IT': "혁신적인 기술 솔루션을 통해 디지털 트랜스포메이션을 이끄는 개발자가 되겠습니다.",
            '금융': "금융 서비스의 혁신과 고객 가치 창출에 기여하는 전문가가 되겠습니다.",
            '제조': "제조업의 디지털화와 스마트 팩토리 구현에 기여하는 인재가 되겠습니다.",
            '서비스': "고객 중심의 서비스 혁신과 경험 개선에 기여하는 전문가가 되겠습니다.",
            '미디어': "차별화된 콘텐츠와 서비스로 새로운 가치를 창출하는 인재가 되겠습니다."
        }
        if requirements['industry'] in industry_expressions:
            conclusion.append(industry_expressions[requirements['industry']])
    
    # 직무별 특화 표현
    if job_title == "개발":
        conclusion.append("기술적 역량을 바탕으로 혁신적인 솔루션을 제공하는 개발자가 되겠습니다.")
    elif job_title == "마케팅":
        conclusion.append("데이터 기반의 전략적 마케팅으로 실질적인 성과를 창출하는 마케터가 되겠습니다.")
    elif job_title == "영업":
        conclusion.append("고객 중심의 영업 전략으로 실적을 창출하는 영업 전문가가 되겠습니다.")
    elif job_title == "디자인":
        conclusion.append("사용자 중심의 디자인으로 제품의 가치를 높이는 디자이너가 되겠습니다.")
    elif job_title == "기획":
        conclusion.append("전략적인 기획력으로 비즈니스 성장을 이끄는 기획자가 되겠습니다.")
    
    # 마무리
    conclusion.append("귀사의 일원이 되어 함께 성장하고 싶습니다. 기회를 주시면 최선을 다하겠습니다.")
    
    return "\n\n".join(conclusion)

def enhance_introduction(introduction, requirements, company_type="중소기업"):
    """자기소개를 강화하고 모집요강과 연계합니다."""
    enhanced = introduction.strip()
    
    # 모집요강의 자격요건과 연계
    if requirements['qualifications']:
        key_qual = requirements['qualifications'][0]  # 첫 번째 자격요건을 주요 키워드로 사용
        enhanced += f"\n\n{key_qual}에 대한 저의 관심과 열정은 대학 시절부터 시작되었습니다. "
        enhanced += "이를 바탕으로 실무에서도 큰 성과를 낼 수 있을 것이라 확신합니다."
    
    # 회사 유형에 따른 표현 추가
    if company_type == "중소기업":
        enhanced += "\n\n창의적이고 유연한 환경에서 빠르게 성장하고 싶은 열망이 있습니다. "
        enhanced += "중소기업의 특성을 잘 활용하여 실질적인 가치를 창출하고 싶습니다."
    else:
        enhanced += "\n\n체계적인 시스템과 전문성을 갖춘 환경에서 더욱 성장하고 싶습니다. "
        enhanced += "대기업의 다양한 리소스를 활용하여 큰 시너지를 만들어내고 싶습니다."
    
    return enhanced

def generate_cover_letter(data):
    """입력된 데이터를 바탕으로 자기소개서를 생성합니다."""
    # 모집요강 분석
    requirements = analyze_recruitment_requirements(data['recruitment_requirements'])
    
    # 경험과 모집요강 매칭
    matched_experience = match_experience_with_requirements(data['major_experience'], requirements)
    
    # 성격의 장단점 자동 생성
    auto_personality = generate_personality_traits(
        data['job_title'],
        requirements,
        data['company_type']
    )
    
    # 지원동기와 맺음말 자동 생성
    auto_motivation = generate_motivation(
        data['job_title'],
        data['major'],
        data['major_experience'],
        requirements,
        data['company_type']
    )
    
    auto_conclusion = generate_conclusion(
        data['job_title'],
        requirements,
        data['company_type']
    )
    
    # 사용자가 입력한 내용이 있으면 우선 사용
    personality = data['personality'] if data['personality'].strip() else auto_personality
    motivation = data['motivation'] if data['motivation'].strip() else auto_motivation
    conclusion = data['conclusion'] if data['conclusion'].strip() else auto_conclusion
    
    # 자기소개서 생성
    cover_letter = f"""지원자: {data['name']}
지원공고: {data['job_title']}
전공: {data['major']}

1. 자기소개
{enhance_introduction(data['introduction'], requirements, data['company_type'])}

2. 성격의 장단점
{personality}

3. 주요 경험
{matched_experience}

4. 지원동기
{motivation}

5. 맺음말
{conclusion}"""
    
    return cover_letter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    cover_letter = generate_cover_letter(data)
    return jsonify({'cover_letter': cover_letter})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False) 