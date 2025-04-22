import os
from pathlib import Path
from typing import Dict, Optional
from .logger import Logger

class PersonaManager:
    def __init__(self):
        self.logger = Logger()
        self.prompts_dir = Path("evolve/prompts")
        self.prompts_cache: Dict[str, str] = {}
        self._load_all_prompts()

    def _load_all_prompts(self) -> None:
        """加载所有提示词文件到缓存"""
        try:
            if not self.prompts_dir.exists():
                self.logger.error(f"Prompts directory not found: {self.prompts_dir}")
                return

            for prompt_file in self.prompts_dir.glob("*.txt"):
                persona_name = prompt_file.stem
                try:
                    with open(prompt_file, 'r', encoding='utf-8') as f:
                        self.prompts_cache[persona_name] = f.read()
                    self.logger.debug(f"Loaded prompt for persona: {persona_name}")
                except Exception as e:
                    self.logger.error(f"Failed to load prompt file {prompt_file}: {e}")
        except Exception as e:
            self.logger.error(f"Failed to load prompts: {e}")

    def get_prompt(self, persona_name: str) -> Optional[str]:
        """获取指定人格的提示词"""
        try:
            prompt = self.prompts_cache.get(persona_name)
            if prompt is None:
                self.logger.warning(f"Prompt not found for persona: {persona_name}")
            return prompt
        except Exception as e:
            self.logger.error(f"Failed to get prompt for {persona_name}: {e}")
            return None

    def reload_prompts(self) -> None:
        """重新加载所有提示词"""
        try:
            self.prompts_cache.clear()
            self._load_all_prompts()
            self.logger.info("Reloaded all prompts")
        except Exception as e:
            self.logger.error(f"Failed to reload prompts: {e}")

    def list_available_personas(self) -> list[str]:
        """获取所有可用的人格列表"""
        return list(self.prompts_cache.keys())

    def get_prompt_template(self, persona_name: str, template_type: str) -> Optional[str]:
        """获取指定人格的特定模板类型提示词"""
        try:
            prompt = self.get_prompt(persona_name)
            if prompt is None:
                return None

            # 从提示词中提取特定模板
            # 这里假设模板以 ## 模板类型 开头
            template_start = f"## {template_type}"
            if template_start not in prompt:
                self.logger.warning(f"Template type '{template_type}' not found in {persona_name} prompt")
                return None

            # 提取模板内容
            template_content = prompt.split(template_start)[1]
            # 找到下一个 ## 开头的部分作为结束
            next_section = template_content.find("\n##")
            if next_section != -1:
                template_content = template_content[:next_section]

            return template_content.strip()
        except Exception as e:
            self.logger.error(f"Failed to get template for {persona_name} ({template_type}): {e}")
            return None 