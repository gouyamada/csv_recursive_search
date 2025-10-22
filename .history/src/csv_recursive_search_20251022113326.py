"""
CSVファイルを再帰的に調査し、指定された列に特定の文字列が存在するか確認するスクリプト
"""
import os
import csv

# 調査を開始するフォルダ
ROOT_DIR = r"\\server2\OrderCsvFiles"


def get_valid_int_input(prompt: str) -> int:
    """
    summary: ユーザーから有効な整数入力を取得する関数

    args:
        prompt (str): ユーザーに表示するプロンプトメッセージ

    returns:
        int: ユーザーが入力した有効な整数
    """
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        print("数値で入力してください。")


def main():
    """
    summary: メインの調査処理を実行する関数
    """
    print("=== CSVファイル調査スクリプト ===")
    column_number = get_valid_int_input("調査する列番号を1始まりで入力してください: ")
    search_string = input("調査する文字列を入力してください: ")
    # column_number = 2  # 調査する列番号（1始まり）
    # search_string = "5"  # 調査する文字列

    print("\n調査を開始します...\n")

    found_any = False
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.lower().endswith(".csv"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, encoding="utf-8", newline="") as f:
                        reader = csv.reader(f)
                        for line_num, row in enumerate(reader, start=1):
                            if not row:
                                continue

                            first_col = row[0].strip() if len(row) > 0 else ""

                            if first_col.startswith("HD") or first_col.startswith("TR"):
                                continue

                            # 列番号が範囲内であればチェック
                            if len(row) >= column_number:
                                target_value = row[column_number - 1].strip()
                                if target_value == search_string:
                                    print(f"一致: {file_path} 行番号: {line_num}")
                                    found_any = True

                except (FileNotFoundError, PermissionError, UnicodeDecodeError, csv.Error) as e:
                    print(f"ファイル読み込みエラー: {file_path} ({e})")

    if not found_any:
        print("一致するデータは見つかりませんでした。")


if __name__ == "__main__":
    main()
