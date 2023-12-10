import csv


class DataStorage:

    def __init__(self, filename='data/data.csv', max_entries=10):
        self.filename = filename
        self.max_entries = max_entries
        self.fieldnames = ["Title", "Content"]

    def read_csv(self):
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                res = list(csv.DictReader(file, fieldnames=self.fieldnames, delimiter=';'))
                # print(f'读取{len(res)}行记录:{res}')
                return res
        except FileNotFoundError:
            return []

    def write_csv(self, entries):
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
        existed_titles = {entry['Title'] for entry in self.read_csv()}
        if title in existed_titles:
            print(f'该标题:{title}已存在，不添加该条目')
            return
        print(f'添加该条目，标题:{title}')
        self.write_csv([{
            "Title": title,
            "Content": content
        }])


if __name__ == '__main__':
    new_data = {'title': 'New Title', 'content': 'New Content'}
    data_manager = DataStorage("data/data.csv")
    data_manager.add_entry("Test Title 1", ['Item 1', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 2", ['Item 2', 'Item 3', 'Item 4'])
    data_manager.add_entry("Test Title 2", ['Item 2', 'Item 1', 'Item 3'])
    data_manager.add_entry("Test Title 3", ['Item 2', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 4", ['Item 2', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 4", ['Item 4', 'Item 2', 'Item 3'])
    data_manager.add_entry("Test Title 5", ['Item 4', 'Item 2', 'Item 3'])
