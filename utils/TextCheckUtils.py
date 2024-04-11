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
	if keyword in text_data_cache:
		print(keyword)


if __name__ == '__main__':
	word_dir = '../word'
	load_file_data(word_dir)
	search_word("")

