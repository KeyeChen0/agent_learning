from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# 加载环境
load_dotenv(override=True)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)
model = "qwen3.5-flash"

# 加载 Skill
with open("skills/calculator/skill.json", encoding="utf-8") as f:
    tool_def = json.load(f)
tools = [{"type": "function", "function": tool_def}]

# 导入 Skill 函数
from skills.calculator.skill import calculator

def agent_skill(query):
    messages = [
        {"role": "system", "content": "你是一个智能助手，必须使用工具计算，不能自己算。"},
        {"role": "user", "content": query}
    ]

    # ====================== 核心：循环 ======================
    max_round = 5  # 最多调用5次工具，防止死循环
    for _ in range(max_round):
        # 1. 调用 LLM
        response = client.chat.completions.create(
            model=model, messages=messages, tools=tools, tool_choice="auto"
        )
        msg = response.choices[0].message

        # 2. 如果 LLM 不需要工具 → 直接返回最终回答
        if not msg.tool_calls:
            return msg.content

        # 3. 如果需要工具 → 执行
        print(f"\n🤖 调用工具")
        call = msg.tool_calls[0]
        args = json.loads(call.function.arguments)
        result = calculator(args["expression"])
        print(f"✅ 工具结果：{result}")

        # 4. 把工具结果加回对话
        messages.append(msg)
        messages.append({
            "role": "tool",
            "content": result,
            "tool_call_id": call.id
        })

    # 超过轮次
    return "已达到最大工具调用次数"

# 测试
if __name__ == "__main__":
    q = "3的5次方是多少？再加20等于多少？"
    print("回答：", agent_skill(q))