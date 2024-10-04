import re


def count_words(text: str) -> int:
    """
    统计文本中的中文和英文词数。

    对于英文，通过空格和标点符号分割单词。
    对于中文，每个汉字视为一个词。

    参数:
        text (str): 要统计的文本。

    返回:
        int: 文本中的总词数。
    """
    # 统计英文单词
    english_words = re.findall(r'\b\w+\b', text)
    # 统计中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(english_words) + len(chinese_chars)


def optimize_subtitles(asr_data):
    """
    优化字幕分割，合并词数少于等于4且时间相邻的段落。

    参数:
        asr_data (ASRData): 包含字幕段落的 ASRData 对象。
    """
    for i in range(len(asr_data.segments) - 1, 0, -1):
        seg = asr_data.segments[i]
        prev_seg = asr_data.segments[i - 1]

        # 判断前一个段落的词数是否小于等于5且时间相邻
        if count_words(prev_seg.text) <= 4 and abs(seg.start_time - prev_seg.end_time) < 100 and count_words(seg.text) <= 10:
            # print(prev_seg.end_time, seg.start_time)
            # print(f"[-]合并段落: 【{prev_seg.text}】 --- 【{seg.text}】")
            asr_data.merge_with_next_segment(i - 1)


if __name__ == '__main__':
    text = "they were manufacturing 1"
    print(count_words(text))  # 3

    text = "你好  world"
    print(count_words(text))  # 3

    text = "Hello, 世界！你好，world！"
    print(count_words(text))  # 6