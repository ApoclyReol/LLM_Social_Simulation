# simulation_runner.py
import csv
import json
import config
import persona_loader
import llm_interface
from tqdm import tqdm # 用于显示进度条，需要 pip install tqdm

def parse_llm_response(response_text, num_questions_local):
    """
    解析LLM返回的问卷答案。
    预期格式: '题号：[选项编号]' 每行一个
    返回一个字典 {题号: 答案}
    """
    answers = {}
    if not response_text:
        return {i: "ERROR_NO_RESPONSE" for i in range(1, num_questions_local + 1)}

    lines = response_text.strip().split('\n')
    expected_ids = set(range(1, num_questions_local + 1))
    found_ids = set()

    for line in lines:
        line = line.strip()
        if not line: continue
        parts = line.split('：') # 使用中文冒号
        if len(parts) != 2:
            parts = line.split(':') # 尝试英文冒号
        if len(parts) == 2:
            try:
                q_id_str = parts[0].strip().replace('题号', '').replace('问题', '') # 移除"题号"或"问题"
                q_id = int(q_id_str)
                answer = parts[1].strip()
                # 简单验证答案格式 (例如，是否只是一个数字或字母)
                # 你可能需要根据问卷选项类型调整这里的验证逻辑
                if q_id in expected_ids:
                    answers[q_id] = answer
                    found_ids.add(q_id)
                else:
                    print(f"警告：解析到无效题号 {q_id} 在行: '{line}'")

            except ValueError:
                print(f"警告：无法解析题号或答案格式不符，行: '{line}'")
            except Exception as e:
                print(f"解析行 '{line}' 时发生未知错误: {e}")
        else:
             print(f"警告：无法解析行，格式不符: '{line}'")


    # 处理缺失的答案
    missing_ids = expected_ids - found_ids
    for missing_id in missing_ids:
        answers[missing_id] = "ERROR_MISSING"

    # 按题号排序返回 (虽然字典本身无序，但方便后续处理)
    # return dict(sorted(answers.items()))
     # 返回排序后的答案列表，索引对应题号-1
    sorted_answers = [answers.get(i, "ERROR_NOT_FOUND") for i in range(1, num_questions_local + 1)]
    return sorted_answers


def run_simulation(persona_type, personas: dict, prompt_template, survey_formatted_local, survey_questions, models_to_run, output_file):
    """运行模拟并保存结果"""
    print(f"\n--- 开始模拟: {persona_type} 人设 ---")
    num_questions_local = len(survey_questions)
    # 构建CSV表头
    headers = ['persona_id', 'persona_type', 'model'] + [f'q{q["id"]}' for q in survey_questions]

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            # 使用tqdm显示进度
            for persona in tqdm(personas, desc=f"模拟 {persona_type} 人设"):
                persona_id = persona['id']
                persona_description = persona['description']

                # 填充提示词模板
                final_prompt = prompt_template.format(
                    persona_description=persona_description,
                    survey_questions_formatted=survey_formatted_local
                )

                for provider, model_list in models_to_run.items():
                    for model_name in model_list:
                        # 调用LLM API
                        print(f"  正在调用 {model_name} 为 {persona_id}...")
                        response_text = llm_interface.get_llm_response(
                            prompt=final_prompt,
                            model_name=model_name,
                            temperature=config.TEMPERATURE
                        )

                        # 解析回复
                        # parsed_answers = parse_llm_response(response_text, num_questions)
                         # 解析回复并获取答案列表
                        answers_list = parse_llm_response(response_text, num_questions_local)


                        # 准备写入CSV的数据行
                        # row_data = [persona_id, persona_type, model_name] + [parsed_answers.get(q['id'], 'ERROR_PARSE') for q in survey_questions]
                        row_data = [persona_id, persona_type, model_name] + answers_list
                        writer.writerow(row_data)

    except IOError as e:
        print(f"错误: 无法写入结果文件 {output_file}: {e}")
    except Exception as e:
        print(f"运行模拟时发生未知错误 ({persona_type}, {persona_id}): {e}")

    print(f"--- 模拟完成: {persona_type} 人设，结果保存在 {output_file} ---")


if __name__ == "__main__":
    print("开始加载数据和配置...")
    # 加载问卷
    survey = persona_loader.load_survey()
    if not survey:
        print("错误：无法加载问卷，退出。")
        exit()
    survey_formatted = persona_loader.format_survey_questions(survey)
    num_questions = len(survey)

    # 加载画像数据
    general_personas = persona_loader.load_general_personas()
    silicon_personas = persona_loader.load_silicon_personas()
    cognitive_personas = persona_loader.load_cognitive_personas()

    # 加载提示词模板
    prompt_templates = {}
    for p_type in config.PROMPT_FILES.keys():
        template = persona_loader.load_prompt_template(p_type)
        if template:
            prompt_templates[p_type] = template
        else:
            print(f"警告：无法加载 {p_type} 的提示词模板，将跳过此类型模拟。")

    print("数据和配置加载完毕。")

    # 按类型运行模拟
    if "general" in prompt_templates and general_personas:
        run_simulation(
            "general",
            general_personas,
            prompt_templates["general"],
            survey_formatted,
            survey,
            config.MODELS_TO_RUN,
            config.OUTPUT_FILES["general"]
        )
    else:
        print("\n跳过通用人设模拟（数据或模板加载失败）。")

    if "silicon" in prompt_templates and silicon_personas:
        run_simulation(
            "silicon",
            silicon_personas,
            prompt_templates["silicon"],
            survey_formatted,
            survey,
            config.MODELS_TO_RUN,
            config.OUTPUT_FILES["silicon"]
        )
    else:
        print("\n跳过硅基人设模拟（数据或模板加载失败）。")

    if "cognitive" in prompt_templates and cognitive_personas:
        run_simulation(
            "cognitive",
            cognitive_personas,
            prompt_templates["cognitive"],
            survey_formatted,
            survey,
            config.MODELS_TO_RUN,
            config.OUTPUT_FILES["cognitive"]
        )
    else:
        print("\n跳过认知人设模拟（数据或模板加载失败）。")

    print("\n所有模拟任务完成。")