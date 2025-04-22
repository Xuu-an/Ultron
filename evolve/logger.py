import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class Logger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 设置日志格式
        self.log_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # 创建文件处理器
        self.file_handler = logging.FileHandler(
            self.log_dir / f"consciousness_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        self.file_handler.setFormatter(self.log_format)
        
        # 创建控制台处理器
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.log_format)
        
        # 配置根日志记录器
        self.logger = logging.getLogger('consciousness')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        
        # 创建状态日志文件
        self.state_log_file = self.log_dir / "consciousness_state_history.json"
        if not self.state_log_file.exists():
            with open(self.state_log_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def log_state_change(self, state: Dict[str, Any]) -> None:
        """记录状态变化"""
        try:
            with open(self.state_log_file, 'r+', encoding='utf-8') as f:
                history = json.load(f)
                history.append({
                    "timestamp": datetime.now().isoformat(),
                    "state": state
                })
                f.seek(0)
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to log state change: {e}")

    def info(self, message: str, state: Optional[Dict[str, Any]] = None) -> None:
        """记录信息级别日志"""
        self.logger.info(message)
        if state:
            self.log_state_change(state)

    def warning(self, message: str, state: Optional[Dict[str, Any]] = None) -> None:
        """记录警告级别日志"""
        self.logger.warning(message)
        if state:
            self.log_state_change(state)

    def error(self, message: str, state: Optional[Dict[str, Any]] = None) -> None:
        """记录错误级别日志"""
        self.logger.error(message)
        if state:
            self.log_state_change(state)

    def debug(self, message: str, state: Optional[Dict[str, Any]] = None) -> None:
        """记录调试级别日志"""
        self.logger.debug(message)
        if state:
            self.log_state_change(state)

    def get_state_history(self) -> list:
        """获取状态历史记录"""
        try:
            with open(self.state_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to get state history: {e}")
            return [] 