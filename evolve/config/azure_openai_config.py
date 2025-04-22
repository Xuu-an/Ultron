from typing import Dict
import os

class AzureOpenAIConfig:
    """Azure OpenAI 配置类"""
    
    def __init__(self):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_base = os.getenv("AZURE_OPENAI_API_BASE")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
    def validate(self) -> bool:
        """验证配置是否完整"""
        required_fields = [
            ("api_key", self.api_key),
            ("api_base", self.api_base),
            ("deployment_name", self.deployment_name)
        ]
        
        missing_fields = [name for name, value in required_fields if not value]
        if missing_fields:
            print(f"缺失的配置项: {', '.join(missing_fields)}")
            return False
        return True
        
    def get_config(self) -> Dict:
        """获取配置字典"""
        return {
            "api_key": self.api_key,
            "api_base": self.api_base,
            "api_version": self.api_version,
            "deployment_name": self.deployment_name
        } 