# -*- coding: utf-8 -*-

import json
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import datetime
import os
import re

# Json（dict）をパースする関数
def parse_json(conversations):
    # 結果格納
    result = True
    result_items = []

    # 現在ノード一覧取得
    key_current_node = "current_node"
    
    for conversation in conversations:
        if not conversation["current_node"]:
            continue

        title = conversation["title"]
        messages = []
        body = ""

        current_node = conversation[key_current_node]

        while current_node:
            node = conversation["mapping"][current_node]
            if node["message"] and \
                node["message"]["content"] and \
                node["message"]["content"]["content_type"] == "text" and \
                len(node["message"]["content"]["parts"][0]) > 0 and \
                node["message"]["author"]["role"] != "system":

                author = node["message"]["author"]["role"]
                message = node["message"]["content"]["parts"][0]
                messages.append(message)
                messages.append("**" + author + "**  \n")
                messages.append('  \n')

            current_node = node["parent"]
        
        messages.reverse();
        for m in messages:
            body += m
            body += '  \n'

        result_items.append((title, body))

    return (result, result_items)

# ファイルを選択する関数
def select_file():
    # ファイル選択ダイアログを表示する
    file_path = filedialog.askopenfilename(initialdir='.', title='ファイルを選択')

    # ファイルが選択された場合は処理を続行する
    if file_path:
        # JSONファイルを読み込む
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "ファイルが見つかりませんでした")
            sys.exit()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "JSONデータの読み込みに失敗しました")
            sys.exit()

        # ファイル名に使えないパターン
        pattern = r"[/:\*\?\"<>\|]"

        # Pythonのデータ構造に変換する
        result = parse_json(data);

        # 結果をファイルに書き出す
        if result[0]:
            result_items = result[1]

            today = datetime.date.today()
            today_str = today.strftime('%Y-%m-%d')

            os.makedirs(today_str, exist_ok=True)
            for item in result_items:

                # テキストファイルを開く
                file_path = today_str + '\\' + item[0] + '.md'
                file_path = re.sub(pattern, "", file_path)

                with open(file_path, 'w', encoding='UTF-8') as f:
                    # データをテキストファイルに書き出す
                    for body in item[1]:
                        f.write('\n'.join(body))
        else:
            messagebox.showinfo("Error", "Jsonパースに失敗しました")
            sys.exit()


        messagebox.showinfo("Information", "処理が完了しました")
    
    sys.exit()

# GUIアプリケーションを作成する
root = tk.Tk()
root.withdraw()

select_file()

# アプリケーションを開始する
root.mainloop()