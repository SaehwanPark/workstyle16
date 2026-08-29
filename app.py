import math
import streamlit as st

st.set_page_config(
  page_title="Workstyle 16",
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
  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 12% 8%, rgba(91,113,255,.15), transparent 26%),
      radial-gradient(circle at 88% 18%, rgba(70,208,188,.10), transparent 24%),
      linear-gradient(180deg, #0b0d10 0%, #10131a 100%);
    color: #f3f4f6;
  }

  [data-testid="stHeader"] { background: transparent; }
  [data-testid="stToolbar"] { right: 1rem; }
  .block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 4rem;
  }

  h1, h2, h3, p, div { letter-spacing: -0.02em; }

  .brand {
    display: flex;
    align-items: center;
    gap: .65rem;
    font-weight: 750;
    margin-bottom: 2.5rem;
  }

  .brand-mark {
    width: 32px;
    height: 32px;
    display: inline-grid;
    place-items: center;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,.10);
    background: linear-gradient(145deg, rgba(142,162,255,.18), rgba(102,217,198,.12));
  }

  .brand-mark span {
    width: 11px;
    height: 11px;
    border: 2px solid #8ea2ff;
    transform: rotate(45deg);
    border-radius: 3px;
  }

  .pill {
    display: inline-block;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.035);
    color: #9aa3b2;
    border-radius: 999px;
    padding: .42rem .7rem;
    font-size: .78rem;
    margin-bottom: 1.25rem;
  }

  .eyebrow {
    color: #66d9c6;
    text-transform: uppercase;
    letter-spacing: .12em;
    font-size: .76rem;
    font-weight: 800;
    margin-bottom: .8rem;
  }

  .hero-title {
    font-size: clamp(3.2rem, 7vw, 6.4rem);
    line-height: .92;
    letter-spacing: -.06em;
    font-weight: 820;
    margin: 0 0 1.5rem 0;
  }

  .hero-copy {
    color: #9aa3b2;
    font-size: 1.05rem;
    line-height: 1.75;
    max-width: 720px;
    margin-bottom: 1.75rem;
  }

  .glass {
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(22,25,31,.74);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 24px 80px rgba(0,0,0,.32);
  }

  .mini-card {
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.026);
    border-radius: 18px;
    padding: 1.2rem;
    height: 100%;
  }

  .mini-card strong {
    display: block;
    margin-bottom: .45rem;
  }

  .mini-card span {
    color: #9aa3b2;
    font-size: .9rem;
    line-height: 1.55;
  }

  .progress-meta {
    color: #9aa3b2;
    font-size: .86rem;
    margin-bottom: .35rem;
  }

  .progress-count {
    font-size: 1.8rem;
    font-weight: 760;
    margin-bottom: .45rem;
  }

  .question-number {
    color: #66d9c6;
    font-weight: 800;
    letter-spacing: .08em;
    font-size: .78rem;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }

  .question-text {
    font-size: clamp(1.65rem, 3vw, 2.55rem);
    line-height: 1.32;
    letter-spacing: -.04em;
    font-weight: 750;
    margin-bottom: 1.4rem;
  }

  div.stButton > button {
    width: 100%;
    text-align: left;
    justify-content: flex-start;
    white-space: normal;
    border-radius: 15px;
    min-height: 3.5rem;
    padding: .85rem 1rem;
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.028);
    color: #f3f4f6;
    transition: all .16s ease;
  }

  div.stButton > button:hover {
    border-color: rgba(142,162,255,.5);
    background: rgba(142,162,255,.08);
    transform: translateX(2px);
    color: #f3f4f6;
  }

  div.stButton > button:focus:not(:active) {
    border-color: rgba(142,162,255,.5);
    color: #f3f4f6;
  }

  .type-code {
    font-size: clamp(4.6rem, 10vw, 8rem);
    line-height: .88;
    letter-spacing: -.07em;
    font-weight: 820;
    margin: .35rem 0 .8rem;
  }

  .type-name {
    color: #66d9c6;
    font-size: 1.15rem;
    font-weight: 800;
    margin-bottom: 1.2rem;
  }

  .summary {
    color: #9aa3b2;
    line-height: 1.75;
    font-size: 1rem;
    max-width: 760px;
  }

  .fit-box {
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.026);
    border-radius: 18px;
    padding: 1rem 1.15rem;
    text-align: center;
  }

  .fit-box span {
    color: #9aa3b2;
    font-size: .75rem;
  }

  .fit-box strong {
    display: block;
    font-size: 2rem;
    margin-top: .2rem;
  }

  .axis-labels {
    display:flex;
    justify-content:space-between;
    font-size:.82rem;
    color:#9aa3b2;
    margin-bottom:.35rem;
  }

  .axis-title {
    font-weight: 760;
    color: #f3f4f6;
  }

  .axis-track {
    position: relative;
    height: 10px;
    border-radius: 999px;
    background: rgba(255,255,255,.07);
    margin-bottom: 1.35rem;
  }

  .axis-track::after {
    content: "";
    position: absolute;
    left: 50%;
    top: -3px;
    bottom: -3px;
    width: 1px;
    background: rgba(255,255,255,.18);
  }

  .axis-dot {
    position:absolute;
    top:50%;
    width:18px;
    height:18px;
    margin-left:-9px;
    margin-top:-9px;
    border-radius:50%;
    background:#f3f4f6;
    border:4px solid #8ea2ff;
    box-shadow:0 0 0 6px rgba(142,162,255,.08);
    z-index:2;
  }

  .alt-card {
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.026);
    border-radius: 16px;
    padding: 1rem;
    height: 100%;
  }

  .alt-card strong {
    font-size: 1.55rem;
    display:block;
    margin-bottom:.25rem;
  }

  .alt-card span {
    color:#9aa3b2;
    font-size:.82rem;
  }

  .fineprint {
    color:#707987;
    font-size:.78rem;
    line-height:1.6;
    margin-top:1.5rem;
  }

  .footer {
    text-align:center;
    color:#626b78;
    font-size:.76rem;
    padding-top:2rem;
  }

  [data-testid="stProgress"] > div > div {
    background-image: linear-gradient(90deg, #8ea2ff, #66d9c6);
  }

  @media (max-width: 700px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .glass { padding: 1.3rem; border-radius: 18px; }
    .hero-title { font-size: 3.7rem; }
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


def render_brand():
  st.markdown(
    """
    <div class="brand">
      <div class="brand-mark"><span></span></div>
      <div>Workstyle 16</div>
    </div>
    """,
    unsafe_allow_html=True,
  )


def render_intro():
  st.markdown(
    '<div class="pill">MBTI-inspired · Technical Workstyle</div>',
    unsafe_allow_html=True,
  )
  st.markdown(
    """
    <div class="eyebrow">For engineers & scientists</div>
    <div class="hero-title">30 scenes.<br>One closest pattern.</div>
    <div class="hero-copy">
      일반적인 성격 질문 대신, 연구와 엔지니어링의 실제 의사결정 장면에서
      당신의 작업 스타일을 관찰합니다. 정밀한 심리측정보다는 16개의 워크스타일
      프로토타입 중 어디에 가장 가까운지 빠르게 탐색하는 테스트입니다.
    </div>
    """,
    unsafe_allow_html=True,
  )

  if st.button("테스트 시작 →", type="primary", use_container_width=False):
    reset_test()
    st.rerun()

  st.write("")
  c1, c2, c3 = st.columns(3)
  cards = [
    ("01 · 정보 밀도", "비슷한 질문을 반복하지 않습니다. 각 문항은 서로 다른 작업 장면에서 새로운 신호를 추가합니다."),
    ("02 · 상황 기반", "코드 리뷰, 연구 설계, 디버깅, 협업, 불확실성처럼 구체적인 기술·연구 상황을 묻습니다."),
    ("03 · 근접 패턴", "하나의 타입을 단정하기보다 가장 가까운 패턴과 인접 후보를 함께 보여줍니다."),
  ]
  for col, (title, body) in zip((c1, c2, c3), cards):
    with col:
      st.markdown(
        f'<div class="mini-card"><strong>{title}</strong><span>{body}</span></div>',
        unsafe_allow_html=True,
      )


def render_quiz():
  current = st.session_state.current
  question = QUESTIONS[current]

  left, right = st.columns([1, 3.1], gap="large")

  with left:
    st.markdown(
      f"""
      <div class="progress-meta">진행률</div>
      <div class="progress-count">{current + 1} / {len(QUESTIONS)}</div>
      """,
      unsafe_allow_html=True,
    )
    st.progress((current + 1) / len(QUESTIONS))
    st.caption(
      '가장 "이상적인 나"가 아니라, 비슷한 상황에서 실제로 반복되는 행동에 가까운 답을 선택하세요.'
    )

    if current > 0:
      if st.button("← 이전 문항", key="previous", use_container_width=True):
        go_previous()
        st.rerun()

  with right:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown(
      f'<div class="question-number">Question {current + 1:02d}</div>',
      unsafe_allow_html=True,
    )
    st.markdown(
      f'<div class="question-text">{question["q"]}</div>',
      unsafe_allow_html=True,
    )

    for index, (label, _) in enumerate(question["a"]):
      if st.button(
        label,
        key=f"q{current}_a{index}",
        use_container_width=True,
      ):
        answer_question(index)
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def render_axis(axis, left_letter, right_letter, left_desc, right_desc, score):
  position = (score + 1) / 2 * 100
  st.markdown(
    f"""
    <div class="axis-labels">
      <div><span class="axis-title">{left_letter}</span> · {left_desc}</div>
      <div>{right_desc} · <span class="axis-title">{right_letter}</span></div>
    </div>
    <div class="axis-track">
      <div class="axis-dot" style="left:{position:.1f}%"></div>
    </div>
    """,
    unsafe_allow_html=True,
  )


def render_result():
  scores = compute_scores()
  ranked = rank_types(scores)
  best_type, best_distance = ranked[0]
  name, summary = TYPE_PROFILES[best_type]

  fit = max(0, min(99, round((1 - best_distance / 4) * 100)))

  st.markdown('<div class="glass">', unsafe_allow_html=True)

  top_left, top_right = st.columns([4, 1], gap="large")
  with top_left:
    st.markdown('<div class="eyebrow">Closest workstyle pattern</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="type-code">{best_type}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="type-name">{name}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary">{summary}</div>', unsafe_allow_html=True)

  with top_right:
    st.markdown(
      f'<div class="fit-box"><span>prototype fit</span><strong>{fit}%</strong></div>',
      unsafe_allow_html=True,
    )

  st.write("")
  st.write("")

  for axis, left_letter, right_letter, left_desc, right_desc in AXES:
    render_axis(
      axis,
      left_letter,
      right_letter,
      left_desc,
      right_desc,
      scores[axis],
    )

  st.write("")
  st.markdown('<div class="eyebrow">Nearest alternatives</div>', unsafe_allow_html=True)

  cols = st.columns(3)
  for rank, (col, (type_code, _)) in enumerate(zip(cols, ranked[1:4]), start=2):
    alt_name, _ = TYPE_PROFILES[type_code]
    with col:
      st.markdown(
        f"""
        <div class="alt-card">
          <strong>{type_code}</strong>
          <span>{alt_name} · #{rank} nearest</span>
        </div>
        """,
        unsafe_allow_html=True,
      )

  st.markdown(
    """
    <div class="fineprint">
      이 테스트는 공식 MBTI® 검사나 임상적 성격 검사가 아닙니다.
      결과는 기술·연구 환경에서의 작업 스타일을 탐색하기 위한 프로토타입이며,
      상황과 역할에 따라 다르게 나타날 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
  )

  st.write("")
  b1, b2 = st.columns([1, 2])
  with b1:
    if st.button("다시 테스트", type="primary", use_container_width=True):
      reset_test()
      st.rerun()

  with b2:
    alt_types = ", ".join(type_code for type_code, _ in ranked[1:4])
    share_text = (
      f"Workstyle 16 결과: {best_type} — {name}\n"
      f"근접 타입: {alt_types}\n"
      f"Prototype fit: {fit}%"
    )
    st.code(share_text, language=None)

  st.markdown('</div>', unsafe_allow_html=True)


def main():
  init_state()
  st.markdown(CSS, unsafe_allow_html=True)
  render_brand()

  if st.session_state.screen == "intro":
    render_intro()
  elif st.session_state.screen == "quiz":
    render_quiz()
  else:
    render_result()

  st.markdown(
    '<div class="footer">Workstyle 16 · Streamlit prototype</div>',
    unsafe_allow_html=True,
  )


if __name__ == "__main__":
  main()
