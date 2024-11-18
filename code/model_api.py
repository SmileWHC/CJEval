import re
import time
import json
import requests
import random
import dashscope
import torch
from http import HTTPStatus
# from openai import OpenAI
from peft import AutoPeftModelForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel, LlamaTokenizer
from transformers.generation.utils import GenerationConfig
from vllm import LLM, SamplingParams
from gpt_utils import get_completion
from volcenginesdkarkruntime import Ark
import openai

class Model_API:
    def __init__(self, model_type="GPT-4"):
        self.model_type = model_type
        if self.model_type == "Qwen-14B-Chat":
            self.model = AutoModelForCausalLM.from_pretrained("./Models/Qwen-14B-Chat",
                device_map="auto",
                torch_dtype="auto",
                trust_remote_code=True).eval()
            self.tokenizer = AutoTokenizer.from_pretrained("./Models/Qwen-14B-Chat",
                trust_remote_code=True)
            self.model.generation_config = GenerationConfig.from_pretrained("./Models/Qwen-14B-Chat", trust_remote_code=True)
        elif self.model_type == "Baichuan2-13B-Chat":
            self.model = AutoModelForCausalLM.from_pretrained("./Models/Baichuan2-13B-Chat",
                revision="v2.0",
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True)
            self.tokenizer = AutoTokenizer.from_pretrained("./Models/Baichuan2-13B-Chat",
                revision="v2.0",
                use_fast=False,
                trust_remote_code=True)
            self.model.generation_config = GenerationConfig.from_pretrained("./Models/Baichuan2-13B-Chat", revision="v2.0")
        elif self.model_type == "GLM4-9B-Chat":
            self.tokenizer = AutoTokenizer.from_pretrained("./Models/GLM4-9B-Chat/ZhipuAI/glm-4-9b-chat",trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                "./Models/GLM4-9B-Chat/ZhipuAI/glm-4-9b-chat",
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                trust_remote_code=True
            ).to("cuda").eval()
        elif self.model_type == "Llama-3-8B-Instruct":
            self.model = AutoModelForCausalLM.from_pretrained("./Models/Llama-3-8B-Instruct",
                device_map="auto",
                torch_dtype="auto")
            self.tokenizer = AutoTokenizer.from_pretrained("./Models/Llama-3-8B-Instruct")
    
    def model_predict(self, text_prompt):
        if self.model_type == "Baichuan2-13B-Chat":
            messages = []
            messages.append({"role": "user", "content": text_prompt})
            response = self.model.chat(self.tokenizer, messages)
        elif self.model_type == "Qwen-14B-Chat" or self.model_type == "Qwen-14B-Chat-Lora":
            response, history = self.model.chat(self.tokenizer, text_prompt, history=None)
        elif self.model_type == "Llama-3-8B-Instruct":
            messages = [
                {"role": "user", "content": text_prompt}
            ]
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.model.device)

            terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            outputs = self.model.generate(
                input_ids,
                max_new_tokens=256,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response = outputs[0][input_ids.shape[-1]:]
            response = self.tokenizer.decode(response, skip_special_tokens=True)
        elif self.model_type == "GLM4-9B-Chat":
            gen_kwargs = {"max_length": 8192, "do_sample": True, "top_k": 1}
            inputs = self.tokenizer.apply_chat_template([{"role": "user", "content": text_prompt}],
                                    add_generation_prompt=True,
                                    tokenize=True,
                                    return_tensors="pt",
                                    return_dict=True
                                    )
            inputs = inputs.to("cuda")
            with torch.no_grad():
                outputs = self.model.generate(**inputs, **gen_kwargs)
                outputs = outputs[:, inputs['input_ids'].shape[1]:]
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        elif self.model_type == "GPT-3.5" or "GPT-4":
            openai.api_type = ""
            openai.api_base = "" #can repalce with the above api base
            openai.api_version = "" #change to "2022-12-01" if using chatgpt
            openai.api_key = ""  #can replace with above api key
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",                                            #can replace with "gpt-4-32k" or "gpt-35-turbo"
                messages=[
                            {"role": "user", "content": text_prompt},
                        ],
                temperature=0.7,
                max_tokens=4096,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None)
            response = response['choices'][0]['message']['content']
        return response