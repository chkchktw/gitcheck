import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import requests
from concurrent.futures import ThreadPoolExecutor

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

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_repository, urls)

    with open(output_file, 'w') as file:
        for url, repo_type in results:
            if url:
                file.write(f"{url} ({repo_type})\n")

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

tk.Button(root, text="開始檢查", command=run_check).pack()

root.mainloop()
