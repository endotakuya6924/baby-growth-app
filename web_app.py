import streamlit as st
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("赤ちゃん成長記録アプリ")
birthday = st.date_input("誕生日")
days_old = (date.today() - birthday).days

st.metric("生後日数", str(days_old) + "日")

name = st.text_input("赤ちゃんの名前")
weight = st.text_input("今日の体重(g)")
height = st.text_input("今日の身長(cm)")

uploaded_file = st.file_uploader(
    "今日の写真",
    type=["jpg", "jpeg", "png"]
)
if uploaded_file is not None:
    st.image(
    uploaded_file,
    caption="今日の写真",
    width=300
)
if st.button("保存"):
    today = date.today()

    with open("record.txt", "a") as file:
        file.write(
    str(today) + "," +
    name + "," +
    weight + "," +
    height + "\n"
)
    st.success("保存しました！")
    if uploaded_file is not None:

        if not os.path.exists("photos"):
            os.makedirs("photos")

        photo_name = str(date.today()) + "_" + uploaded_file.name

        with open(
            os.path.join("photos", photo_name),
            "wb"
        ) as f:
            f.write(uploaded_file.getbuffer())
st.subheader("成長記録一覧")

records = []

with open("record.txt", "r") as file:
    for line in file:
        parts = line.strip().split(",")

        if len(parts) == 4and parts[2].isdigit():
            records.append({
    "日付": parts[0],
    "名前": parts[1],
    "体重(g)": int(parts[2]),
    "身長(cm)": float(parts[3])
})

df = pd.DataFrame(records)
if len(df) > 0:
    current_weight = df["体重(g)"].iloc[-1]
    current_height = df["身長(cm)"].iloc[-1]
if len(df) > 1:
    diff_height = current_height - df["身長(cm)"].iloc[-2]
else:
    diff_height = 0

    if len(df) > 1:
        diff_weight = current_weight - df["体重(g)"].iloc[-2]
    else:
        diff_weight = 0

    st.metric(
        "現在体重",
        f"{current_weight} g",
        f"{diff_weight:+} g"
    )
    st.metric(
    "現在身長",
    f"{current_height} cm"
)
    st.write(f"前回比 {diff_height:+.1f} cm")
st.table(df.set_index("日付"))

st.subheader("体重グラフ")

fig, ax = plt.subplots()
ax.plot(df["日付"], df["体重(g)"], marker="o")
ax.set_title("体重推移")
ax.set_ylabel("体重(g)")

st.pyplot(fig)
st.subheader("身長グラフ")

fig2, ax2 = plt.subplots()

ax2.plot(df["日付"], df["身長(cm)"], marker="o")

ax2.set_title("Height Growth")
ax2.set_ylabel("Height(cm)")

st.pyplot(fig2)
st.subheader("写真アルバム")

if os.path.exists("photos"):
    photo_files = sorted(os.listdir("photos"), reverse=True)

    for photo in photo_files:
        st.write("📅 " + photo[:10])

        st.image(
    os.path.join("photos", photo),
    use_container_width=True
)

else:
    st.write("まだ写真は保存されていません")