# ISBN を基に国会図書館のデータベースから書籍情報を取得する

import time
import urllib.request
from collections import defaultdict

from bs4 import BeautifulSoup


def get_book_info_for_ndl(isbn: str):
    """引数に渡された ISBN から書籍情報を国会図書館のデータベースから検索し､取得された情報をディクショナリで返す
    データが取得できなかった場合は None を返す
    """

    book_info_list = []
    search_isbn_url = f"http://iss.ndl.go.jp/books?search_mode=advanced&rft.isbn={isbn}"

    def check_failue(value: any):
        if value in [200, [], None]:
            return None

    # ISBN の検索結果
    response = urllib.request.urlopen(search_isbn_url)
    check_failue(response.status)

    source = response.read()
    soup = BeautifulSoup(source, "html.parser")
    book_name_data = soup.find_all(class_="item_summarywrapper")
    check_failue(book_name_data)

    # 検索結果の一番上の書籍をデータの取得対象とする
    target_url = book_name_data[0].a.attrs["href"]
    check_failue(target_url)

    # 書籍の詳細情報取得
    response = urllib.request.urlopen(target_url)
    check_failue(response.status)

    source = response.read()
    soup = BeautifulSoup(source, "html.parser")
    contents = soup.find_all(id="itemcontent")
    contents = contents[0].contents[7]

    for c in contents:

        if c != "\n":

            data_tmp = c.text
            data_tmp = data_tmp.replace("\n", "")
            book_info_list.append(data_tmp)

    time.sleep(1)  # インターバル
    return parse_book_data(book_info_list)


def parse_book_data(book_info_list):
    """Web から取得したデータを 項目名:内容 のディクショナリで返す
    get_book_info_for_ndl() で取得したデータの整形用関数
    """

    book_info_dict = {}
    book_info_dict = defaultdict(set)

    for info in book_info_list:

        formated_data = book_info_string_format(info)

        if formated_data is not None:
            book_info_dict[formated_data[0]].add(formated_data[1])

    return book_info_dict


def book_info_string_format(contents: str):
    """書籍情報の項目名と内容を分離する"""

    key_names = [
        "タイトル",
        "著者",
        "著者標目",
        "出版社",
        "出版年月日等",
        "大きさ、容量等",
        "    注記        ",  # 空白を消さないように注意
        "ISBN",
        "NACSIS-CATレコード",
        "別タイトル",
        "出版年(W3CDTF)",
        "件名（キーワード）",
        "NDLC",
        "NDC（10版）",
        "NDC（9版）",
        "NDC(8版)",
        "対象利用者",
        "資料の種別",
        "言語（ISO639-2形式）",
    ]

    for key in key_names:

        if contents.startswith(key):

            tmp = contents.replace(key, "")

            if tmp.startswith("標目"):
                tmp = contents.replace("著者標目", "")
                return ("著者標目", tmp)

            if key == "    注記        ":
                return ("注記", contents)

            return (key, contents)

    return None


def disp_data(book_info: dict):
    print(f"{'*' * 50}")
    for key, value in book_info.items():

        print(f"■{key}")
        for v in value:

            # MEMO: 注記のデータの場合は場合分けして対応しないと文字が揃わない
            v = v.replace(key, "")
            print(f"    {v}")

    print(f"{'*' * 50}")
    print()


def main():

    with open("isbnlist.txt", mode="r", encoding="utf-8") as f:
        isbns = f.readlines()

    for isbn in isbns:

        book_info = get_book_info_for_ndl(isbn)

        if book_info is None:
            print(f"{isbn} is no hit.")
            continue

        if len(book_info) != 0:
            disp_data(book_info)
        else:
            print(f"{isbn} is no hit.")


if __name__ == "__main__":
    main()
