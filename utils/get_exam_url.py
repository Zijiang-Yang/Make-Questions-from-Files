import os
import glob
from tqdm import tqdm
from datetime import datetime
from utils.cleaning import filename_cleaning
from utils.upload_db import upload_file
from utils.async_get_questions import get_question_csv_from_knowledgefile_path
from dotenv import load_dotenv
load_dotenv()

def get_url(in_dir_path: str):
    task_type = "chanpin"
    # 获取今天的日期
    date_str = datetime.today().strftime('%Y%m%d')
    #输出csv文件保存文件夹路径（不用手动设置）data/out/async/{当天日期}
    out_dir_path = f"data/out/{date_str}"
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)

    markdown_file_paths = glob.glob(in_dir_path + "/**/*.md", recursive=True)
    return_url=''
    total_fee = 0
    for file_path in tqdm(markdown_file_paths,desc = "文件夹进度",total=len(markdown_file_paths)):
        file_name = filename_cleaning(os.path.basename(file_path).split('.')[0])
        try:
            fee, df = get_question_csv_from_knowledgefile_path(task_type, file_path, file_name)
            out_file_path = os.path.join(out_dir_path, f"{file_name}.csv")
            if not os.path.exists(out_file_path):
                # 创建输出文件路径的目录
                os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
            df = df.drop_duplicates(subset='题干')
            df.to_csv(out_file_path, encoding='utf8', index=False)
            url = upload_file(task_type, date_str, file_name)
            oss_bucket_path = os.path.join('give_exam_questions', task_type, date_str, f"{file_name}.csv")
            url = f"https://{os.getenv('OSS_BUCKET_NAME')}.{os.getenv('ENDPONIT')}/{oss_bucket_path}"
            total_fee = total_fee + fee
            print(f'{file_name} 试题生成完成, total_fee: {total_fee*7}元')
        except Exception as e:
            print(e)
            print(f'!!!!!!!!!! fail{file_name} fail!!!!!!!!!!!')