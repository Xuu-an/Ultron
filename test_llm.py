import os
from dotenv import load_dotenv
from evolve.llm_driver import get_llm_driver

def test_llm_connection():
    # 加载环境变量
    load_dotenv()
    
    # 获取Azure OpenAI驱动
    driver = get_llm_driver("azure")
    
    if not driver:
        print("❌ 无法创建LLM驱动，请检查环境变量配置")
        return
    
    # 测试分析功能
    test_prompt = "请分析这段代码的功能"
    test_code = "def hello(): print('Hello, World!')"
    
    try:
        result = driver.analyze(test_prompt, test_code)
        if "error" in result:
            print(f"❌ LLM分析失败: {result['error']}")
        else:
            print("✅ LLM分析成功")
            print(f"分析结果: {result['analysis']}")
            
        # 测试生成功能
        test_context = {"description": "生成一个简单的Hello World函数"}
        generated_code = driver.generate("请生成代码", test_context)
        if generated_code and not generated_code.startswith("生成失败"):
            print("✅ LLM生成成功")
            print(f"生成的代码: {generated_code}")
        else:
            print(f"❌ LLM生成失败: {generated_code}")
            
    except Exception as e:
        print(f"❌ LLM测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    test_llm_connection() 