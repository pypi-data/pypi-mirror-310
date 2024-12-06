from pathlib import Path

from givemecontext.automations.directory_logger import DirectoryLogger
from givemecontext.automations.format_check_test import CodeQualityAutomation
from givemecontext.config import get_logs_dir


class GiveMeContext:
    """
    GiveMeContext provides a unified interface for running all givemecontext automations.
    It follows the singleton pattern to ensure consistent state across the application.

    Example usage:
        from givemecontext import context, to_log

        @to_log
        def my_function():
            pass

        # Run all automations
        context.run()

        # Or run specific automations
        context.run_code_quality()
        context.run_directory_logger()
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the GiveMeContext instance."""
        # Ensure logs directory exists
        get_logs_dir()

    def run(self, code_quality: bool = True, directory_logger: bool = True) -> None:
        """
        Run all enabled automations.

        Args:
            code_quality (bool): Whether to run code quality checks. Defaults to True.
            directory_logger (bool): Whether to log directory structure. Defaults to True.
        """
        try:
            if code_quality:
                self.run_code_quality()

            if directory_logger:
                self.run_directory_logger()
        except Exception as e:
            print(f"Error running GiveMeContext automations: {e}")
            raise

    def run_code_quality(self) -> None:
        """Run code quality checks (black, ruff, pytest)."""
        try:
            CodeQualityAutomation.run_with_log()
        except Exception as e:
            print(f"Error running code quality checks: {e}")
            raise

    def run_directory_logger(self) -> None:
        """Log the filtered directory structure."""
        try:
            DirectoryLogger.log_filtered_directory_structure()
        except Exception as e:
            print(f"Error logging directory structure: {e}")
            raise

    @property
    def logs_dir(self) -> Path:
        """Get the path to the logs directory."""
        return get_logs_dir()
