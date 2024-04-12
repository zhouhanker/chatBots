import os

text_data_cache = []


def load_file_data(directory):
	# 获取目录下所有文件
	files = os.listdir(directory)
	for file_name in files:
		if file_name.endswith('.txt'):
			file_path = os.path.join(directory, file_name)
			with open(file_path, 'r', encoding='utf8') as file:
				# 逐行读取文件内容
				for line in file:
					text_data_cache.append(line.strip())


def search_word(keyword):
	for text in text_data_cache:
		if keyword.find(text):
			return hide_string(keyword)
		else:
			return None


def check_black_text(msg):
	word_dir = '../word'
	load_file_data(word_dir)
	return search_word(msg)


def hide_string(input_str):
	# 如果字符串长度小于等于1，则直接返回原字符串
	if len(input_str) <= 1:
		return input_str
	# 生成需要隐藏的部分
	hidden_part = '*' * (len(input_str) - 1)
	# 返回隐藏部分和最后一个字符组成的字符串
	return hidden_part + input_str[-1]


if __name__ == '__main__':
	s1 = '小b崽子123'
	print(check_black_text(s1))
