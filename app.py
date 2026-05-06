import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="コンデンサー容量・種類判別", layout="centered")

# --- カスタムCSS（コンデンサーの外観用） ---
st.markdown("""
    <style>
    .credit { text-align: right; font-size: 14px; color: #666; margin-bottom: -20px; }
    .cap-visual {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        margin: 10px 0;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        text-shadow: 1px 1px 2px black;
        min-height: 100px;
    }
    /* 種類別の色設定 */
    .ceramic { background-color: #D2B48C; border: 3px solid #A52A2A; width: 80px; height: 80px; border-radius: 50%; } /* 茶丸 */
    .tantalum { background-color: #FFA500; border: 3px solid #FF8C00; width: 70px; height: 90px; border-radius: 20% 20% 50% 50%; } /* 雫型 */
    .film { background-color: #FF4500; border: 3px solid #8B0000; width: 100px; height: 70px; border-radius: 5px; } /* 赤四角 */
    
    .result-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)
st.title('⚡ コンデンサー容量・種類判別')

# --- 1. コンデンサーの種類選択 ---
st.subheader("1. 外観の種類を選択")
cap_type = st.radio(
    "形状と種類",
    ["セラミック (円盤型/茶)", "タンタル (雫型/橙)", "積層セラミック/フィルム (四角/赤)"],
    horizontal=True
)

# プレビュー表示
if "セラミック" in cap_type:
    st.markdown('<div style="display: flex; justify-content: center;"><div class="cap-visual ceramic">104</div></div>', unsafe_allow_html=True)
    st.caption("セラミックコンデンサー：安価で高周波に強い。容量は小さめ。")
elif "タンタル" in cap_type:
    st.markdown('<div style="display: flex; justify-content: center;"><div class="cap-visual tantalum">226</div></div>', unsafe_allow_html=True)
    st.caption("タンタルコンデンサー：極性（＋ー）あり。小型で大容量。爆発注意。")
else:
    st.markdown('<div style="display: flex; justify-content: center;"><div class="cap-visual film">473</div></div>', unsafe_allow_html=True)
    st.caption("フィルム/積層セラミック：温度変化に強く、オーディオや精密回路に。")

st.markdown("---")

# --- 2. 数値・カラーコード入力 ---
st.subheader("2. 表記数値の入力 (例: 104)")
col1, col2 = st.columns(2)

with col1:
    code = st.text_input("3桁の数字を入力", value="104", max_chars=3)
with col2:
    voltage = st.selectbox("耐圧記号 (もしあれば)", ["表記なし", "1H (50V)", "2A (100V)", "2E (250V)", "2J (630V)"])

# --- 3. 計算ロジック ---
if len(code) == 3 and code.isdigit():
    n1 = int(code[0])
    n2 = int(code[1])
    n3 = int(code[2])
    
    # 基本は pF (ピコファラド)
    pf_val = (n1 * 10 + n2) * (10 ** n3)
    
    # 単位換算
    nf_val = pf_val / 1000
    uf_val = nf_val / 1000
    
    # 結果表示
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("📊 容量換算結果")
    c1, c2, c3 = st.columns(3)
    c1.metric("μF (マイクロ)", f"{uf_val:g}")
    c2.metric("nF (ナノ)", f"{nf_val:g}")
    c3.metric("pF (ピコ)", f"{pf_val:,}")
    
    if voltage != "表記なし":
        st.info(f"想定耐圧: {voltage.split(' ')[1]}")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("数値を3桁で入力してください（例：104 → 10 + 0000 pF）")

# --- 4. 知っておきたい特殊表記 ---
with st.expander("📝 判別が難しいコンデンサーの知識"):
    st.write("""
    - **チップコンデンサー (SMD):** 表面に何も書いていないことが多いです。基板から外すと容量判別は困難（LCRメータが必要）。
    - **カラーコードコンデンサー:** 抵抗器と同じ色の帯がついています。読み方は抵抗と同じですが、単位は **pF** になります。
    - **R表記:** 「2R2」などの表記がある場合、Rは小数点を表します（2.2pF）。
    - **アルファベット記号 (誤差):** 
        - J = ±5%
        - K = ±10%
        - M = ±20%
    """)
