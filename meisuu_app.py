import streamlit as st
import pandas as pd

# データ読み込み（ファイル名は半角・英語に統一しておくこと！）
df = pd.read_excel("meisuu_data_1970s.xlsx")

# タイプ判定関数
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

# --- UI ---
st.title("五星三心占い｜命数＆タイプ診断")

# 西暦・月・日を分けて入力
col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("西暦", list(range(1970, 1980)))
with col2:
    month = st.selectbox("月", list(range(1, 13)))
with col3:
    day = st.selectbox("日", list(range(1, 32)))

# 検索処理
row = df[(df["年"] == year) & (df["月"] == month) & (df["日"] == day)]

if not row.empty:
    m1 = int(row["命数1"].values[0])
    m2 = int(row["命数2"].values[0])
    m3 = int(row["命数3"].values[0])
    type_name = get_gosei_type(year, m2)

    st.success(f"🎯 あなたの命数（現在・個性）は **{m2}番** です")
    st.markdown(f"✨ あなたの五星三心タイプは **{type_name}**")

    st.markdown("#### 🔍 命数の内訳")
    st.markdown(f"""
    - 🕰 **第一の命数（過去・ベースとなる性質）**：{m1}
    - 🌟 **第二の命数（現在・個性）**：{m2}
    - 🚀 **第三の命数（未来・才能）**：{m3}
    """)
else:
    st.warning("この日付のデータはまだ登録されていません。")
import os

# タイプ名から画像ファイル名を返す関数
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

# ▼ タイプ判定後の表示に追加 ▼
filename = type_to_filename(type_name)
if filename:
    image_path = os.path.join("images", filename)
    st.image(image_path, caption=f"{type_name}のイメージ", use_column_width=True)
