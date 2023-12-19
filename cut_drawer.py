import ast
import re
from collections import Counter

import jieba as jieba
from matplotlib import pyplot as plt
from snownlp import SnowNLP
from wordcloud import WordCloud

import data_storage

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用中文字体，SimHei 是黑体的意思
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def is_file_empty(filename):
    # 使用 try-except 捕获文件不存在的情况
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 读取文件内容并判断是否为空
            return not any(file.read())
    except FileNotFoundError:
        # 文件不存在也认为是空文件
        return True


def write_list_to_file(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        # 将列表中的每个元素写入文件
        for item in data_list:
            file.write(str(item) + '\n')


def read_file_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件的每一行并去除换行符
            content_list = [line.strip() for line in file.readlines()]
            return content_list
    except FileNotFoundError:
        print(f"文件 '{file_path}' 不存在。")
        return []


class CutDrawer:
    def __init__(self, filename='data/data.csv', topn_counts=20):
        self.filename = filename
        self.custom_dict = 'data/custom_dict.txt'
        self.cut_res = 'data/cut_res.txt'
        self.topn_counts = topn_counts
        self.stop_words = read_file_to_list('data/stop_words.txt')
        self.data_storage = data_storage.DataStorage()

    def cut_and_draw(self):
        self._cut_and_save()
        self._analysis_context()

    def _cut_and_save(self):
        with open('data/data.csv', 'r', encoding='utf-8') as file:
            content = file.read()

        # 将分词结果存储到列表中
        if is_file_empty(self.cut_res):
            jieba.load_userdict(self.custom_dict)
            # 分词
            content = re.sub(r'[^\w\s]', '', content)
            words = [word for word in jieba.cut(content) if word.strip() and word not in self.stop_words]
            write_list_to_file(self.cut_res, words)

    def _analysis_context(self):
        word_list = read_file_to_list(self.cut_res)
        character_list = read_file_to_list(self.custom_dict)
        emo_score_list = []
        num_words_list = []
        self._word_freq_draw(word_list)
        entries = self.data_storage.read_csv()

        # emo统计
        self._emo_analysis(character_list, emo_score_list, entries, num_words_list)

    def _emo_analysis(self, character_list, emo_score_list, entries, num_words_list):
        for character in character_list:
            has_character = False
            for entry in entries:
                if character in entry["Title"]:
                    has_character = True
                    # 查找相关词汇
                    print()
                    print()
                    print("entry[\"Content\"]:", entry["Content"])
                    print(f'typeEntryContent{type(entry["Content"])}')
                    actual_list = ast.literal_eval(entry["Content"])
                    actual_list = [item for item in actual_list if item != ""]
                    print(f"acType:{type(actual_list)}")
                    print(f"actual_list:{actual_list}")
                    print("act size: ", len(actual_list))
                    for item in actual_list:
                        print(item)
                    train_data = entry["Content"].split()
                    print(f'train_data:{train_data}')
                    print("type", type(train_data))
                    num_words_list.append(len(train_data))
                    s = SnowNLP(entry["Content"])
                    emo_score_list.append(s.sentiments)
                    break
            if not has_character:
                emo_score_list.append(0)
        print(character_list)
        print(emo_score_list)
        print(len(character_list), len(emo_score_list))
        plt.bar(character_list, emo_score_list, color='blue')
        # 设置标题和坐标轴标签
        plt.title('上下文情感分析')
        plt.xlabel('名称')
        plt.ylabel('情感得分')
        plt.show()

    def _word_freq_draw(self, word_list):
        # 词频统计
        word_freq = Counter(word_list)
        top_words = word_freq.most_common(15)
        cloud_top_words = word_freq.most_common(1000)
        labels, values = zip(*top_words)
        word_cloud_map = {k: int(v) for k, v in cloud_top_words}
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel('词汇')
        plt.ylabel('词频')
        plt.title('词频统计')
        plt.xticks(rotation=45)

        # 词云统计
        wordcloud = WordCloud(font_path='C:\\Windows\\Fonts\\msyh.ttc', width=800, height=400,
                              background_color='white').generate_from_frequencies(
            word_cloud_map)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # 隐藏坐标轴
        plt.show()


if __name__ == '__main__':
    cut_drawer = CutDrawer()
    cut_drawer.cut_and_draw()
