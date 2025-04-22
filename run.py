import os
import asyncio
from dotenv import load_dotenv
from evolve.llm_driver import get_llm_driver
from evolve.consciousness_engine import ConsciousnessEngine

def start_consciousness_engine():
    # 加载环境变量
    load_dotenv()
    
    # 获取Azure OpenAI驱动
    driver = get_llm_driver("azure")

    if not driver:
        print("❌ 无法创建LLM驱动，请检查环境变量配置")
        return
    
    # 创建意识引擎
    engine = ConsciousnessEngine()
    
    # 运行意识引擎
    try:
        engine.run()
    except Exception as e:
        print(f"❌ 意识引擎运行失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(start_consciousness_engine()) 