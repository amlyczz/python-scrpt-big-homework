import csv
from collections import deque


class DataStorage:

    def __init__(self, filename, max_entries=10):
        self.filename = filename
        self.max_entries = max_entries
        self.fieldnames = ["Title", "Content"]

    def _read_csv(self, has_max_entries=True):
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                last_n_rows = deque(csv.DictReader(file, fieldnames=self.fieldnames, delimiter=';'),
                                    maxlen=self.max_entries) \
                    if has_max_entries \
                    else csv.DictReader(file,
                                        fieldnames=self.fieldnames,
                                        delimiter=';')

                res = list(last_n_rows)
                print(f'读取的最后{len(res)}行记录:{res}')
                return res
        except FileNotFoundError:
            return []

    def _write_csv(self, entries):
        # 如果文件不存在，写入标题
        file_exists = True
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                csv.reader(file, delimiter=';')
        except FileNotFoundError:
            file_exists = False
        with open(self.filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames, delimiter=';')
            if not file_exists:
                writer.writeheader()
            for entry in entries:
                writer.writerow(entry)

    def add_entry(self, title, content):
        existed_titles = {entry['Title'] for entry in self._read_csv()}
        if title in existed_titles:
            print(f'该标题:{title}已存在，不添加该条目')
            return

        self._write_csv([{
            "Title": title,
            "Content": content
        }])


if __name__ == '__main__':
    new_data = {'title': 'New Title', 'content': 'New Content'}
    data_manager = DataStorage("data.csv")
    data_manager.add_entry("Test Title 1", ['Item 1', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 2", ['Item 2', 'Item 3', 'Item 4'])
    data_manager.add_entry("Test Title 2", ['Item 2', 'Item 1', 'Item 3'])
    data_manager.add_entry("Test Title 3", ['Item 2', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 4", ['Item 2', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 4", ['Item 4', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 5", ['Item 4', 'Item 2', 'Item 3'])
