import os
import json
import random
import argparse

from tqdm import tqdm
from model_api import Model_API
from generate_prompt import kct_prompt_0, qdp_prompt_0, qa_prompt_0, qg_prompt_1

def data_loader(folder_path):
    all_data = {}
    for file in os.listdir(folder_path):
        subject = file.split('.')[0]
        all_data[subject] = []
        with open(os.path.join(folder_path, file), 'r') as f:
            for line in f:
                all_data[subject].append(json.loads(line))
    return all_data

def kct_task(data_folder, model, shot_type, output_folder):

    test_data = data_loader(data_folder)

    for subject, data in tqdm(test_data.items()):
        output = []

        for item in tqdm(data):
            ques_subject = subject
            ques_knowledges, ques_content = item['ques_knowledges'], item['ques_content']
            ques_ans = f"题目答案: {item['ques_ans']}"
            ques_analyze = f"题目解析: {item['ques_analyze']}"
            rag_knowledges = item["ques_rag_knowledges"]

            
            target_ans = [rag_knowledges.index(k) + 1 for k in ques_knowledges]
            knowledge_set_str = " ".join("{}.{}".format(i+1, k) for i, k in enumerate(rag_knowledges))

            if shot_type == "zero":
                prompt = kct_prompt_0(ques_subject, ques_content, ques_ans, ques_analyze, knowledge_set_str)
            
            predict_ans = model.model_predict(prompt)
            
            output.append({
                "ques_id": item['id'],
                "target": target_ans,
                "predict": predict_ans
            })

            output_path = os.path.join(output_folder, f"{subject}_output.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)

    return output

def qdp_task(data_folder, model, shot_type, output_folder):
    
    test_data = data_loader(data_folder)

    for subject, data in tqdm(test_data.items()):
        output = []

        for item in tqdm(data):
            if item["id"] in evaluated_ids:
                continue
            ques_subject = subject
            ques_content = item['ques_content']
            ques_ans = f"题目答案: {item['ques_ans']}"
            ques_analyze = f"题目解析: {item['ques_analyze']}"
            target_ans = item['ques_difficulty']

            if shot_type == "zero":
                prompt = qdp_prompt_0(ques_subject, ques_content, ques_ans, ques_analyze)

            predict_ans = model.model_predict(prompt)

            output.append({
                "ques_id": item['id'],
                "target": target_ans,
                "predict": predict_ans
            })

            output_path = os.path.join(output_folder, f"{subject}_output.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)

    return output

def qa_task(data_folder, model, shot_type, output_folder):
    test_data = data_loader(data_folder)
    choice_types = ["选择题", "单选题", "多选题", "单项选择", "词汇选择题", "阅读单选", "单项选择题"]
    pan_types = ["判断题", "阅读判断"]
    other_types = ["填空题", "简答题", "计算题", "解答题", "现代文阅读", "诗歌鉴赏"]

    for subject, data in tqdm(test_data.items()):
        output = []
        for item in tqdm(data):

            ques_subject = subject
            ques_type = item['ques_type']
            ques_content = item['ques_content']
            ques_ans = item['structured_answer']

            if ques_type in choice_types:
                ques_type_num = 0
            elif ques_type in pan_types:
                ques_type_num = 1
            else:
                ques_type_num = 2
            prompt = qa_prompt_0(ques_subject, ques_type, ques_content)

            predict_str = model.model_predict(prompt)

            output.append({
                "ques_id": item['ques_id'],
                "ques_type": ques_type_num,
                "target": ques_ans,
                "predict": predict_str
            })

            output_path = os.path.join(output_folder, f"{subject}_output.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)

    return output

def qg_task(data_folder, model, shot_type, output_folder):
    
    test_data = data_loader(data_folder)

    for subject, data in tqdm(test_data.items()):
        output = []

        def shot_generate(item):
            ques_subject = item['subject']
            ques_content = item['ques_content'][5:]
            ques_ans = item['ques_ans']
            ques_knowledges = item['ques_knowledges']
            ques_analyze = item['ques_analyze']
            ques_difficulty = item["update_difficulty"]
            knowledge_set_str = " ".join("{}.{}".format(i+1, k) for i, k in enumerate(rag_knowledges))
            target_str = json.dumps({"题目内容": ques_content, "题目答案": ques_ans, "题目解析": ques_analyze}, ensure_ascii=False)

            shot_str = "输入:\n题目学科:{}\n题目类型:{}\n题目知识点:{}\n题目难度:{}\n\n输出:\n{}".format(ques_subject, ques_type, knowledge_set_str, ques_difficulty, target_str)
            return shot_str
        
        for item in tqdm(data):

            ques_subject = subject
            ques_type = item['ques_type']
            ques_difficulty = item['update_difficulty']
            ques_knowledges = item['ques_knowledges']
            ques_knowledges_str = " ".join("{}.{}".format(i+1, k) for i, k in enumerate(ques_knowledges))
            shot_str = shot_generate(item)
            prompt = qg_prompt_1(ques_subject, ques_knowledges_str, ques_difficulty, ques_type, shot_str)
            
            predict_str = model.model_predict(prompt)

            output.append({
                "ques_id": item['id'],
                "ques_type": ques_type,
                "ques_difficulty": ques_difficulty,
                "ques_knowledges": ques_knowledges_str,
                "predict": predict_str
            })

            output_path = os.path.join(output_folder, f"{subject}_output.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
    
    return output

def run(args):
    model = Model_API(args.model_name)
    data_folder = os.path.join(args.input_path, args.data_type)
    task_folder = os.path.join(args.output_path, args.task_type)
    shot_folder = os.path.join(task_folder, args.shot_type)
    if not os.path.exists(task_folder):
        os.makedirs(task_folder)
    if not os.path.exists(shot_folder):
        os.makedirs(shot_folder)
    if args.task_type == "knowledge_predict":
        kct_task(data_folder, model, args.shot_type, shot_folder)
    elif args.task_type == "difficulty_predict":
        qdp_task(data_folder, model, args.shot_type, shot_folder)
    elif args.task_type == "question_answer_predict":
        qa_task(data_folder, model, args.shot_type, shot_folder)
    elif args.task_type == "question_generation_predict":
        qg_task(data_folder, model, args.shot_type, shot_folder)
    
args = parse_args()
run(args)