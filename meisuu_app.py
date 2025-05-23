import streamlit as st
import pandas as pd
import datetime

# データ読み込み
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

# UI
st.title("五星三心占い｜命数＆タイプ診断")

birthday = st.date_input(
    "生年月日を入力してください",
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date(2035, 12, 31)
)

year, month, day = birthday.year, birthday.month, birthday.day
row = df[(df["年"] == year) & (df["月"] == month) & (df["日"] == day)]

if not row.empty:
    meisuu = int(row["命数2"].values[0])
    gossei_type = get_gosei_type(year, meisuu)
    st.success(f"🎯 あなたの命数は **{meisuu}番** です！")
    st.markdown(f"✨ あなたの五星三心タイプは **{gossei_type}** です。")
else:
    st.warning("この日付のデータはまだ登録されていません。")
