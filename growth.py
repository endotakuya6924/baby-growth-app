from datetime import date

today = date.today()

name = input("赤ちゃんの名前を入力してください：")
weight = input("今日の体重(g)を入力してください：")

with open("record.txt", "a") as file:
    file.write(str(today) + "," + name + "," + weight + "\n")

print("保存しました！")
