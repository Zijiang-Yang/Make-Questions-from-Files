from dotenv import load_dotenv
load_dotenv()
from utils.get_exam_url import get_url
if __name__ == "__main__":
    #输入知识文档文件夹路径  注意不是某个文件路径  将会一次性处理文件夹中所有知识文档
    in_dir_path = f"./data/in/new"
    url = get_url(in_dir_path)
    