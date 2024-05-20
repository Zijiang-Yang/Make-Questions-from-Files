import oss2
import os


auth = oss2.Auth(os.getenv("ACCESS_KEY_ID"), os.getenv("ACCESS_KEY_SECRET"))
oss_bucket = oss2.Bucket(auth, os.getenv('ENDPONIT'), os.getenv('OSS_BUCKET_NAME'))


def upload_file(task_type, date_str, file_name):
    local_file_path = os.path.join(f"./data/out/{date_str}", f"{file_name}.csv")
    oss_bucket_path = os.path.join('give_exam_questions', task_type, date_str, f"{file_name}.csv")
    oss_bucket.put_object_from_file(oss_bucket_path, local_file_path)
    url = f"https://{os.getenv('OSS_BUCKET_NAME')}.{os.getenv('ENDPONIT')}/{oss_bucket_path}"
    print("-----------------------------------\n已上传文件的URL：", url,'\n')
    return url