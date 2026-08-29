import json
import math
import streamlit as st

st.set_page_config(
  page_title="Workstyle 16 — Technical Archetype Assessment",
  page_icon="◈",
  layout="wide",
  initial_sidebar_state="collapsed",
)

QUESTIONS = [
  {
    "q": "새 프로젝트를 맡았는데 요구사항이 아직 상당히 모호합니다. 가장 자연스러운 첫 행동은?",
    "a": [
      ("혼자 문서와 코드베이스를 훑으며 문제의 구조를 먼저 만든다.", {"EI": -2, "SN": -1}),
      ("관련 사람들과 짧게 이야기하며 무엇이 중요한 문제인지부터 잡는다.", {"EI": 2, "TF": 1}),
      ("작은 프로토타입을 바로 만들어 실제 반응을 본다.", {"JP": 2, "SN": 2}),
      ("성공 기준과 산출물을 먼저 명확히 정의한다.", {"JP": -2, "SN": -1}),
    ],
  },
  {
    "q": "분석 결과가 예상과 정반대로 나왔습니다. 당신이 가장 먼저 확인할 가능성이 높은 것은?",
    "a": [
      ("데이터 파이프라인과 구현 오류부터 의심한다.", {"SN": 2, "TF": 1}),
      ("기존 가정 자체가 틀렸을 가능성을 탐색한다.", {"SN": -2, "JP": 1}),
      ("동료에게 결과를 보여주고 다른 해석을 빠르게 모은다.", {"EI": 2, "TF": -1}),
      ("사전에 정한 분석 계획과 결과가 어떻게 어긋났는지 정리한다.", {"JP": -2}),
    ],
  },
  {
    "q": "코드 리뷰에서 가장 가치 있다고 느끼는 피드백은?",
    "a": [
      ("논리적 결함이나 숨은 edge case를 정확히 짚는 피드백", {"TF": 2, "SN": 1}),
      ("구조를 더 단순하고 확장 가능하게 만드는 피드백", {"SN": -2, "JP": -1}),
      ("실제 사용자가 겪을 불편을 알려주는 피드백", {"TF": -2, "SN": 1}),
      ("팀 컨벤션과 유지보수성을 높이는 구체적 제안", {"JP": -2, "TF": 1}),
    ],
  },
  {
    "q": "새로운 기술 스택을 배울 때 가장 편한 방식은?",
    "a": [
      ("공식 문서와 개념 모델을 먼저 충분히 이해한다.", {"EI": -1, "SN": -2}),
      ("작은 예제를 직접 깨뜨려가며 배운다.", {"SN": 2, "JP": 2}),
      ("경험 많은 사람의 설명과 추천 흐름을 먼저 듣는다.", {"EI": 2}),
      ("실제 프로젝트 문제에 바로 적용하면서 필요한 만큼 배운다.", {"JP": 2, "SN": 1}),
    ],
  },
  {
    "q": "연구 아이디어를 평가할 때 무엇이 가장 빨리 눈에 들어옵니까?",
    "a": [
      ("가설의 논리 구조와 반증 가능성", {"TF": 2, "SN": -1}),
      ("실제 임상적·현업적 중요성", {"TF": -2, "SN": 1}),
      ("기존 문헌과 연결되는 더 큰 그림", {"SN": -2}),
      ("실행 가능성과 데이터 가용성", {"SN": 2, "JP": -1}),
    ],
  },
  {
    "q": "회의 중 토론이 예상보다 훨씬 길어지고 있습니다.",
    "a": [
      ("논점이 충분히 정리될 때까지 토론을 이어가는 편이다.", {"EI": 1, "JP": 1}),
      ("결정해야 할 항목을 분리하고 결론을 내자고 제안한다.", {"JP": -2, "TF": 1}),
      ("회의 후 혼자 생각할 시간이 필요하다고 느낀다.", {"EI": -2}),
      ("사람들이 실제로 우려하는 지점을 먼저 파악한다.", {"TF": -2, "EI": 1}),
    ],
  },
  {
    "q": "복잡한 버그를 만났을 때 당신의 기본 전략은?",
    "a": [
      ("재현 조건을 최소화하고 하나씩 제거한다.", {"SN": 2, "TF": 2}),
      ("전체 시스템 구조에서 가능한 원인을 먼저 추론한다.", {"SN": -2, "TF": 1}),
      ("로그를 더 심고 빠르게 여러 가설을 시험한다.", {"JP": 2, "SN": 1}),
      ("비슷한 경험이 있는 동료와 함께 문제를 본다.", {"EI": 2}),
    ],
  },
  {
    "q": "장기 프로젝트의 로드맵을 만들 때 선호하는 방식은?",
    "a": [
      ("중요 milestone과 exit criteria를 미리 정한다.", {"JP": -2}),
      ("몇 개의 방향만 잡고 세부 경로는 열어둔다.", {"JP": 2}),
      ("기술적 의존성과 구조를 먼저 모델링한다.", {"SN": -2, "TF": 1}),
      ("팀원들의 역할과 협업 흐름을 먼저 맞춘다.", {"TF": -2, "EI": 1}),
    ],
  },
  {
    "q": "좋은 설명이라고 느끼는 것은?",
    "a": [
      ("핵심 원리를 압축해서 보여주는 설명", {"SN": -2}),
      ("구체적 예시와 실제 입력·출력을 보여주는 설명", {"SN": 2}),
      ("왜 이것이 사람에게 중요한지 연결해주는 설명", {"TF": -2}),
      ("정의, 전제, 단계가 명확히 정리된 설명", {"JP": -1, "TF": 1}),
    ],
  },
  {
    "q": "예상치 못한 흥미로운 결과가 나왔지만 원래 계획에는 없던 분석입니다.",
    "a": [
      ("즉시 추가 분석을 해보고 가능성을 넓힌다.", {"JP": 2, "SN": -1}),
      ("흥미롭지만 우선 preregistered 계획을 완결한다.", {"JP": -2}),
      ("새 결과의 실질적 의미부터 동료들과 논의한다.", {"EI": 2, "TF": -1}),
      ("원인을 설명할 수 있는 이론적 가설을 먼저 세운다.", {"SN": -2, "TF": 1}),
    ],
  },
  {
    "q": "팀에서 의견 충돌이 있을 때 가장 먼저 하는 것은?",
    "a": [
      ("각 주장에 어떤 증거가 있는지 분리한다.", {"TF": 2}),
      ("사람들이 무엇을 중요하게 생각하는지 이해하려 한다.", {"TF": -2}),
      ("쟁점을 문서로 정리해 비동기적으로 생각한다.", {"EI": -2, "JP": -1}),
      ("실험이나 프로토타입으로 빠르게 판별하자고 제안한다.", {"JP": 2, "SN": 2}),
    ],
  },
  {
    "q": "좋은 코드베이스의 가장 중요한 속성은?",
    "a": [
      ("명시적이고 예측 가능한 구조", {"JP": -2, "SN": 1}),
      ("새 요구에 유연하게 진화할 수 있는 구조", {"JP": 2, "SN": -1}),
      ("핵심 abstraction이 우아하게 잡혀 있는 구조", {"SN": -2}),
      ("팀원 누구나 쉽게 이해하고 수정할 수 있는 구조", {"TF": -1, "EI": 1}),
    ],
  },
  {
    "q": "논문이나 기술 문서를 읽을 때 보통 어디서 시작합니까?",
    "a": [
      ("초록과 결론으로 전체 주장부터 파악한다.", {"SN": -1, "JP": 1}),
      ("methods나 구현 세부를 먼저 본다.", {"SN": 2, "TF": 1}),
      ("그림과 결과를 보며 감을 잡는다.", {"SN": 1, "JP": 1}),
      ("처음부터 순서대로 읽으며 논리 전개를 따라간다.", {"JP": -1}),
    ],
  },
  {
    "q": "당신이 가장 몰입하기 쉬운 작업 환경은?",
    "a": [
      ("긴 시간 방해 없이 혼자 깊게 생각할 수 있는 환경", {"EI": -2}),
      ("주변 사람과 바로 질문하고 반응을 주고받을 수 있는 환경", {"EI": 2}),
      ("정해진 일정과 우선순위가 명확한 환경", {"JP": -2}),
      ("그날 가장 중요한 문제를 자유롭게 선택할 수 있는 환경", {"JP": 2}),
    ],
  },
  {
    "q": "모델 성능이 개선되었지만 설명 가능성은 낮아졌습니다.",
    "a": [
      ("목표 지표 개선이 충분하면 우선 수용할 수 있다.", {"TF": 2, "SN": 1}),
      ("왜 좋아졌는지 이해하기 전에는 쉽게 신뢰하지 않는다.", {"SN": -2, "TF": 1}),
      ("실사용자에게 미칠 영향을 먼저 검토한다.", {"TF": -2}),
      ("운영 리스크와 fallback 조건을 명확히 설정한다.", {"JP": -2, "TF": 1}),
    ],
  },
  {
    "q": "브레인스토밍에서 당신에게 더 자연스러운 역할은?",
    "a": [
      ("아이디어를 많이 던지며 가능성을 넓힌다.", {"EI": 1, "SN": -2, "JP": 2}),
      ("다른 사람의 아이디어 사이 구조와 연결을 찾는다.", {"SN": -2, "EI": -1}),
      ("실현 가능한 아이디어를 빠르게 골라낸다.", {"SN": 2, "TF": 2}),
      ("사람들이 말하지 않은 우려나 필요를 포착한다.", {"TF": -2}),
    ],
  },
  {
    "q": "마감이 한 달 남은 프로젝트에서 현재 진척은 60%입니다.",
    "a": [
      ("남은 일을 세분화하고 일정에 다시 배치한다.", {"JP": -2}),
      ("가장 불확실한 부분부터 집중적으로 해결한다.", {"SN": -1, "TF": 1}),
      ("범위를 줄이더라도 핵심 결과물을 완성한다.", {"TF": 2, "JP": -1}),
      ("진척을 보며 우선순위를 계속 조정한다.", {"JP": 2}),
    ],
  },
  {
    "q": "동료가 기술적으로는 덜 좋은 접근을 선호하지만 팀 전체에는 더 편한 방식이라고 주장합니다.",
    "a": [
      ("장기 기술 부채를 근거로 더 좋은 구조를 설득한다.", {"TF": 2, "SN": -1}),
      ("팀 전체 생산성이 실제로 높다면 받아들일 수 있다.", {"TF": -1, "SN": 1}),
      ("작은 실험으로 두 접근의 차이를 측정해본다.", {"SN": 2, "JP": 1}),
      ("갈등 비용까지 포함해 균형점을 찾는다.", {"TF": -2}),
    ],
  },
  {
    "q": "새 데이터셋을 처음 받았을 때 무엇부터 합니까?",
    "a": [
      ("schema, missingness, 분포를 빠르게 훑는다.", {"SN": 2, "JP": 1}),
      ("이 데이터로 어떤 질문까지 답할 수 있을지 상상한다.", {"SN": -2}),
      ("데이터 생성 과정과 provenance를 이해한다.", {"TF": 1, "SN": -1}),
      ("분석 목적과 필요한 변수 목록을 먼저 고정한다.", {"JP": -2}),
    ],
  },
  {
    "q": "전문가가 강하게 주장하지만 데이터는 애매합니다.",
    "a": [
      ("전문가 판단을 중요한 prior로 존중한다.", {"TF": -1, "SN": 1}),
      ("증거가 부족하면 판단을 유보한다.", {"TF": 2, "JP": 1}),
      ("왜 그런 직관이 생겼는지 구조를 이해하려 한다.", {"SN": -2}),
      ("추가로 어떤 데이터가 필요할지 구체화한다.", {"JP": -1, "SN": 2}),
    ],
  },
  {
    "q": "하루가 끝났을 때 가장 만족스러운 느낌은?",
    "a": [
      ("복잡했던 문제가 머릿속에서 깔끔한 구조로 정리되었다.", {"SN": -2, "EI": -1}),
      ("여러 사람과 협력해 막힌 일이 풀렸다.", {"EI": 2, "TF": -1}),
      ("명확한 결과물 하나를 완성했다.", {"JP": -2, "SN": 1}),
      ("예상하지 못한 새로운 방향을 발견했다.", {"JP": 2, "SN": -2}),
    ],
  },
  {
    "q": "좋은 연구 질문의 조건에 더 가까운 것은?",
    "a": [
      ("이론적으로 중요한 구조를 드러낸다.", {"SN": -2}),
      ("실제 의사결정을 바꿀 수 있다.", {"TF": -2, "SN": 1}),
      ("명확히 측정하고 검증할 수 있다.", {"SN": 2, "TF": 1}),
      ("후속 질문을 풍부하게 만들어낸다.", {"JP": 2, "SN": -1}),
    ],
  },
  {
    "q": "코드나 분석을 공유하기 직전, 마지막으로 가장 신경 쓰는 것은?",
    "a": [
      ("edge case와 실패 조건", {"TF": 2, "SN": 2}),
      ("API나 구조의 일관성", {"JP": -1, "SN": -1}),
      ("다른 사람이 읽고 이해할 수 있는가", {"TF": -1, "EI": 1}),
      ("다음 변경에도 쉽게 대응할 수 있는가", {"JP": 2}),
    ],
  },
  {
    "q": "새로운 협업자가 합류했습니다. 당신은 보통?",
    "a": [
      ("문서와 맥락을 정리해 스스로 따라올 수 있게 한다.", {"EI": -1, "JP": -1}),
      ("직접 대화하며 프로젝트의 큰 그림을 전달한다.", {"EI": 2, "SN": -1}),
      ("작은 실제 작업을 하나 맡겨 빠르게 적응하게 한다.", {"SN": 2, "JP": 1}),
      ("그 사람이 관심 있는 문제를 먼저 파악한다.", {"TF": -2, "EI": 1}),
    ],
  },
  {
    "q": "두 가지 구현 중 하나를 골라야 하는데 benchmark 차이는 거의 없습니다.",
    "a": [
      ("개념적으로 더 단순하고 우아한 쪽", {"SN": -2}),
      ("운영 중 예측 가능하고 안전한 쪽", {"JP": -2, "SN": 1}),
      ("팀이 이미 익숙한 쪽", {"TF": -1, "SN": 1}),
      ("나중에 방향을 바꾸기 쉬운 쪽", {"JP": 2}),
    ],
  },
  {
    "q": "계획에 없던 중요한 요청이 갑자기 들어왔습니다.",
    "a": [
      ("현재 계획의 우선순위를 다시 계산한다.", {"JP": -1, "TF": 1}),
      ("일단 요청의 중요성과 맥락을 사람들과 확인한다.", {"EI": 2, "TF": -1}),
      ("흥미롭다면 흐름을 바꿔 바로 파고들 수 있다.", {"JP": 2}),
      ("기존 약속을 지키는 것이 우선이다.", {"JP": -2}),
    ],
  },
  {
    "q": "설명을 들었는데 세부는 이해되지만 전체 그림이 잘 안 잡힙니다.",
    "a": [
      ("상위 수준의 구조나 비유를 요청한다.", {"SN": -2}),
      ("구체적인 예제를 하나 더 요청한다.", {"SN": 2}),
      ("직접 다시 정리해본 뒤 질문한다.", {"EI": -2}),
      ("상대와 대화를 이어가며 이해를 맞춘다.", {"EI": 2}),
    ],
  },
  {
    "q": "의사결정에서 가장 불편한 상황은?",
    "a": [
      ("논리적으로 일관되지 않은 결정", {"TF": 2}),
      ("사람에게 미치는 영향이 무시된 결정", {"TF": -2}),
      ("근거가 너무 추상적이고 실제 정보가 부족한 결정", {"SN": 2}),
      ("결론이 계속 미뤄지는 상황", {"JP": -2}),
    ],
  },
  {
    "q": "주말에 개인 기술 프로젝트를 한다면 어떤 흐름이 더 자연스럽습니까?",
    "a": [
      ("처음부터 만들고 싶은 구조를 설계한다.", {"SN": -1, "JP": -1}),
      ("재미있는 부분부터 바로 구현한다.", {"JP": 2, "SN": 1}),
      ("새 개념이나 언어를 탐구하는 계기로 삼는다.", {"SN": -2}),
      ("다른 사람에게 보여주거나 피드백 받을 수 있는 형태까지 만든다.", {"EI": 1, "TF": -1}),
    ],
  },
  {
    "q": "마지막 질문입니다. 일을 잘하고 있다는 느낌은 언제 가장 강합니까?",
    "a": [
      ("혼란스러운 문제에서 명확한 원리를 찾아냈을 때", {"SN": -2, "TF": 1}),
      ("팀이 함께 움직일 수 있는 방향을 만들었을 때", {"EI": 2, "TF": -1}),
      ("신뢰할 수 있는 결과물을 끝까지 완성했을 때", {"JP": -2, "SN": 1}),
      ("새로운 가능성을 열어두고 다음 실험으로 이어갈 때", {"JP": 2, "SN": -1}),
    ],
  },
]

TYPE_PROFILES = {
  "INTJ": ("Systems Architect", "복잡한 문제의 underlying structure를 먼저 찾고, 장기적으로 견고한 모델과 시스템을 설계하는 경향이 강합니다."),
  "INTP": ("Exploratory Theorist", "정답을 빠르게 고정하기보다 개념과 가설을 깊게 탐색하며, 문제를 더 정확하게 표현하는 데 강점이 있습니다."),
  "ENTJ": ("Technical Strategist", "기술적 복잡성을 빠르게 구조화하고, 사람과 자원을 정렬해 결과로 밀어붙이는 스타일에 가깝습니다."),
  "ENTP": ("Prototype Catalyst", "새로운 가능성을 빠르게 발견하고, 토론과 실험을 통해 아이디어를 움직이게 만드는 경향이 강합니다."),
  "INFJ": ("Insight Translator", "복잡한 시스템과 사람의 필요를 함께 읽으며, 큰 그림을 일관된 방향으로 번역하는 데 강점이 있습니다."),
  "INFP": ("Values Researcher", "독립적인 탐색과 깊은 의미를 중시하며, 기술적 선택이 사람과 목적에 어떻게 연결되는지 민감하게 봅니다."),
  "ENFJ": ("Collaborative Architect", "사람 사이의 이해를 정렬하면서도 장기적인 방향과 구조를 만들어가는 협업 중심형입니다."),
  "ENFP": ("Possibility Connector", "아이디어와 사람 사이의 연결을 빠르게 만들고, 새로운 프로젝트의 잠재력을 발견하는 데 강점이 있습니다."),
  "ISTJ": ("Reliability Engineer", "명확한 기준, 재현성, 운영 안정성을 중시하며 복잡한 일을 예측 가능한 시스템으로 바꾸는 데 강합니다."),
  "ISFJ": ("Steady Maintainer", "실제 사용 맥락과 팀의 필요를 세심하게 챙기며, 신뢰할 수 있는 작업 흐름을 유지하는 데 강점이 있습니다."),
  "ESTJ": ("Delivery Lead", "목표와 책임을 명확히 하고, 실행 가능한 계획으로 전환해 결과를 안정적으로 완성하는 데 강합니다."),
  "ESFJ": ("Team Integrator", "팀의 정보 흐름과 협업 상태를 빠르게 읽고, 사람들이 함께 움직일 수 있는 환경을 만드는 스타일입니다."),
  "ISTP": ("Pragmatic Debugger", "문제를 실제 작동 단위로 분해하고, 직접 실험하며 가장 효율적인 해결책을 찾는 데 강합니다."),
  "ISFP": ("Craft Specialist", "현실적인 감각과 개인적 기준을 바탕으로, 사용자와 맥락에 잘 맞는 세심한 결과물을 만드는 경향이 있습니다."),
  "ESTP": ("Rapid Operator", "실제 상황에서 빠르게 반응하고, 실험과 행동을 통해 불확실성을 줄이는 데 강한 스타일입니다."),
  "ESFP": ("Human-Centered Builder", "사람의 반응과 실제 사용성을 빠르게 읽고, 즉각적인 피드백 속에서 결과물을 발전시키는 데 강합니다."),
}

AXES = [
  ("EI", "I", "E", "내향적 집중", "외향적 상호작용"),
  ("SN", "N", "S", "추상·패턴", "구체·관찰"),
  ("TF", "F", "T", "사람·가치", "논리·기준"),
  ("JP", "J", "P", "구조·확정", "유연·탐색"),
]

CSS = """
<style>
  /* Reset and base styles - hide ONLY Streamlit internal chrome */
  #MainMenu { display: none !important; }
  [data-testid="stHeader"] { display: none !important; }
  [data-testid="stToolbar"] { display: none !important; }
  [data-testid="stDecoration"] { display: none !important; }
  [data-testid="stStatusWidget"] { display: none !important; }

  :root {
    --bg: #0b0d10;
    --panel: rgba(22, 25, 31, 0.78);
    --panel-2: rgba(28, 32, 39, 0.92);
    --text: #f3f4f6;
    --muted: #9aa3b2;
    --line: rgba(255, 255, 255, 0.09);
    --accent: #8ea2ff;
    --accent-2: #66d9c6;
    --danger: #ff8e8e;
    --shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
    --radius: 24px;
  }

  html { scroll-behavior: smooth; }

  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 15% 10%, rgba(91, 113, 255, 0.16), transparent 28%),
      radial-gradient(circle at 88% 18%, rgba(70, 208, 188, 0.12), transparent 26%),
      linear-gradient(180deg, #0b0d10 0%, #0f1218 100%) !important;
    color: #f3f4f6 !important;
    font-family: Inter, Pretendard, "Noto Sans KR", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    letter-spacing: -0.02em;
    min-height: 100vh;
  }

  [data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.035;
    background-image:
      radial-gradient(circle at 20% 20%, #fff 0 1px, transparent 1px),
      radial-gradient(circle at 80% 40%, #fff 0 1px, transparent 1px);
    background-size: 18px 18px, 22px 22px;
    z-index: 0;
  }

  .block-container {
    max-width: 1120px !important;
    padding-top: 28px !important;
    padding-bottom: 64px !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    position: relative;
    z-index: 1;
  }

  /* Topbar header */
  .topbar {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 16px !important;
    margin-bottom: 36px !important;
    width: 100% !important;
    visibility: visible !important;
  }

  .brand {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    color: #f3f4f6 !important;
  }

  .brand-mark {
    width: 34px !important;
    height: 34px !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 10px !important;
    display: grid !important;
    place-items: center !important;
    background: linear-gradient(145deg, rgba(142, 162, 255, 0.18), rgba(102, 217, 198, 0.12)) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    position: relative !important;
  }

  .brand-mark::before {
    content: "" !important;
    width: 14px !important;
    height: 14px !important;
    border-radius: 4px !important;
    border: 2px solid #8ea2ff !important;
    transform: rotate(45deg) !important;
    display: block !important;
  }

  .pill {
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    background: rgba(255, 255, 255, 0.035) !important;
    color: #9aa3b2 !important;
    border-radius: 999px !important;
    padding: 8px 14px !important;
    font-size: 13px !important;
    display: inline-block !important;
  }

  /* Intro Section */
  .st-key-hero_left_container {
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    background: rgba(22, 25, 31, 0.78) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 24px !important;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35) !important;
    padding: 44px !important;
    min-height: 480px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
  }

  .eyebrow {
    color: #66d9c6;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 800;
    margin-bottom: 16px;
  }

  .hero-title {
    font-size: clamp(38px, 6vw, 76px);
    line-height: 0.95;
    letter-spacing: -0.055em;
    margin: 0 0 22px;
    font-weight: 800;
    color: #f3f4f6;
  }

  .hero-copy {
    color: #9aa3b2;
    font-size: clamp(15px, 1.8vw, 19px);
    line-height: 1.65;
    margin: 0 0 28px 0;
  }

  .hero-card-right {
    border: 1px solid rgba(255, 255, 255, 0.09);
    background: rgba(22, 25, 31, 0.78);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
    padding: 28px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 480px;
  }

  .hero-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 20px;
  }

  .stat {
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 16px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.025);
  }

  .stat strong {
    display: block;
    font-size: 22px;
    font-weight: 700;
    color: #f3f4f6;
    margin-bottom: 5px;
  }

  .stat span {
    color: #9aa3b2;
    font-size: 12px;
  }

  .matrix {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    align-content: end;
  }

  .matrix div {
    aspect-ratio: 1;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.09);
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.055), rgba(255, 255, 255, 0.02));
    display: flex;
    align-items: flex-end;
    padding: 12px;
    color: #d9def7;
    font-size: 12px;
    font-weight: 700;
    transition: 0.25s ease;
  }

  .matrix div:hover {
    transform: translateY(-3px) rotate(-1deg);
    border-color: rgba(142, 162, 255, 0.35);
  }

  .philosophy {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 24px;
    margin-bottom: 28px;
  }

  .mini-card {
    border: 1px solid rgba(255, 255, 255, 0.09);
    background: rgba(22, 25, 31, 0.78);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 22px;
  }

  .mini-card h3 {
    margin: 0 0 8px;
    font-size: 16px;
    font-weight: 700;
    color: #f3f4f6;
  }

  .mini-card p {
    margin: 0;
    color: #9aa3b2;
    line-height: 1.55;
    font-size: 14px;
  }

  /* Button styling matching HTML */
  .st-key-start_btn button {
    border: none !important;
    color: #0b0d10 !important;
    background: linear-gradient(135deg, #8ea2ff, #bac5ff) !important;
    border-radius: 14px !important;
    padding: 13px 24px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    transition: 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(142, 162, 255, 0.2) !important;
    width: auto !important;
  }

  .st-key-start_btn button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(142, 162, 255, 0.35) !important;
  }

  .btn-anchor {
    border: 1px solid rgba(255, 255, 255, 0.09);
    background: rgba(255, 255, 255, 0.04);
    color: #f3f4f6;
    border-radius: 14px;
    padding: 13px 20px;
    font-weight: 700;
    font-size: 15px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: 0.2s ease;
    cursor: pointer;
    box-sizing: border-box;
  }

  .btn-anchor:hover {
    transform: translateY(-1px);
    background: rgba(255, 255, 255, 0.07);
    color: #f3f4f6;
  }

  /* Quiz Section */
  .quiz-sidebar {
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 20px;
    background: rgba(18, 21, 26, 0.78);
    padding: 20px;
    position: sticky;
    top: 24px;
  }

  .quiz-sidebar small {
    color: #9aa3b2;
    font-size: 13px;
    line-height: 1.5;
    display: block;
  }

  .quiz-sidebar strong {
    font-size: 28px;
    font-weight: 700;
    color: #f3f4f6;
    display: block;
    margin: 4px 0 12px;
  }

  .progress-track {
    height: 8px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 99px;
    overflow: hidden;
    margin: 12px 0 18px;
  }

  .progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #8ea2ff, #66d9c6);
    border-radius: 99px;
    transition: width 0.25s ease;
  }

  .st-key-quiz_card_container {
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    background: rgba(22, 25, 31, 0.78) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 24px !important;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35) !important;
    padding: clamp(24px, 4.5vw, 46px) !important;
    min-height: 520px !important;
  }

  .q-number {
    color: #66d9c6;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 18px;
  }

  .question-text {
    font-size: clamp(24px, 3.6vw, 36px);
    line-height: 1.3;
    letter-spacing: -0.035em;
    margin: 0 0 26px;
    font-weight: 700;
    color: #f3f4f6;
  }

  /* Answer Buttons in Quiz */
  .st-key-quiz_card_container div[data-testid="stButton"] {
    margin-bottom: 12px !important;
  }

  .st-key-quiz_card_container div[data-testid="stButton"] > button {
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    background: rgba(255, 255, 255, 0.025) !important;
    color: #f3f4f6 !important;
    padding: 18px 20px !important;
    border-radius: 16px !important;
    line-height: 1.5 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    white-space: normal !important;
    min-height: unset !important;
    transition: 0.18s ease !important;
  }

  .st-key-quiz_card_container div[data-testid="stButton"] > button:hover {
    border-color: rgba(142, 162, 255, 0.42) !important;
    background: rgba(142, 162, 255, 0.07) !important;
    transform: translateX(3px) !important;
    color: #f3f4f6 !important;
  }

  .st-key-prev_btn button {
    width: auto !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    background: rgba(255, 255, 255, 0.04) !important;
    color: #f3f4f6 !important;
    border-radius: 14px !important;
    padding: 11px 22px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    transition: 0.2s ease !important;
    margin-top: 16px !important;
  }

  .st-key-prev_btn button:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    transform: translateY(-1px) !important;
  }

  .st-key-prev_btn button:disabled {
    opacity: 0.35 !important;
    cursor: default !important;
    transform: none !important;
  }

  /* Result Screen */
  .st-key-result_card_container {
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    background: rgba(22, 25, 31, 0.78) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 24px !important;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35) !important;
    padding: clamp(28px, 5vw, 54px) !important;
  }

  .result-head {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 24px;
    align-items: start;
    margin-bottom: 36px;
  }

  .type-code {
    font-size: clamp(56px, 10vw, 108px);
    line-height: 0.9;
    letter-spacing: -0.07em;
    font-weight: 800;
    margin: 10px 0 12px;
    color: #f3f4f6;
  }

  .type-name {
    color: #66d9c6;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 12px;
  }

  .type-summary {
    max-width: 760px;
    color: #9aa3b2;
    line-height: 1.7;
    font-size: 16px;
    margin: 0;
  }

  .distance-badge {
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 18px;
    padding: 16px;
    min-width: 160px;
    background: rgba(255, 255, 255, 0.025);
    text-align: center;
  }

  .distance-badge span {
    color: #9aa3b2;
    font-size: 12px;
    display: block;
  }

  .distance-badge strong {
    display: block;
    font-size: 28px;
    font-weight: 700;
    margin-top: 4px;
    color: #f3f4f6;
  }

  .axes {
    display: grid;
    gap: 18px;
    margin: 36px 0;
  }

  .axis-row {
    display: grid;
    grid-template-columns: 120px 1fr 120px;
    gap: 16px;
    align-items: center;
  }

  .axis-label {
    font-weight: 800;
    font-size: 14px;
    color: #f3f4f6;
    line-height: 1.3;
  }

  .axis-label small {
    color: #9aa3b2;
    font-weight: 500;
    font-size: 12px;
    display: block;
  }

  .axis-label.right {
    text-align: right;
    color: #9aa3b2;
  }

  .axis-track {
    position: relative;
    height: 10px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 99px;
  }

  .axis-mid {
    position: absolute;
    left: 50%;
    top: -4px;
    bottom: -4px;
    width: 1px;
    background: rgba(255, 255, 255, 0.2);
  }

  .axis-dot {
    position: absolute;
    top: 50%;
    width: 18px;
    height: 18px;
    margin-top: -9px;
    margin-left: -9px;
    border-radius: 50%;
    background: #f3f4f6;
    border: 4px solid #8ea2ff;
    box-shadow: 0 0 0 6px rgba(142, 162, 255, 0.09);
    transition: left 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
  }

  .alternatives {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 14px;
  }

  .alt {
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 18px;
    padding: 18px;
    background: rgba(255, 255, 255, 0.025);
  }

  .alt strong {
    font-size: 24px;
    font-weight: 700;
    display: block;
    margin-bottom: 5px;
    color: #f3f4f6;
  }

  .alt span {
    color: #9aa3b2;
    font-size: 13px;
  }

  .fineprint {
    color: #737c8b;
    font-size: 12px;
    line-height: 1.6;
    margin-top: 28px;
    margin-bottom: 24px;
  }

  .st-key-restart_btn button {
    border: none !important;
    color: #0b0d10 !important;
    background: linear-gradient(135deg, #8ea2ff, #bac5ff) !important;
    border-radius: 14px !important;
    padding: 13px 24px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    transition: 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(142, 162, 255, 0.2) !important;
    width: auto !important;
  }

  .st-key-restart_btn button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(142, 162, 255, 0.35) !important;
  }

  .footer {
    text-align: center;
    color: #66707f;
    font-size: 12px;
    padding-top: 34px;
  }

  /* Responsive layout adjustments */
  @media (max-width: 860px) {
    .st-key-hero_left_container { min-height: 420px; padding: 34px !important; }
    .philosophy { grid-template-columns: 1fr; }
    .result-head { grid-template-columns: 1fr; }
    .alternatives { grid-template-columns: 1fr; }
    .axis-row { grid-template-columns: 58px 1fr 58px; gap: 8px; }
    .hero-stats { grid-template-columns: 1fr; }
    .quiz-sidebar { position: static; margin-bottom: 18px; }
  }

  @media (max-width: 520px) {
    .block-container { padding-left: 10px !important; padding-right: 10px !important; padding-top: 12px !important; }
    .topbar { margin-bottom: 20px; }
    .st-key-hero_left_container { padding: 24px !important; border-radius: 18px !important; }
    .hero-card-right { padding: 20px; border-radius: 18px; }
    .st-key-quiz_card_container { padding: 20px !important; border-radius: 18px !important; }
    .st-key-result_card_container { padding: 20px !important; border-radius: 18px !important; }
    .matrix { grid-template-columns: repeat(4, 1fr); gap: 6px; }
    .matrix div { border-radius: 12px; padding: 7px; font-size: 10px; }
  }
</style>
"""


def init_state():
  defaults = {
    "screen": "intro",
    "current": 0,
    "responses": [None] * len(QUESTIONS),
  }
  for key, value in defaults.items():
    if key not in st.session_state:
      st.session_state[key] = value


def reset_test():
  st.session_state.screen = "quiz"
  st.session_state.current = 0
  st.session_state.responses = [None] * len(QUESTIONS)


def answer_question(index):
  current = st.session_state.current
  st.session_state.responses[current] = index

  if current < len(QUESTIONS) - 1:
    st.session_state.current += 1
  else:
    st.session_state.screen = "result"


def go_previous():
  if st.session_state.current > 0:
    st.session_state.current -= 1


def compute_scores():
  raw = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}

  for question, selected_index in zip(QUESTIONS, st.session_state.responses):
    if selected_index is None:
      continue
    selected = question["a"][selected_index][1]
    for axis, value in selected.items():
      raw[axis] += value

  normalized = {}
  for axis in raw:
    theoretical = 0
    for question in QUESTIONS:
      theoretical += max(abs(answer[1].get(axis, 0)) for answer in question["a"])

    normalized[axis] = (
      max(-1, min(1, raw[axis] / theoretical * 2.2))
      if theoretical
      else 0
    )

  return normalized


def vector_for_type(type_code):
  return {
    "EI": 1 if type_code[0] == "E" else -1,
    "SN": 1 if type_code[1] == "S" else -1,
    "TF": 1 if type_code[2] == "T" else -1,
    "JP": 1 if type_code[3] == "P" else -1,
  }


def type_distance(scores, type_code):
  vector = vector_for_type(type_code)
  return math.sqrt(
    sum((scores[axis] - vector[axis]) ** 2 for axis in scores)
  )


def rank_types(scores):
  ranked = [
    (type_code, type_distance(scores, type_code))
    for type_code in TYPE_PROFILES
  ]
  return sorted(ranked, key=lambda item: item[1])


def render_topbar():
  st.html(
    """
    <div class="topbar">
      <div class="brand">
        <div class="brand-mark"></div>
        <span>Workstyle 16</span>
      </div>
      <div class="pill">MBTI-inspired · Technical Workstyle</div>
    </div>
    """
  )


def render_intro():
  col1, col2 = st.columns([1.15, 0.85], gap="large")

  with col1:
    with st.container(key="hero_left_container"):
      st.html(
        """
        <div>
          <div class="eyebrow">For engineers & scientists</div>
          <h1 class="hero-title">30 scenes.<br>One closest pattern.</h1>
          <p class="hero-copy">
            일반적인 성격 질문 대신, 연구와 엔지니어링의 실제 의사결정 장면에서
            당신의 작업 스타일을 관찰합니다. 정밀한 심리측정보다는 16개의 워크스타일
            프로토타입 중 어디에 가장 가까운지 빠르게 탐색하는 테스트입니다.
          </p>
        </div>
        """
      )

      btn_left, btn_right, _ = st.columns([1.1, 1.2, 1.0])
      with btn_left:
        if st.button("테스트 시작", key="start_btn"):
          reset_test()
          st.rerun()
      with btn_right:
        st.html(
          '<a href="#principles" class="btn-anchor">설계 원칙 보기</a>'
        )

  with col2:
    st.html(
      """
      <aside class="hero-card-right">
        <div class="hero-stats">
          <div class="stat"><strong>30</strong><span>고밀도 상황형 문항</span></div>
          <div class="stat"><strong>4</strong><span>연속적 성향 축</span></div>
          <div class="stat"><strong>16</strong><span>기술 작업 아키타입</span></div>
        </div>
        <div class="matrix" aria-label="16 archetypes">
          <div>INTJ</div><div>INTP</div><div>ENTJ</div><div>ENTP</div>
          <div>INFJ</div><div>INFP</div><div>ENFJ</div><div>ENFP</div>
          <div>ISTJ</div><div>ISFJ</div><div>ESTJ</div><div>ESFJ</div>
          <div>ISTP</div><div>ISFP</div><div>ESTP</div><div>ESFP</div>
        </div>
      </aside>
      """
    )

  st.html(
    """
    <section class="philosophy" id="principles">
      <article class="mini-card">
        <h3>01 · 정보 밀도</h3>
        <p>비슷한 질문을 반복하지 않습니다. 각 문항은 서로 다른 작업 장면을 통해 새로운 신호를 추가합니다.</p>
      </article>
      <article class="mini-card">
        <h3>02 · 상황 기반</h3>
        <p>추상적인 자기평가 대신 코드 리뷰, 연구 설계, 디버깅, 협업, 불확실성 같은 구체적 상황을 묻습니다.</p>
      </article>
      <article class="mini-card">
        <h3>03 · 근접 패턴</h3>
        <p>가짜 정밀도를 피합니다. 하나의 타입을 단정하기보다 가장 가까운 패턴과 인접 후보를 함께 보여줍니다.</p>
      </article>
    </section>
    """
  )


def render_quiz():
  current = st.session_state.current
  question = QUESTIONS[current]
  progress_pct = ((current + 1) / len(QUESTIONS)) * 100

  left, right = st.columns([1, 2.7], gap="large")

  with left:
    st.html(
      f"""
      <aside class="quiz-sidebar">
        <small>진행률</small>
        <strong>{current + 1} / {len(QUESTIONS)}</strong>
        <div class="progress-track">
          <div class="progress-bar-fill" style="width: {progress_pct:.1f}%;"></div>
        </div>
        <small>
          가장 “이상적인 나”가 아니라, 실제로 비슷한 상황에서 반복적으로 보이는 행동에 가까운 답을 선택하세요.
        </small>
      </aside>
      """
    )

  with right:
    # Selected button highlighting if navigating back
    selected_idx = st.session_state.responses[current]
    if selected_idx is not None:
      st.html(
        f"""
        <style>
          .st-key-q_{current}_a_{selected_idx} button {{
            border-color: #8ea2ff !important;
            background: rgba(142, 162, 255, 0.14) !important;
          }}
        </style>
        """
      )

    with st.container(key="quiz_card_container"):
      st.html(
        f"""
        <div class="q-number">Question {current + 1:02d}</div>
        <h2 class="question-text">{question["q"]}</h2>
        """
      )

      for index, (label, _) in enumerate(question["a"]):
        if st.button(label, key=f"q_{current}_a_{index}"):
          answer_question(index)
          st.rerun()

      if st.button("이전", key="prev_btn", disabled=(current == 0)):
        go_previous()
        st.rerun()


def render_result():
  scores = compute_scores()
  ranked = rank_types(scores)
  best_type, best_distance = ranked[0]
  name, summary = TYPE_PROFILES[best_type]

  fit = max(0, min(99, round((1 - best_distance / 4) * 100)))

  alt_cards_html = "".join([
    f'<div class="alt"><strong>{alt_type}</strong><span>{TYPE_PROFILES[alt_type][0]} · #{rank_idx} nearest</span></div>'
    for rank_idx, (alt_type, _) in enumerate(ranked[1:4], start=2)
  ])

  axes_html = "".join([
    f"""
    <div class="axis-row">
      <div class="axis-label">{left_letter}<small>{left_desc}</small></div>
      <div class="axis-track">
        <div class="axis-mid"></div>
        <div class="axis-dot" style="left: {((scores[axis] + 1) / 2) * 100:.1f}%;"></div>
      </div>
      <div class="axis-label right"><span class="axis-letter">{right_letter}</span><small>{right_desc}</small></div>
    </div>
    """
    for axis, left_letter, right_letter, left_desc, right_desc in AXES
  ])

  alt_types_str = ", ".join(type_code for type_code, _ in ranked[1:4])
  share_text_raw = (
    f"Workstyle 16 결과: {best_type} — {name}\n"
    f"근접 타입: {alt_types_str}\n"
    f"Prototype fit: {fit}%"
  )
  js_share_text = json.dumps(share_text_raw)

  with st.container(key="result_card_container"):
    st.html(
      f"""
      <div class="result-head">
        <div>
          <div class="eyebrow">Closest workstyle pattern</div>
          <div class="type-code">{best_type}</div>
          <div class="type-name">{name}</div>
          <p class="type-summary">{summary}</p>
        </div>
        <div class="distance-badge">
          <span>prototype fit</span>
          <strong>{fit}%</strong>
        </div>
      </div>

      <div class="axes">
        {axes_html}
      </div>

      <div>
        <div class="eyebrow">Nearest alternatives</div>
        <div class="alternatives">
          {alt_cards_html}
        </div>
      </div>

      <p class="fineprint">
        이 테스트는 공식 MBTI® 검사나 임상적 성격 검사가 아닙니다. 결과는 기술·연구 환경에서의 작업 스타일을
        탐색하기 위한 프로토타입이며, 상황과 역할에 따라 다르게 나타날 수 있습니다.
      </p>
      """
    )

    action_col1, action_col2, _ = st.columns([1.1, 1.3, 2.0])
    with action_col1:
      if st.button("다시 테스트", key="restart_btn"):
        reset_test()
        st.rerun()

    with action_col2:
      st.html(
        f"""
        <button class="btn-anchor" id="copyResultBtn" onclick='
          navigator.clipboard.writeText({js_share_text});
          this.textContent = "복사됨";
          setTimeout(() => this.textContent = "결과 복사", 1400);
        '>결과 복사</button>
        """,
        unsafe_allow_javascript=True,
      )


def main():
  init_state()
  st.html(CSS)
  render_topbar()

  if st.session_state.screen == "intro":
    render_intro()
  elif st.session_state.screen == "quiz":
    render_quiz()
  else:
    render_result()

  st.html(
    '<div class="footer">Workstyle 16 · Technical Archetype Assessment</div>'
  )


if __name__ == "__main__":
  main()

