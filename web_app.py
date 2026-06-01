import gspread
from google.oauth2.service_account import Credentials
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("赤ちゃん成長記録アプリ")
birthday = st.date_input(
    "誕生日",
    value=date(2026, 5, 26)
)
days_old = (date.today() - birthday).days

st.metric("生後日数", str(days_old) + "日")

name = st.text_input("赤ちゃんの名前", value="遠藤史親")
weight = st.text_input("今日の体重")
height = st.text_input("今日の身長")
milk = st.text_input("ミルク量")
memo = st.text_area("今日のメモ")

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1UPNcnr_nAcvuihUmWIFjf00ymyca8lyLTWiEFGt3CwU/edit?pli=1&gid=0#gid=0"
).sheet1

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
    sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1UPNcnr_nAcvuihUmWIFjf00ymyca8lyLTWiEFGt3CwU/edit?pli=1&gid=0#gid=0"
).sheet1
if st.button("保存"):
    today = date.today()

    with open("record.txt", "a") as file:
        file.write(
    str(today) + "," +
    name + "," +
    weight + "," +
    height + "\n"
    )


from datetime import date
today = date.today()
if not weight:
    weight = ""

if not height:
    height = ""

if not milk:
    milk = ""

if not memo:
    memo = ""
photo_name = ""

if uploaded_file is not None:
    photo_name = str(date.today()) + "_" + uploaded_file.name

sheet.append_row([
    str(today),
    name,
    weight,
    height,
    milk,
    memo,
    photo_name
])

st.success("保存しました！")

if uploaded_file is not None:
    photo_name = str(date.today()) + "_" + uploaded_file.name

    if not os.path.exists("photos"):
        os.makedirs("photos")

    with open(os.path.join("photos", photo_name), "wb") as f:
        f.write(uploaded_file.getbuffer())
else:
    photo_name = ""
st.subheader("成長記録一覧")

sheet_data = sheet.get_all_records()
df = pd.DataFrame(sheet_data)
st.write(df.columns.tolist())

df["体重"] = pd.to_numeric(df["体重"], errors="coerce")
df["身長"] = pd.to_numeric(df["身長"], errors="coerce")
df["ミルク量"] = pd.to_numeric(df["ミルク量"], errors="coerce")

if len(df) > 0:
    current_weight = df["体重"].iloc[-1]
    current_height = df["身長"].iloc[-1]
if len(df) > 1:
    diff_height = current_height - float(df["身長"].iloc[-2])
else:
    diff_height = 0

    if len(df) > 1:
        diff_weight = current_weight - df["体重"].iloc[-2]
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
if len(df) >= 2:

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    
    weight_diff = latest["体重"] - previous["体重"]
    height_diff = latest["身長"] - previous["身長"]
    milk_diff = latest["ミルク量"] - previous["ミルク量"]
    st.subheader("前回比")

    st.metric(
        "体重増加",
        f"{latest['体重']} g",
        f"{weight_diff:+.0f} g"
    )

    st.metric(
        "身長増加",
        f"{latest['身長']} cm",
        f"{height_diff:+.1f} cm"
    )
    st.metric(
    "ミルク量",
    f'{latest["ミルク量"]} ml',
    f'{milk_diff:+} ml'
)
   
st.subheader("体重グラフ")

fig, ax = plt.subplots()
ax.plot(df["日付"], df["体重"], marker="o")
ax.set_title("体重推移")
ax.set_ylabel("体重")

st.pyplot(fig)
st.subheader("身長グラフ")

fig2, ax2 = plt.subplots()

ax2.plot(df["日付"], df["身長"], marker="o")

ax2.set_title("Height Growth")
ax2.set_ylabel("Height(cm)")

st.pyplot(fig2)
st.subheader("写真アルバム")

st.subheader("📸 写真アルバム")

if os.path.exists("photos"):

    photo_files = sorted(
        os.listdir("photos"),
        reverse=True
    )

    for photo in photo_files:

        st.image(
            os.path.join("photos", photo),
            caption=photo,
            width=300
        )

else:
    st.write("まだ写真はありません")


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)
st.subheader("📝 NICU日記")

if "メモ" in df.columns:

    diary_df = df[
    df["メモ"].notna() &
    (df["メモ"].astype(str).str.strip() != "")
]

diary_df = diary_df.drop_duplicates(
    subset=["日付", "メモ"]
)

diary_df = diary_df.sort_values(
    "日付",
    ascending=False
)

for _, row in diary_df.iterrows():
    st.markdown(f"### 📅 {row['日付']}")
    st.info(row["メモ"])

    photo_name = str(row["写真"]).strip()
    if photo_name and photo_name != "nan":
        photo_path = os.path.join("photos", photo_name)
        if os.path.exists(photo_path):
            st.image(photo_path, width=300)

    st.divider()

