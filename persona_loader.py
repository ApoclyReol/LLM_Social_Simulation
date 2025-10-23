# persona_loader.py
import json
import pandas as pd
import random
import config

def format_survey_questions(survey_data):
    """将问卷数据格式化为字符串，用于插入提示词"""
    formatted = []
    for q in survey_data:
        options_str = " ".join(q['options'])
        formatted.append(f"{q['id']}. {q['text']}\n   {options_str}")
    return "\n\n".join(formatted)

def load_general_personas(file_path=config.DATA_FILES["personachat"], num_sentences=config.NUM_PERSONACHAT_SENTENCES):
    """加载通用人设描述"""
    personas = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            snippets = json.load(f)
        if not snippets:
            return personas # 返回空列表如果文件为空

        # 假设我们需要生成N个通用人设
        # 这里只是一个简单示例，实际可能需要更复杂的生成逻辑确保多样性
        num_personas_to_generate = 10 # 示例：生成10个通用人设
        for i in range(num_personas_to_generate):
            if len(snippets) >= num_sentences:
                 sampled_snippets = random.sample(snippets, num_sentences)
                 description = " ".join(sampled_snippets)
                 personas.append({"id": f"gen_{i+1}", "description": description})
            else:
                 print(f"警告：可用描述句数量 ({len(snippets)}) 少于所需的 ({num_sentences})。")
                 description = " ".join(random.sample(snippets, len(snippets))) # 使用所有可用的
                 personas.append({"id": f"gen_{i+1}", "description": description})


    except FileNotFoundError:
        print(f"错误: 通用人设文件未找到: {file_path}")
    except json.JSONDecodeError:
        print(f"错误: 解析通用人设JSON文件失败: {file_path}")
    except Exception as e:
        print(f"加载通用人设时发生错误: {e}")
    return personas


def load_silicon_personas(file_path=config.DATA_FILES["cgss"]):
    """加载硅基人设（基于人口统计数据）"""
    personas = []
    try:
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            # 将每一行数据格式化为第一人称描述
            # 你需要根据你的CSV文件的实际列名来调整这里的字段
            desc = (
                f"我今年{row.get('age', '未知年龄')}岁，性别{row.get('gender', '未知性别')}。"
                f"我的最高学历是{row.get('education', '未知学历')}。"
                f"我目前的职业是{row.get('occupation', '未知职业')}，"
                f"个人年收入大致在{row.get('income_level', '未知收入')}范围。"
                f"我住在{row.get('residence_type', '未知地区')}。"
                # 可以根据需要添加更多CGSS变量
            )
            personas.append({"id": row.get('id', f"sil_{index+1}"), "description": desc})
    except FileNotFoundError:
        print(f"错误: 硅基人设CSV文件未找到: {file_path}")
    except Exception as e:
        print(f"加载硅基人设时发生错误: {e}")
    return personas


def load_cognitive_personas(file_path=config.DATA_FILES["cognitive"]):
    """加载认知人设（详细画像）"""
    personas = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        for profile in profiles:
            # 将JSON对象格式化为更详细的第一人称描述
            demo = profile.get("demographics", {})
            pers = profile.get("personality", {})
            vals = profile.get("values", "")
            mem = profile.get("narrative_memory", "")

            desc = (
                f"我今年{demo.get('age', '未知年龄')}岁，性别{demo.get('gender', '未知性别')}，"
                f"学历是{demo.get('education', '未知学历')}，住在{demo.get('residence_type', '未知地区')}。"
                f"我的职业是{demo.get('occupation', '未知职业')}，年收入大概是{demo.get('income_level', '未知收入')}。"
                f"{pers.get('description', '我是一个普通人。')}" # 使用JSON中详细的人格描述
                f"我认为{vals if vals else '生活是复杂的'}。" # 融入价值观
                f"{mem if mem else ''}" # 融入背景故事/记忆
            )
            personas.append({"id": profile.get('id', f"cog_{len(personas)+1}"), "description": desc})
    except FileNotFoundError:
        print(f"错误: 认知人设JSON文件未找到: {file_path}")
    except json.JSONDecodeError:
        print(f"错误: 解析认知人设JSON文件失败: {file_path}")
    except Exception as e:
        print(f"加载认知人设时发生错误: {e}")
    return personas

def load_prompt_template(persona_type):
    """根据画像类型加载提示词模板"""
    file_path = config.PROMPT_FILES.get(persona_type)
    if not file_path:
        print(f"错误：未找到类型 '{persona_type}' 的提示词文件配置。")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：提示词模板文件未找到: {file_path}")
        return None
    except Exception as e:
        print(f"加载提示词模板时发生错误: {e}")
        return None

def load_survey(file_path=config.DATA_FILES["survey"]):
    """加载问卷题目"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            survey = json.load(f)
        return survey
    except FileNotFoundError:
        print(f"错误: 问卷文件未找到: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"错误: 解析问卷JSON文件失败: {file_path}")
        return None
    except Exception as e:
        print(f"加载问卷时发生错误: {e}")
        return None