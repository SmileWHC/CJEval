import os
import re
import json
import time
import Levenshtein
from tqdm import tqdm
from generate_prompt import qa_evaluate_prompt, qg_evaluate_prompt

'''
Knowledge Concepts Predict Task Evaluation
data_folder: str, the folder path of the predict data
'''
def kct_evaluate(data_folder):
    evaluation_result = {}
    
    for file in tqdm(os.listdir(data_folder)):
        data_path = os.path.join(data_folder, file)
        subject = file.split('_')[0]

        with open(data_path, 'r') as f:
            predict_data = json.load(f)

        output_acc, output_recall, output_f1, total_num = 0, 0, 0, 0
        for item in predict_data:
            target, predict = item['target'], item['predict']

            # remove the comments in the predict result
            pattern = r'\{[^{}]*\}'
            match = re.search(pattern, predict)
            if match:
                predict = match.group(0)

            predict = predict.replace("'", '"')
            error_pattern = r'\/\/.*\n|\#.*\n'
            predict = re.sub(error_pattern, "", predict)

            # calculate the precision, recall and f1
            predict = json.loads(predict)
            key = next(iter(predict))
            predict = predict[key]

            intersection = set(target) & set(predict)
            precision = len(intersection) / len(predict) if predict else 0
            recall = len(intersection) / len(target) if target else 0
            f1 = 2 * (precision * recall) / (precision + recall) if precision + recall else 0

            output_acc += precision
            output_recall += recall
            output_f1 += f1
            total_num += 1

        evaluation_result[subject] = {
            "acc": round(output_acc * 100 / total_num, 2),
            "recall": round(output_recall * 100 / total_num, 2),
            "f1": round(output_f1 * 100 / total_num, 2)
        }

    avg_acc = sum([result['acc'] for subject, result in evaluation_result.items()]) / len(evaluation_result)
    avg_recall = sum([result['recall'] for subject, result in evaluation_result.items()]) / len(evaluation_result)
    avg_f1 = sum([result['f1'] for subject, result in evaluation_result.items()]) / len(evaluation_result)

    evaluation_result['avg'] = {
        "acc": round(avg_acc, 2),
        "recall": round(avg_recall, 2),
        "f1": round(avg_f1, 2)
    }

    return evaluation_result

def dp_evaluate(data_folder):

    output_result = {}
    difficulty_set = {"容易": 0, "较易": 1, "中等": 2, "较难": 3, "困难": 4}

    for file in tqdm(os.listdir(data_folder)):
        data_path = os.path.join(data_folder, file)
        subject = file.split('_')[0]

        with open(data_path, 'r') as f:
            predict_data = json.load(f)

        output_acc, total_num = 0, 0
        for item in predict_data:
            target, predict = item['target'], item['predict']

            # re search
            pattern = r'\{[^{}]*\}'
            match = re.search(pattern, predict)
            if match:
                predict = match.group(0)
            predict = predict.replace("\'", "\"")

            predict = json.loads(predict)
            key = list(predict.keys())[0]
            predict = predict[key]

            if abs(int(target) - difficulty_set[predict]) <= 1:
                output_acc += 1

            total_num += 1

        output_result[subject] = {
            "tacc": round(output_acc * 100 / total_num, 2)
        }

    avg_acc = sum([result['tacc'] for subject, result in output_result.items()]) / len(output_result)
    output_result['avg'] = {
        "tacc": round(avg_acc, 2)
    }

    return output_result

def qa_evaluate(data_folder):

    # load the AQs and FBQs evaluate result
    evaluate_folder = data_folder.replace("zero", "evaluate")
    evaluate_result = {}
    for file in os.listdir(evaluate_folder):
        data_path = os.path.join(evaluate_folder, file)
        with open(data_path, 'r') as f:
            predict_data = json.load(f)
        for item in predict_data:
            print(item["ques_id"])
            ques_id = int(item["ques_id"])
            result = item["result"]
            evaluate_result[ques_id] = result

    output = {"total_avg": {"SCQs": [0, 0], "MRQs": [0, 0], "TFQs": [0, 0], "FBQs": [0, 0], "AQs": [0, 0]}}

    for file in tqdm(os.listdir(data_folder)):
        output_result = {"SCQs": [0, 0], "MRQs": [0, 0], "TFQs": [0, 0], "FBQs": [0, 0], "AQs": [0, 0]}
        data_path = os.path.join(data_folder, file)
        subject = file.split('_')[0]

        with open(data_path, 'r') as f:
            predict_data = json.load(f)
        
        for question in predict_data:
            ques_id = question["ques_id"]
            ques_type = id_types[ques_id]
            acc_flag = False
            if ques_type in {"SCQs", "MRQs", "TFQs"}:
                target = question["target"]
                pattern = r'\{[^{}]*\}'
                
                # 合并字符串替换操作
                predict = question["predict"].replace("[\'", "[\"").replace("\']", "\"]").replace("\\n", "").replace("\n", "").replace("\\\"", "").replace('\\', "")
                
                match = re.search(pattern, predict)
                if match:
                    predict = match.group(0)
                predict = json.loads(predict)
                predict_ans = predict["答案结果"]
                
                # 合并并简化目标和预测答案处理
                target_s = "".join(ans.lower().strip() for ans in target)
                predict_s = "".join(ans.lower().strip() for ans in predict_ans)
                
                if sorted(target_s) == sorted(predict_s):
                    acc_flag = True
            elif ques_type in {"AQs", "FBQs"}:
                if evaluate_result[ques_id] == "正确":
                    acc_flag = True

            if acc_flag:
                output_result[ques_type][0] += 1
                output["total_avg"][ques_type][0] += 1

            output_result[ques_type][1] += 1
            output["total_avg"][ques_type][1] += 1

        output_result["avg"] = [sum([result[0] for result in output_result.values()]) / sum([result[1] for result in output_result.values()])]
        output[subject] = output_result

    output["total_avg"]["avg"] = [sum([result[0] for result in output["total_avg"].values()]) / sum([result[1] for result in output["total_avg"].values()])]
    return output

def qg_evaluate(data_folder):
    dif_total_acc, kno_total_acc, total_total_num = 0, 0, 0
    output = {}

    for file in tqdm(os.listdir(data_folder)):
        data_path = os.path.join(data_folder, file)
        subject = file.split('_')[0]

        dif_acc, kno_acc, total_num = 0, 0, 0
        with open(data_path, 'r') as f:
            predict_data = json.load(f)
        
        for item in predict_data:
            result = json.loads(item["evaluated"].replace("```json", "").replace("```", ""))
            if result["题目难度"] == "符合":
                dif_acc += 1
                dif_total_acc += 1
            if result["题目知识点"] == "符合":
                kno_acc += 1
                kno_total_acc += 1
            total_num += 1
            total_total_num += 1
        
        output[subject] = {
            "dif_acc": dif_acc / total_num,
            "kno_acc": kno_acc / total_num
        }
    
    output["total"] = {
        "dif_acc": dif_total_acc / total_total_num,
        "kno_acc": kno_total_acc / total_total_num
    }

    return output