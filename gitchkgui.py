import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import requests
import time

def check_repository(url):
    try:
        # 檢查 Git 儲存庫
        git_response = requests.get(url + '/.git/HEAD', timeout=5)
        git_content = git_response.text.lower()
        if git_response.status_code == 200 and not any(keyword in git_content for keyword in ['block', 'support id', 'rejected']):
            return url, 'Git'

        # 檢查 SVN 儲存庫
        svn_response = requests.get(url + '/.svn/entries', timeout=5)
        svn_content = svn_response.text.lower()
        if svn_response.status_code == 200 and not any(keyword in svn_content for keyword in ['block', 'support id', 'rejected']):
            return url, 'SVN'
    except requests.RequestException:
        pass
    return None, None

def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def run_check():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not input_file or not output_file:
        messagebox.showerror("錯誤", "請選擇檔案")
        return

    with open(input_file, 'r') as file:
        urls = file.read().splitlines()

    progress_text.config(text="進度：0%")
    result_text.delete(1.0, tk.END)  # 清空結果顯示區域

    for i, url in enumerate(urls):
        result, repo_type = check_repository(url)
        if result:
            result_text.insert(tk.END, f"{result} ({repo_type})\n")

        # 更新進度文本
        progress_value = int((i + 1) / len(urls) * 100)
        progress_text.config(text=f"進度：{progress_value}%")
        root.update()  # 更新視窗

    messagebox.showinfo("完成", "檢查完成")

# 設置 GUI
root = tk.Tk()
root.title("Git/SVN 檢查工具")

input_entry = tk.Entry(root, width=50)
input_entry.pack()
tk.Button(root, text="選擇輸入檔案", command=load_file).pack()

output_entry = tk.Entry(root, width=50)
output_entry.pack()
tk.Button(root, text="選擇輸出檔案", command=save_file).pack()

progress_text = tk.Label(root, text="進度：0%")
progress_text.pack()

result_text = tk.Text(root, width=50, height=10)
result_text.pack()

tk.Button(root, text="開始檢查", command=run_check).pack()

root.mainloop()
