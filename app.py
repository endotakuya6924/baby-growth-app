import tkinter as tk
from datetime import date

def save_record():
    name = name_entry.get()
    weight = weight_entry.get()
    today = date.today()

    with open("record.txt", "a") as file:
        file.write(str(today) + "," + name + "," + weight + "\n")

    message_label.config(text="保存しました！")

window = tk.Tk()
window.title("赤ちゃん成長記録アプリ")
window.geometry("420x320")
window.configure(bg="lightgray")

title_label = tk.Label(window, text="赤ちゃん成長記録", bg="lightgray", fg="black", font=("Arial", 20))
title_label.place(x=90, y=30)

name_label = tk.Label(window, text="赤ちゃんの名前", bg="lightgray", fg="black", font=("Arial", 14))
name_label.place(x=140, y=80)

name_entry = tk.Entry(window, width=25, bg="white", fg="black")
name_entry.place(x=120, y=110)

weight_label = tk.Label(window, text="今日の体重(g)", bg="lightgray", fg="black", font=("Arial", 14))
weight_label.place(x=140, y=150)

weight_entry = tk.Entry(window, width=25, bg="white", fg="black")
weight_entry.place(x=120, y=180)

save_button = tk.Button(window, text="保存", command=save_record)
save_button.place(x=180, y=225)

message_label = tk.Label(window, text="", bg="lightgray", fg="black", font=("Arial", 14))
message_label.place(x=150, y=265)

window.mainloop()