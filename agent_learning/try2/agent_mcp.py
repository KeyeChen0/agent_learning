from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from mcp.client import MCPClient

load_dotenv(override=True)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)
model = "qwen3.5-flash"

async def agent_mcp(query):
    # 连接 MCP 服务
    mcp = MCPClient()
    await mcp.connect(stdio_server=("python", ["mcp_server.py"]))

    # 自动获取工具（无需手动写 JSON！）
    tools = await mcp.list_tools()

    messages = [
        {"role": "system", "content": "必须使用工具计算"},
        {"role": "user", "content": query}
    ]

    res = client.chat.completions.create(model=model, messages=messages, tools=tools)
    msg = res.choices[0].message

    if msg.tool_calls:
        call = msg.tool_calls[0]
        args = json.loads(call.function.arguments)

        # 关键：通过 MCP 远程调用
        tool_result = await mcp.call_tool(
            tool_name=call.function.name,
            arguments=args
        )

        messages.append(msg)
        messages.append({
            "role": "tool",
            "content": tool_result.content[0].text,
            "tool_call_id": call.id
        })

        final = client.chat.completions.create(model=model, messages=messages)
        await mcp.close()
        return final.choices[0].message.content

    await mcp.close()
    return msg.content

# 测试
if __name__ == "__main__":
    import asyncio
    q = "3的5次方是多少？再加20等于多少？"
    print("回答：", asyncio.run(agent_mcp(q)))