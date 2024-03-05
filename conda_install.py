import argparse
import os
import requests
from bs4 import BeautifulSoup
import re
import subprocess

def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the HTML content from {url}: {e}")
        return ""

def find_conda_download_link(html_content, version, os_info):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')

    # 调整 os_info 格式以匹配链接中的格式
    os_info_adjusted = os_info.replace('_', '-').replace('linux', 'Linux').replace('x86', 'x86_64')

    # 构建匹配模式
    pattern = re.compile(f"Miniconda3-{version}.*{os_info_adjusted}.sh")

    for link in links:
        if pattern.search(link.text):
            return f"https://repo.anaconda.com/miniconda/{link['href']}"

    return "No matching link found."

def install_conda(version="py39", os_info="linux_x86_64"):
    # 从 URL 获取 HTML 内容
    url = "https://repo.anaconda.com/miniconda/"
    html_content = fetch_html_content(url)

    download_url = find_conda_download_link(html_content, version, os_info)
    if download_url:
        print(f"Downloading Conda from {download_url}")
        subprocess.run(["wget", "-c", download_url, "-O", "miniconda.sh"])
        subprocess.run(["chmod", "+x", "miniconda.sh"])
        subprocess.run(["./miniconda.sh", "-b", "-f", "-p", "/usr/local"], check=True)
        # 将 Conda 添加到 PATH
        os.environ['PATH'] = "/usr/local/bin:" + os.environ['PATH']
        print("Conda installed successfully!")
    else:
        print("Failed to find a Conda download link.")

def main():
    parser = argparse.ArgumentParser(description='Install Conda environment.')
    parser.add_argument('--version', type=str, help='Python version to install with Conda.', default='py39')
    parser.add_argument('--os_info', type=str, help='Operating system info, e.g., linux_x86.', default='linux_x86')
    args = parser.parse_args()

    # 自动下载和安装 Conda
    install_conda(args.version, args.os_info)

    # 验证 Conda 安装
    print("Checking Conda installation...")
    subprocess.run(["which", "conda"])
    subprocess.run(["conda", "--version"])
    subprocess.run(["which", "python"])
    subprocess.run(["python", "--version"])

if __name__ == "__main__":
    main()