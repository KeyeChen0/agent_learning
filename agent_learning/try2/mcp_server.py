# MCP 服务：把 Skill 暴露成远程服务
from mcp.server import FastMCP
from skills.calculator.skill import calculator

mcp = FastMCP("calculator-service")

# 直接把 Skill 注册成 MCP 工具
@mcp.tool()
def calculate(expression: str) -> str:
    return calculator(expression)

if __name__ == "__main__":
    mcp.run()