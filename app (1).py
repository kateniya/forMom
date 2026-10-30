import streamlit as st

st.set_page_config(page_title="장보기 메모", page_icon="🛒", layout="centered")

CATS = {
    "🥬 야채": ["피망", "양배추", "적상추", "청상추", "깻잎", "시금치", "배추", "대파", "양파", "마늘",
              "당근", "오이", "애호박", "고추", "브로콜리", "감자", "고구마", "무", "토마토", "버섯"],
    "🍎 과일": ["사과", "배", "바나나", "귤", "오렌지", "포도", "딸기", "수박", "참외", "복숭아",
              "감", "키위", "블루베리", "망고", "레몬", "방울토마토"],
    "🥩 정육/계란": ["삼겹살", "목살", "소고기(불고기)", "소고기(국거리)", "닭가슴살", "닭다리", "닭볶음탕용",
                 "돼지고기(앞다리)", "다짐육", "햄", "소시지", "베이컨", "계란", "메추리알"],
    "🐟 수산/건어물": ["고등어", "갈치", "오징어", "새우", "연어", "조개", "굴", "꽃게", "어묵",
                  "멸치", "김", "미역", "다시마", "북어채"],
    "🥛 유제품/냉장": ["우유", "두유", "요거트", "치즈", "버터", "두부", "콩나물", "순두부",
                  "김치", "만두", "냉동피자", "냉동식품", "아이스크림"],
    "🍚 쌀/면/곡물": ["쌀", "잡곡", "라면", "국수", "파스타면", "당면", "즉석밥", "시리얼", "오트밀", "밀가루", "부침가루"],
    "🧂 양념/소스": ["소금", "설탕", "간장", "된장", "고추장", "참기름", "식용유", "올리브유", "식초",
                 "고춧가루", "후추", "케첩", "마요네즈", "카레", "쌈장"],
    "🥫 통조림/가공": ["참치캔", "스팸", "통조림 과일", "잼", "땅콩버터", "콩통조림", "레토르트", "국/찌개 밀키트"],
    "🍪 과자/간식": ["과자", "초콜릿", "젤리", "사탕", "견과류", "육포", "쿠키", "빵", "식빵", "떡"],
    "🥤 음료/주류": ["생수", "탄산수", "콜라", "사이다", "주스", "커피", "차(티백)", "이온음료", "맥주", "소주", "와인"],
    "🧴 생필품": ["휴지", "물티슈", "세제", "샴푸", "바디워시", "치약", "칫솔", "주방세제",
               "쓰레기봉투", "키친타월", "비누", "섬유유연제", "건전지", "랩/호일"],
    "💊 건강/위생": ["마스크", "밴드", "소독제", "비타민", "생리대", "기저귀", "면도기", "화장솜", "핸드워시"],
    "🐶 반려동물": ["강아지 사료", "고양이 사료", "간식", "배변패드", "모래"],
    "📦 기타": ["일회용 컵", "종이컵", "지퍼백", "전구", "문구류", "꽃/화분"],
}
STAR = {1: "★☆☆", 2: "★★☆", 3: "★★★"}

st.markdown("""<style>
.block-container{padding:1.2rem .8rem 0 .8rem;max-width:560px}
header,footer{visibility:hidden;height:0}
div[data-testid="stVerticalBlock"]{gap:.25rem}
.stButton button,[data-testid="stPopover"] button{padding:.1rem .4rem;min-height:2rem}
.bar{background:#16a34a;color:#fff;border-radius:10px;padding:.4rem .7rem;
display:flex;justify-content:space-between;font-weight:700;margin-bottom:.5rem}
.row{font-size:.95rem;line-height:2rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s3{color:#dc2626}.s2{color:#d97706}.s1{color:#6b7280}
</style>""", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("items", [])
ss.setdefault("nid", 1)

def find(i):
    return next(x for x in ss["items"] if x["id"] == i)

def setst(i, status, **kw):
    it = find(i); it["status"] = status; it.update(kw)

todo = sorted([x for x in ss["items"] if x["status"] == "todo"], key=lambda x: -x["imp"])
cart = [x for x in ss["items"] if x["status"] == "cart"]
skip = [x for x in ss["items"] if x["status"] == "skip"]
total = sum(x["price"] * x["qty"] for x in cart)

# ---- 상단 현황바 (항상 보임)
st.markdown(f'<div class="bar"><span>🛒 {len(cart)}개 담음 · 남은 {len(todo)}개</span>'
            f'<span>{total:,.0f}원</span></div>', unsafe_allow_html=True)

# ---- 추가
with st.popover("➕ 메모 추가", use_container_width=True):
    c0, c1 = st.columns(2)
    cat = c0.selectbox("카테고리", list(CATS), key="cat_sel", label_visibility="collapsed")
    name = c1.selectbox("상품", CATS[cat], key=f"prod_{cat}", label_visibility="collapsed")
    c2, c3 = st.columns([1, 1])
    imp = c2.radio("중요도", [1, 2, 3], index=1, horizontal=True, key="imp_sel")
    limit = c3.number_input("패스 기준가(원)", 0, step=500, key="lim_sel", help="0=기준 없음")
    if st.button("추가", use_container_width=True, type="primary"):
        ss["items"].append(dict(id=ss["nid"], cat=cat, name=name, imp=imp,
                                limit=limit, status="todo", price=0, qty=0))
        ss["nid"] += 1
        st.rerun()
    st.caption("중요도 3=꼭 사야 함 / 1=비싸면 안 사도 됨")

# ---- 살 것 목록
if not todo:
    st.caption("살 물건이 없어요. ➕로 추가하세요.")
for x in todo:
    c1, c2, c3 = st.columns([6, 1.3, 1.1], vertical_alignment="center")
    lim = f" ≤{x['limit']:,.0f}" if x["limit"] else ""
    c1.markdown(f'<div class="row s{x["imp"]}">{x["cat"].split()[0]} <b>{x["name"]}</b> '
                f'{STAR[x["imp"]]}<small>{lim}</small></div>', unsafe_allow_html=True)
    with c2.popover("🛒"):
        p = st.number_input("단가(원)", 0, step=100, key=f"p{x['id']}")
        q = st.number_input("수량", 1, value=1, key=f"q{x['id']}")
        over = x["limit"] and p > x["limit"]
        if over and x["imp"] < 3:
            st.warning(f"기준가 {x['limit']:,.0f}원 초과! 중요도 {x['imp']} → 패스 추천")
            if st.button("🙅 안 사기(패스)", key=f"ps{x['id']}", use_container_width=True):
                setst(x["id"], "skip"); st.rerun()
        elif over:
            st.info("기준가 초과지만 중요도 3이라 구매 권장")
        if st.button(f"담기 {p * q:,.0f}원", key=f"a{x['id']}", type="primary",
                     use_container_width=True, disabled=p <= 0):
            setst(x["id"], "cart", price=p, qty=q); st.rerun()
    if c3.button("✕", key=f"x{x['id']}", help="패스(안 사기)"):
        setst(x["id"], "skip"); st.rerun()

# ---- 담은 물건 / 패스
if cart:
    with st.expander(f"✅ 담은 물건 {len(cart)}개 · {total:,.0f}원"):
        for x in cart:
            a, b = st.columns([6, 1.3], vertical_alignment="center")
            a.markdown(f'<div class="row">{x["name"]} {x["price"]:,.0f}×{x["qty"]}='
                       f'<b>{x["price"] * x["qty"]:,.0f}</b></div>', unsafe_allow_html=True)
            if b.button("↩", key=f"u{x['id']}", help="카트에서 빼기"):
                setst(x["id"], "todo"); st.rerun()
if skip:
    with st.expander(f"🙅 패스 {len(skip)}개"):
        for x in skip:
            a, b = st.columns([6, 1.3], vertical_alignment="center")
            a.markdown(f'<div class="row">{x["name"]} {STAR[x["imp"]]}</div>', unsafe_allow_html=True)
            if b.button("↩", key=f"r{x['id']}", help="다시 목록으로"):
                setst(x["id"], "todo"); st.rerun()
