import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
import os
from functools import lru_cache


class BrownLogger:
    """
    A Singleton Logger implementation that supports both console and file logging.
    Triển khai Logger theo mẫu Singleton hỗ trợ ghi log ra console và file.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton pattern implementation to ensure only one logger instance exists.
        Triển khai mẫu Singleton để đảm bảo chỉ tồn tại một instance logger.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        default_name: str = "BrownLogger",
        log_to_console: bool = True,
        log_to_file: bool = False,
        log_file_path: Optional[str] = None,
        log_level: int = logging.DEBUG,
        max_bytes: int = 5_000_000,
        backup_count: int = 5,
    ) -> None:
        """
        Initialize the logger with specified configuration.
        Khởi tạo logger với cấu hình được chỉ định.

        Args:
            default_name (str): Logger identifier name / Tên định danh của logger
            log_to_console (bool): Enable/disable console logging / Bật/tắt ghi log ra console
            log_to_file (bool): Enable/disable file logging / Bật/tắt ghi log ra file
            log_file_path (Optional[str]): Path to log file / Đường dẫn đến file log
            log_level (int): Minimum log level / Cấp độ log tối thiểu
            max_bytes (int): Maximum size of each log file / Kích thước tối đa của mỗi file log
            backup_count (int): Number of backup files to keep / Số lượng file backup cần giữ lại
        """
        if hasattr(self, "logger"):
            return

        if log_level not in [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]:
            raise ValueError(f"Invalid log level: {log_level}")

        self.default_name = default_name
        self.logger = logging.getLogger(default_name)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            handlers_configured = False
            if log_to_console:
                self._setup_console_handler(log_level)
                handlers_configured = True
            if log_to_file:
                self._setup_file_handler(
                    log_file_path, log_level, max_bytes, backup_count
                )
                handlers_configured = True

            if not handlers_configured:
                self._setup_console_handler(log_level)
                logging.warning(
                    "No handlers were configured. Defaulting to console logging."
                )

    def _setup_console_handler(self, log_level: int) -> None:
        """
        Set up console handler for logging to stdout.
        Thiết lập console handler để ghi log ra stdout.

        Args:
            log_level (int): Minimum log level / Cấp độ log tối thiểu
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        stream_handler.setFormatter(log_format)
        self.logger.addHandler(stream_handler)

    def _setup_file_handler(
        self,
        log_file_path: Optional[str],
        log_level: int,
        max_bytes: int,
        backup_count: int,
    ) -> None:
        """
        Set up file handler for logging to a file with rotation.
        Thiết lập file handler để ghi log ra file với rotation.

        Args:
            log_file_path (Optional[str]): Path to log file / Đường dẫn file log
            log_level (int): Minimum log level / Cấp độ log tối thiểu
            max_bytes (int): Maximum size of each log file / Kích thước tối đa của mỗi file log
            backup_count (int): Number of backup files / Số lượng file backup
        """
        try:
            if max_bytes <= 0:
                raise ValueError("max_bytes must be positive")

            if backup_count < 0:
                raise ValueError("backup_count must be non-negative")

            if log_file_path is None:
                log_file_path = f"{self.default_name}.log"

            log_dir = os.path.dirname(log_file_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(log_level)
            log_format = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(log_format)
            self.logger.addHandler(file_handler)
        except Exception as e:
            self.logger.error(f"Không thể tạo file handler: {str(e)}")

    def set_level(self, level: int) -> None:
        """
        Dynamically change the log level for all handlers.
        Thay đổi cấp độ log động cho tất cả các handlers.

        Args:
            level (int): New log level to set / Cấp độ log mới cần thiết lập
        """
        if level not in [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]:
            raise ValueError(f"Invalid log level: {level}")
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def __enter__(self) -> "BrownLogger":
        """
        Context manager entry point.
        Điểm vào của context manager.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point - closes and removes all handlers.
        Điểm thoát của context manager - đóng và xóa tất cả handlers.
        """
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

    @lru_cache(maxsize=128)
    def debug(self, message: object):
        """
        Log a debug message with caching.
        Ghi log debug message với cache.

        Args:
            message (object): Message to log / Thông điệp cần ghi log
        """
        self.logger.debug(message)

    @lru_cache(maxsize=128)
    def info(self, message: object):
        """
        Log an info message with caching.
        Ghi log info message với cache.

        Args:
            message (object): Message to log / Thông điệp cần ghi log
        """
        self.logger.info(message)

    def warning(self, message: object):
        """
        Log a warning message.
        Ghi log warning message.

        Args:
            message (object): Message to log / Thông điệp cần ghi log
        """
        self.logger.warning(message)

    def error(self, message: object):
        """
        Log an error message.
        Ghi log error message.

        Args:
            message (object): Message to log / Thông điệp cần ghi log
        """
        self.logger.error(message)

    def critical(self, message: object):
        """
        Log a critical message.
        Ghi log critical message.

        Args:
            message (object): Message to log / Thông điệp cần ghi log
        """
        self.logger.critical(message)

    def get_status(self) -> dict:
        """
        Get the current status of the logger.
        Lấy trạng thái hiện tại của logger.

        Returns:
            dict: Dạng dictionary chứa thông tin trạng thái của logger
            dict: Dictionary containing logger status information
        """
        return {
            "name": self.default_name,
            "level": logging.getLevelName(self.logger.level),
            "handlers": [
                {
                    "type": type(handler).__name__,
                    "level": logging.getLevelName(handler.level),
                }
                for handler in self.logger.handlers
            ],
        }

    def clear_cache(self) -> None:
        """
        Clear the message cache for debug and info levels.
        Xóa cache của các message cho level debug và info.
        """
        self.debug.cache_clear()
        self.info.cache_clear()

    def is_logging_to_file(self) -> bool:
        """
        Check if the logger is currently logging to a file.
        Kiểm tra xem logger có đang ghi vào file hay không.

        Returns:
            bool: True if logging to file, False otherwise
        """
        return any(
            isinstance(handler, RotatingFileHandler) for handler in self.logger.handlers
        )

    def remove_all_handlers(self) -> None:
        """
        Remove all handlers from the logger.
        Xóa tất cả handlers khỏi logger.
        """
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
