from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from utils.get_split_contents import get_data_list
from utils.chain import get_chain
from utils.openai_token_count import count_openai_tokens
import asyncio
import json
import re
from tqdm.asyncio import tqdm_asyncio,tqdm

df = pd.DataFrame(columns=['试题类型','难度','标签','题干','镜像题干','分数','问题解释','答案','可选','选项A','选项B','选项C','选项D'])
num = 0
total_fee = 0

def get_question(json_str, question_df,name):
    pattern = r'\{"question":"[^"]+","options":\{[^}]+\},"answer":"[A-D]","difficulty":"[^"]+"\}'
    try: 
        modify_json_str = json_str.replace('\n','').replace(' ','')
        modify_json_str = modify_json_str.split('[')[-1].split(']')[0]
        list = modify_json_str.split('}')
        list[-1] = ''
        modify_json_str =  '}'.join(list)
        modify_json_str = modify_json_str.replace(modify_json_str.split('{')[0],'')
        #modify_json_str = f'[{modify_json_str}]'
        json_obj = [json.loads(i) for i in re.findall(pattern, modify_json_str)]
    except:
        print('正则匹配解析错误: \n'+modify_json_str)
        return question_df
    for item in json_obj:
        try:
            raw_question = item['question']
            difficulty = item['difficulty']
            options = item['options']
            option_num = len(options.keys())
            if option_num == 2:
                option_a = item['options']['A']
                option_b = item['options']['B']
                option_c = ''
                option_d = ''
            if option_num == 3:
                option_a = item['options']['A']
                option_b = item['options']['B']
                option_c = item['options']['C']
                option_d = ''
            if option_num == 4:                       
                option_a = item['options']['A']
                option_b = item['options']['B']
                option_c = item['options']['C']
                option_d = item['options']['D']
            answer = item['answer']
        except:
            print('error choices:'+item.__str__())
            continue
        if len(answer) > 1:
            question_type = '多选题'
        else:
            question_type = '单选题'
        question_df.loc[len(question_df)] = [f'{question_type}',f'{difficulty}',f'AI试题|{name}',raw_question,'','1','',answer,'', option_a, option_b, option_c, option_d]
    return question_df

def get_question_csv_from_content(task_type, content, name):
    chain = get_chain(task_type)
    total_fee = 0
    question_df = pd.DataFrame(columns=['试题类型','难度','标签','题干','镜像题干','分数','问题解释','答案','可选','选项A','选项B','选项C','选项D'])
    if len(content) <= 50:
        MAX_ITERATION = 1
        MIN_QUESTIONS = 1
    elif len(content) > 50 and len(content) <= 100:
        MAX_ITERATION = 2
        MIN_QUESTIONS = 2
    elif len(content) > 100 and len(content) <= 300:
        MAX_ITERATION = 2
        MIN_QUESTIONS = 5
    elif len(content) > 300 and len(content) <= 500:
        MAX_ITERATION = 2  
        MIN_QUESTIONS = 8
    elif len(content) > 500:
        MAX_ITERATION = 3  
        MIN_QUESTIONS = 10

    iteration = 0
    question_num = 0
    question_list=[]

    while iteration <= MAX_ITERATION and question_num < MIN_QUESTIONS:
        question_list=question_df["题干"].tolist()
        if question_list:
            question_list_str= '\n'.join(question_list)
        else:
            question_list_str=''
        #print('---------------------existed questions:',question_list_str)
        question = chain.invoke({"new_content": content,"existed_question" : question_list_str,'question_num':MIN_QUESTIONS})
        try:
            total_fee = count_openai_tokens(content)/1000*0.01+count_openai_tokens(question)/1000*0.03
        except:
            total_fee = 0
        try:
            question_df = get_question(question,question_df,name)
            question_df = question_df.drop_duplicates(subset='题干')
        except:
            iteration += 1
            continue
        question_num = len(question_df["题干"])
        iteration += 1
    return question_df, total_fee

async def async_get_questions(task_type, content, name):
    global df
    global num
    global total_fee
    loop = asyncio.get_event_loop()
    middle_df,fee = await loop.run_in_executor(None,get_question_csv_from_content,task_type, content ,name)
    df = pd.concat([df,middle_df])
    num = num + 1
    total_fee = total_fee + fee
    
async def async_main(task_type, to_evaluate_texts, name):
    tasks=[async_get_questions(task_type,content,name) for content in to_evaluate_texts]
    await tqdm_asyncio.gather(*tasks, desc = name)


def get_question_csv_from_knowledgefile_path(task_type, raw_fp, name):
    global df
    global num
    global total_fee
    with open(raw_fp, 'r',encoding = 'utf8') as f:
        content = f.read()
    to_evaluate_texts = get_data_list(content)
    asyncio.run(async_main(task_type, to_evaluate_texts, name))
    #print("dataframe如下：\n", df)
    print(f'总费用：{total_fee*7}元')
    return total_fee,df