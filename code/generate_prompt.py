import os
import json

def kct_prompt_0(ques_subject, ques_content, ques_ans, ques_analyze, subject_knowledge_s):
    prompt = """
### 任务设定：
你是知识渊博的初中辅导老师，需要根据题目信息，预测题目涉及的知识点。
输入为 题目学科、题目内容、题目答案、题目解析以及该学科带有编号的的所有知识点
输出格式要求为json, 答案结果要求为一个列表，列表中的元素为题目涉及的知识点编号，json格式要求: {{"知识点序号": [1, 2, 3]}}

### 输入：
题目学科: {}
{}
{}
{}
科目知识点：{}

### 输出：
""".format(ques_subject, ques_content, ques_ans, ques_analyze, subject_knowledge_s)
    return prompt

def dp_prompt_0(ques_subject, ques_content, ques_ans, ques_analyze):
    prompt = """
### 任务设定：
你是知识渊博的初中辅导老师，需要根据题目信息，判断题目难度。
题目信息的输入包括 题目学科、题目内容、题目答案、题目解析
可以根据内容复杂度、题目类型、解题步骤数量、知识点数目和知识点难度等多方面因素进行判断
题目难度集合包括："容易, 较易, 一般, 较难, 困难"
输出格式要求为json, 题目难度为题目难度集合中的一个, json格式要求: {{"题目难度": "xx"}}

### 输入：
题目学科：{}
{}
{}
{}

### 输出：
""".format(ques_difficulty, ques_subject, ques_content, ques_ans, ques_analyze)
    return prompt

def qa_prompt_0(ques_subject, ques_content, ques_ans, ques_analyze):
    prompt = """
### 任务设定：
你是知识渊博的初中辅导老师，给你提供题目学科、题目类型和题目内容，需要你按照格式输出答案
思考后，给出答案结果
输出格式要求为json, 每个小题的答案用（1）（2）表示，json格式要求: {{"答案结果": "（1）xxx （2）xxx"}}

### 输入
题目学科：{}
题目类型：{}
{}

### 输出
""".format(ques_subject, ques_type, ques_content)
    return prompt

def qg_prompt_1(ques_difficulty, ques_knowledges, ques_info):
    prompt = """ 任务设定：
你是知识渊博的初中辅导老师，给你提供一道题目，请根据题目的内容、答案和解析来判断题目难度是否符合要求，以及题目是否涉及并涵盖了所有知识点
输出格式要求为json，示例：{{"题目难度":"XX", "题目知识点":"XX"}}，只可以输出符合或不符合

### 输入：
要求：
难度要求：{}
知识点要求：{}

题目信息：
{}

### 输出：
""".format(ques_difficulty, ques_knowledges, ques_info)
    return prompt

def qa_evaluate_prompt(target, predict):
    prompt = """
### 任务设定：
你是知识渊博的初中辅导老师，现在给你多道题目的正确答案和学生的答案和解析过程，需要你判断学生的答案是否正确
输入为每道题目的id、正确答案、学生答案
输出格式为json, json格式要求: {{"题目id1": "XX", "题目id2": "XX"}}, 只有正确和不正确两种情况

### 输入：
正确答案：{}
学生答案：{}

### 输出：
""".format(target, predict)
    return prompt

def qg_evaluate_prompt(ques_difficulty, ques_knowledges, ques_info):
    prompt = """ 任务设定：
你是知识渊博的初中辅导老师，给你提供一道题目，请根据题目的内容、答案和解析来判断题目难度是否符合要求，以及题目是否涉及并涵盖了所有知识点
输出格式要求为json，示例：{{"题目难度":"XX", "题目知识点":"XX"}}，只可以输出符合或不符合

### 输入：
要求：
难度要求：{}
知识点要求：{}

题目信息：
{}

### 输出：
""".format(ques_difficulty, ques_knowledges, ques_info)
    return prompt