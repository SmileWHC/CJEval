# CJEval: A Benchmark for Assessing Large Language Models Using Chinese Junior High School Exam Data

## Introduction
CJEval is a benchmark based on Chinese Junior High School Exam Evaluations. It consists of 26,136 samples across four application-level educational tasks covering ten subjects. These samples include not only questions and answers but also detailed annotations such as question types, difficulty levels, knowledge concepts, and answer explanations.

## Dataset Statistics
**Table: Overall statistics of CJEval.**
|                   | **SCQs** | **MRQs** | **TFQs** | **FBQs** | **AQs** |
|-------------------|----------|----------|----------|----------|---------|
| **No.S**          | 10       | 5        | 5        | 9        | 7       |
| **No.Q**          | 7,701    | 2,569    | 3,729    | 6,193    | 5,944   |
| **Avg.Q Tokens**  | 112.8    | 211.7    | 102.1    | 107.1    | 376.9   |
| **Avg.A Tokens**  | 1        | 2.65     | 1.35     | 22.6     | 73.3    |
| **Avg.AE Tokens** | 232.8    | 313.9    | 211.8    | 241.6    | 372.7   |
| **Avg.No.KC**     | 2.4      | 2.7      | 2.7      | 2.4      | 2.6     |

 S: Subject. Q: Question. KC: Knowledge Concept. AE: Answer Explanation. Here, No.S represents the number of accounts covered under the corresponding question type. Avg.No.KC represents the average number of knowledge concepts associated with each question. Regarding dataset segmentation, the train set, valid set, test set and total set consist of 20,820, 2,106, 3,210 and 26,136 questions, respectively.

**Showcase:**
```
{"subject": "初中生物", "ques_type": "单选题", "ques_difficulty": "一般",
 "ques_content": "在下列生物中，哪个具有完整的细胞核？ (     )
选项: A. 酵母菌 B. 肝炎病毒 C. 乳酸菌 D. 大肠杆菌", 
"ques_answer": ["A"], 
"ques_analyze": "此题考查不同生物的细胞结构特点。 
A. 酵母菌是属于真菌类的生物，真菌细胞具有成形的细胞核，因此选项A正确。 
B. 肝炎病毒没有细胞结构，是非细胞生物，不具备成形的细胞核，所以选项B错误。 
C. 乳酸菌属于细菌类，细菌细胞没有成形的细胞核，所以选项C错误。 
D. 大肠杆菌也是细菌类，同样无成形细胞核，因此选项D错误。 通过上述分析，确定选项A为正确答案。
理解病毒、细菌和真菌在细胞结构上的区别是解答此类题目的关键。", 
"ques_knowledges": ["细菌和真菌的区别", "病毒的结构特征"]}
```

## Benchmarks

**Table: The overall results of the four question-based tasks under zero-shot settings are summarized below.**

<img src="https://github.com/SmileWHC/CJEval/blob/main/src/overall_results.png" width="860" />

## Deployment

See code/README.md .

## Ethics

CJEval is derived from actual junior high school test questions, which have been meticulously rewritten and scrutinized. The CJEval dataset is intended solely for academic and research purposes. Commercial use or any misuse that deviates from these intended purposes is strictly prohibited. 

Adhering to these guidelines is essential to maintain the dataset's integrity and ensure ethical use.

## Citation
CJEval: A Benchmark for Assessing Large Language Models Using Chinese Junior High School Exam Data

https://arxiv.org/abs/2409.16202

 If you find our projects helpful to your research, please consider citing it:
```
@article{zhang2024cjeval,
      title={CJEval: A Benchmark for Assessing Large Language Models Using Chinese Junior High School Exam Data}, 
      author={Qian-Wen Zhang and Haochen Wang and Fang Li and Siyu An and Lingfeng Qiao and Liangcai Gao and Di Yin and Xing Sun},
      year={2024},
      eprint={2409.16202},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
}
```