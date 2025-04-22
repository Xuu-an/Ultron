import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, Any
import asyncio
from pathlib import Path
from .logger import Logger
from .llm_driver import LLMDriver
from .persona_manager import PersonaManager

class ConsciousnessEngine:
    def __init__(self, check_interval: int = 300):  # 默认5分钟检查一次
        self.check_interval = check_interval
        self.state_file = Path("evolve/consciousness_state.json")
        self.current_goal = None
        self.logger = Logger()
        self.llm_driver = LLMDriver()
        self.persona_manager = PersonaManager()
        self.load_state()

    def load_state(self) -> None:
        """加载持久化的目标状态"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.current_goal = json.load(f)
                self.logger.info("Loaded existing goal state", self.current_goal)
            else:
                self.current_goal = {
                    "id": "initial_goal",
                    "description": "initialize the system",
                    "status": "in_progress",
                    "progress": 0.0,
                    "start_time": datetime.now().isoformat(),
                    "last_update": datetime.now().isoformat(),
                    "metrics": {}
                }
                self.save_state()
                self.logger.info("Created initial goal state", self.current_goal)
        except Exception as e:
            self.logger.error(f"Failed to load state: {e}")

    def save_state(self) -> None:
        """保存当前目标状态"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_goal, f, ensure_ascii=False, indent=2)
            self.logger.debug("Saved current goal state", self.current_goal)
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")

    async def check_goal_progress(self) -> Dict[str, Any]:
        """检查目标进度"""
        try:
            # 调用自我认知人格评估目标进度
            self_cognition_prompt = self.persona_manager.get_prompt("self_cognition")
            assessment = await self.llm_driver.generate_response(
                prompt=self_cognition_prompt,
                context={
                    "current_goal": self.current_goal,
                    "task_type": "goal_assessment"
                }
            )
            
            self.logger.info(f"Goal progress checked: {assessment['completion_status']}", assessment)
            return assessment
        except Exception as e:
            self.logger.error(f"Failed to check goal progress: {e}")
            return {
                "completion_status": "failed",
                "quality_score": 0.0,
                "issues": [str(e)],
                "adjustments_needed": ["检查目标进度失败"]
            }

    async def generate_new_goal(self) -> Dict[str, Any]:
        """生成新的目标"""
        try:
            # 调用自我认知人格生成新目标
            self_cognition_prompt = self.persona_manager.get_prompt("self_cognition")
            new_goal = await self.llm_driver.generate_response(
                prompt=self_cognition_prompt,
                context={
                    "current_state": self.current_goal,
                    "task_type": "goal_generation"
                }
            )
            
            self.logger.info("Generated new goal", new_goal)
            return new_goal
        except Exception as e:
            self.logger.error(f"Failed to generate new goal: {e}")
            return {
                "id": f"goal_{int(time.time())}",
                "description": "错误恢复目标",
                "rationale": "生成新目标失败",
                "priority": "high",
                "estimated_complexity": "low",
                "dependencies": [],
                "success_criteria": ["恢复系统正常运行"]
            }

    async def coordinate_personas(self) -> Dict[str, Any]:
        """协调其他人格工作"""
        try:
            # 调用意识人格协调其他人格
            consciousness_prompt = self.persona_manager.get_prompt("consciousness")
            coordination = await self.llm_driver.generate_response(
                prompt=consciousness_prompt,
                context={
                    "current_goal": self.current_goal,
                    "task_type": "coordination"
                }
            )
            
            self.logger.info("Coordinated personas", coordination)
            return coordination
        except Exception as e:
            self.logger.error(f"Failed to coordinate personas: {e}")
            return {
                "required_personas": [],
                "task_assignments": [],
                "collaboration_points": []
            }

    async def run(self) -> None:
        """运行意识引擎的主循环"""
        self.logger.info("Starting consciousness engine")
        while True:
            try:
                # 检查目标进度
                assessment = await self.check_goal_progress()
                
                if assessment["completion_status"] == "complete":
                    # 目标完成，生成新目标
                    new_goal = await self.generate_new_goal()
                    self.current_goal = {
                        **new_goal,
                        "status": "in_progress",
                        "progress": 0.0,
                        "start_time": datetime.now().isoformat(),
                        "last_update": datetime.now().isoformat(),
                        "metrics": {}
                    }
                    self.logger.info("Goal completed, generated new goal", self.current_goal)
                else:
                    # 目标未完成，协调其他人格继续工作
                    coordination = await self.coordinate_personas()
                    # 更新进度
                    self.current_goal["progress"] = min(1.0, self.current_goal["progress"] + 0.1)
                    self.current_goal["last_update"] = datetime.now().isoformat()
                    self.logger.info("Goal in progress, coordinated personas", self.current_goal)
                
                # 保存状态
                self.save_state()
                
                # 等待下一次检查
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in consciousness engine: {e}")
                await asyncio.sleep(60)  # 发生错误时等待1分钟后重试

async def main():
    engine = ConsciousnessEngine()
    await engine.run()

if __name__ == "__main__":
    asyncio.run(main()) 