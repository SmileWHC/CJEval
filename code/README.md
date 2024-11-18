
### README.md for CJEval Code

#### Overview
This repository contains the code for the CJEval project, which includes utilities for evaluating and running machine learning tasks related to education. Here you will find scripts to generate prompts, run tasks, and evaluate results using a predefined model API.

#### Files Description
- `evaluation.py`: Script for evaluating the performance of models based on specified metrics.
- `run_task.py`: Main executable script to run tasks specified in the command line arguments.
- `generate_prompt.py`: Utility to generate prompts that are used as input for models.
- `model_api.py`: Defines the API interactions with the model, handling requests and responses.

#### Prerequisites
- Python 3.8 or above

#### Usage
To run the evaluation script, use:
```
python evaluation.py
```

To run a specific task, use:
```
python run_task.py <task-name>
```

#### Detailed Usage of `run_task.py`
- **Functionality**: Handles multiple educational tasks such as knowledge point prediction, question difficulty prediction, answer generation, and question generation.
- **Data Loading**: Loads data from specified directory and processes JSON formatted files.
- **Tasks**: Includes functions like `kct_task`, `qdp_task`, `qa_task`, `qg_task` for various prediction and generation tasks.
- **Command Line Arguments**:
  - `model_name`: Name of the model to use.
  - `input_path`: Path where input data is located.
  - `data_type`: Type of data to process.
  - `output_path`: Path where outputs should be saved.
  - `task_type`: Type of task to perform.
  - `shot_type`: Specifies the shot type like zero-shot or few-shot.
- **Execution**: Parses command line arguments and processes data based on the task type using the specified model.
