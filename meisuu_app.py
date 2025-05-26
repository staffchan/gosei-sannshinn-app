
import streamlit as st
import pandas as pd
import datetime
import os

# データ読み込み
df = pd.read_excel("meisuu_data_1970s.xlsx")
df_types = pd.read_excel("type_info_template.xlsx")

# タイプ名 → 画像ファイル名
def type_to_filename(type_name):
    mapping = {
        "金の羅針盤": "kin_rashinban.png",
        "銀の羅針盤": "gin_rashinban.png",
        "金のインディアン": "kin_indian.png",
        "銀のインディアン": "gin_indian.png",
        "金の鳳凰": "kin_phoenix.png",
        "銀の鳳凰": "gin_phoenix.png",
        "金の時計": "kin_clock.png",
        "銀の時計": "gin_clock.png",
        "金のカメレオン": "kin_chameleon.png",
        "銀のカメレオン": "gin_chameleon.png",
        "金のイルカ": "kin_dolphin.png",
        "銀のイルカ": "gin_dolphin.png"
    }
    return mapping.get(type_name)

# 命数 → タイプ名
def get_gosei_type(year, meisuu):
    kin_or_gin = "金" if year % 2 == 0 else "銀"
    if 1 <= meisuu <= 10:
        base = "羅針盤"
    elif 11 <= meisuu <= 20:
        base = "インディアン"
    elif 21 <= meisuu <= 30:
        base = "鳳凰"
    elif 31 <= meisuu <= 40:
        base = "時計"
    elif 41 <= meisuu <= 50:
        base = "カメレオン"
    elif 51 <= meisuu <= 60:
        base = "イルカ"
    else:
        base = "不明"
    return f"{kin_or_gin}の{base}"

# 欲の傾向判定関数
def get_desire(meisuu):
    last_digit = meisuu % 10
    if last_digit in [1, 2]:
        return "自我欲（自分を中心に考えたい欲）"
    elif last_digit in [3, 4]:
        return "食欲・性欲（楽しみたい欲）"
    elif last_digit in [5, 6]:
        return "金欲・財欲（得をしたい欲）"
    elif last_digit in [7, 8]:
        return "権力・支配欲（上に立ちたい欲）"
    else:  # 9 or 0
        return "創作欲（才能を発揮したい欲）"

# UI構築
st.title("五星三心占い｜命数＆タイプ診断")

# 生年月日を選択
col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("西暦", list(range(1970, 1980)))
with col2:
    month = st.selectbox("月", list(range(1, 13)))
with col3:
    day = st.selectbox("日", list(range(1, 32)))

# データ検索
row = df[(df["年"] == year) & (df["月"] == month) & (df["日"] == day)]

if not row.empty:
    m1 = int(row["命数1"].values[0])
    m2 = int(row["命数2"].values[0])
    m3 = int(row["命数3"].values[0])
    type_name = get_gosei_type(year, m2)

    st.markdown(f"## 🌟 あなたの五星三心タイプ：**{type_name}**")
    st.markdown("### 🔍 命数の内訳")
    st.markdown(f'''
    - 🕰 **第一の命数（過去・ベースとなる性質）**：{m1}
    - 🌟 **第二の命数（現在・個性）**：{m2}
    - 🚀 **第三の命数（未来・才能）**：{m3}
    ''')
    
# 欲の傾向を表示
desire = get_desire(m2)
st.markdown("### 🔥 あなたに強い欲の傾向")
st.markdown(f"**{desire}**")
    
type_row = df_types[df_types["タイプ名"] == type_name]
if not type_row.empty:
        st.markdown("### 💫 持っている星")
        stars = type_row["持っている星"].values[0]
        st.markdown(f"<div style='background-color:#f0f8ff;padding:10px;border-radius:8px'>{stars}</div>", unsafe_allow_html=True)

        st.markdown("### 📖 基本性格")
        traits = type_row["基本性格"].values[0]
        st.markdown(traits)

        filename = type_to_filename(type_name)
        if filename:
        image_path = f"images/{filename}"
        st.image(image_path, caption=f"{type_name}のイメージ", use_container_width=True)
else:
    st.warning("この日付のデータはまだ登録されていません。")
