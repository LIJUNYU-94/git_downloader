import requests
import os
import zipfile

def download_and_extract_github_repo(github_url, extract_path=None):
    """
    GitHubのリポジトリをダウンロードし、自動でZIPを展開した後、ZIPファイルを削除する関数
    :param github_url: GitHubのリポジトリURL（例: https://github.com/user/repo）
    :param extract_path: ZIPを展開するフォルダ名（指定しない場合、リポジトリ名）
    """
    if not github_url.startswith("https://github.com/"):
        print("エラー: 正しいGitHubのURLを入力してください。")
        return

    repo_name = github_url.rstrip('/').split("/")[-1]
    zip_url = f"{github_url}/archive/refs/heads/main.zip"  # メインブランチを対象
    zip_path = f"{repo_name}.zip"  # 一時的なZIPファイル名

    if extract_path is None:
        extract_path = repo_name  # デフォルトの展開フォルダ名

    try:
        # ZIPファイルをダウンロード
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()

        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"{repo_name} のリポジトリを {zip_path} にダウンロードしました。")

        # ZIPを解凍
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        print(f"{zip_path} を {extract_path} に展開しました。")

        # ダウンロードしたZIPを削除
        os.remove(zip_path)
        print(f"ダウンロードしたZIP {zip_path} を削除しました。")

    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
    except zipfile.BadZipFile:
        print("エラー: ZIPファイルが破損している可能性があります。")

if __name__ == "__main__":
    github_url = input("GitHubリポジトリのURLを入力してください: ")
    extract_folder = input("展開するフォルダ名（空欄ならリポジトリ名）: ").strip()

    if not extract_folder:
        extract_folder = None  # デフォルトのフォルダ名を使用

    download_and_extract_github_repo(github_url, extract_folder)
