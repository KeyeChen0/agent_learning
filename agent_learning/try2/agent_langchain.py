from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
# 🔥🔥🔥 LangChain 1.x 唯一正确的 Agent 导入（官方标准）
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

load_dotenv()

# 计算器工具（完全不变）
@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except:
        return "计算错误"

# LLM 配置（通义千问，不变）
llm = ChatOpenAI(
    model="qwen3.5-flash",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0
)

# 1.x 极简用法：直接创建Agent，内置执行器
agent = create_react_agent(llm, [calculator])

# 运行
if __name__ == "__main__":
    # 1.x 调用方式
    res = agent.invoke({
        "messages": [("user", "3的5次方是多少？再加20等于多少？")]
    })
    print("\n✅ 最终回答：", res["messages"][-1].content)