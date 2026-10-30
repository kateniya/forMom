import streamlit as st

st.set_page_config(page_title="장보기 메모", page_icon="🛒", layout="centered")

CATS = {"🥬 야채": "야채", "🍎 과일": "과일", "🥩 육류": "육류", "🐟 수산": "수산",
        "🥛 유제품": "유제품", "🍞 빵/간식": "빵/간식", "🧴 생필품": "생필품", "📦 기타": "기타"}
STAR = {1: "★☆☆", 2: "★★☆", 3: "★★★"}

st.markdown("""<style>
.block-container{padding:.6rem .8rem 0 .8rem;max-width:560px}
header,footer{visibility:hidden;height:0}
div[data-testid="stVerticalBlock"]{gap:.25rem}
.stButton button,[data-testid="stPopover"] button{padding:.1rem .4rem;min-height:2rem}
.bar{background:#16a34a;color:#fff;border-radius:10px;padding:.4rem .7rem;
display:flex;justify-content:space-between;font-weight:700}
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
    with st.form("add", clear_on_submit=True):
        c1, c2 = st.columns([1, 1.4])
        cat = c1.selectbox("카테고리", list(CATS), label_visibility="collapsed")
        name = c2.text_input("상품명", placeholder="상품명 (예: 대파 1단)", label_visibility="collapsed")
        c3, c4 = st.columns(2)
        imp = c3.radio("중요도", [1, 2, 3], index=1, horizontal=True,
                       format_func=lambda v: f"{v}")
        limit = c4.number_input("이 가격 넘으면 패스(원, 0=없음)", 0, step=500)
        if st.form_submit_button("추가", use_container_width=True) and name.strip():
            ss["items"].append(dict(id=ss["nid"], cat=cat, name=name.strip(), imp=imp,
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
