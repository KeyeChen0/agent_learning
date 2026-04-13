def calculator(expression: str) -> str:
    """安全计算器：支持 +-*/%**() 运算"""
    try:
        # 白名单：只允许数字、运算符、括号
        allowed_chars = "0123456789+-*/%(). "
        for char in expression:
            if char not in allowed_chars:
                return "计算错误：包含非法字符"
        
        # 安全计算（限制数学表达式）
        result = eval(expression, {"__builtins__": None}, {})
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{str(e)}"