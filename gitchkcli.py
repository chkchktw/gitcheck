import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

def check_repository(url):
    try:
        # 檢查 Git 儲存庫
        git_response = requests.get(url + '/.git/HEAD', timeout=1)
        git_content = git_response.text.lower()
        if git_response.status_code == 200 and not any(keyword in git_content for keyword in ['block', 'support id', 'rejected']):
            return f"找到 Git 儲存庫：{url}"

        # 檢查 SVN 儲存庫
        svn_response = requests.get(url + '/.svn/entries', timeout=1)
        svn_content = svn_response.text.lower()
        if svn_response.status_code == 200 and not any(keyword in svn_content for keyword in ['block', 'support id', 'rejected']):
            return f"找到 SVN 儲存庫：{url}"

        # 如果都未找到，返回未發現的結果
        return f"未發現：{url}"
    except requests.RequestException:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description='搜尋URL中的Git儲存庫')
    parser.add_argument('url_list', help='包含URL清單的檔案名稱')
    parser.add_argument('-o', '--output', help='指定輸出檔案名稱')

    args = parser.parse_args()

    with open(args.url_list, 'r') as file:
        urls = file.read().splitlines()

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for result in executor.map(check_repository, urls):
            if result:
                print(result)
                results.append(result)

    if args.output:
        with open(args.output, 'w') as file:
            for result in results:
                file.write(result + '\n')

    if results:
        print("\n以下URL發現GIT:")
        for result in results:
            print(result)

if __name__ == '__main__':
    main()
