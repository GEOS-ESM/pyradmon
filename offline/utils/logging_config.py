"""
Logging configuration for pyradmon.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional, Union


class PyRadmonLogger:    
    _loggers: dict[str, logging.Logger] = {}
    _initialized: bool = False
    
    @classmethod
    def setup_logging(
        cls,
        log_dir: Union[str, Path],
        log_filename: str = "pyradmon.log",
        level: Union[str, int] = logging.INFO,
        component: str = "pyradmon",
        console_output: bool = True,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ) -> logging.Logger:
        """
        Setting up logging for a pyradmon component.
        
        Args:
            log_dir: Directory where log files will be stored
            log_filename: Name of the log file
            level: Logging level (string or logging constant)
            component: Component name (e.g., 'spatial', 'timeseries')
            console_output: Whether to output logs to console
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup log files to keep
            
        Returns:
            Logger instance
            
        Raises:
            OSError: If log directory cannot be created
            PermissionError: If log file cannot be written
        """
        # Convert log_dir to Path if it's a string
        log_dir = Path(log_dir) if isinstance(log_dir, str) else log_dir
        
        # Create log directory if it doesn't exist
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise OSError(f"Failed to create log directory '{log_dir}': {e}") from e
        
        # Get or create logger for this component
        logger_name = f"pyradmon.{component}"
        logger = logging.getLogger(logger_name)
        
        # Avoid duplicate handlers if already configured
        if logger.handlers:
            return logger
        
        # Convert string level to logging constant
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        
        logger.setLevel(level)
        
        # File handler with rotation
        log_file = log_dir / log_filename
        try:
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except (OSError, PermissionError) as e:
            # If file logging fails, at least try console logging
            if not console_output:
                raise PermissionError(
                    f"Failed to create log file '{log_file}': {e}"
                ) from e
            # Continue with console-only logging
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # Prevent propagation to root logger to avoid duplicate messages
        logger.propagate = False
        
        # Store logger
        cls._loggers[logger_name] = logger
        cls._initialized = True
        
        logger.info(f"Logging initialized for component '{component}' at {log_file}")
        
        return logger
    
    @classmethod
    def get_logger(cls, component: str = "pyradmon") -> logging.Logger:
        """
        Get an existing logger for a component.
        
        Args:
            component: Component name
            
        Returns:
            Logger instance, or root logger if component logger doesn't exist
        """
        logger_name = f"pyradmon.{component}"
        logger = cls._loggers.get(logger_name)
        
        if logger is None:
            # Return root logger as fallback
            return logging.getLogger("pyradmon")
        
        return logger
    
    @classmethod
    def is_initialized(cls) -> bool:
        """Check if logging has been initialized."""
        return cls._initialized


def setup_logging(
    log_dir: Union[str, Path],
    log_filename: str = "pyradmon.log",
    level: Union[str, int] = logging.INFO,
    component: str = "pyradmon",
    console_output: bool = True
) -> logging.Logger:
    """
    Function to set up logging.
    
    This is a wrapper around PyRadmonLogger.setup_logging() for easier use.
    
    Args:
        log_dir: Directory where log files will be stored
        log_filename: Name of the log file
        level: Logging level (string or logging constant)
        component: Component name (e.g., 'spatial', 'timeseries')
        console_output: Whether to output logs to console
        
    Returns:
        Configured logger instance
    """
    return PyRadmonLogger.setup_logging(
        log_dir=log_dir,
        log_filename=log_filename,
        level=level,
        component=component,
        console_output=console_output
    )


def get_logger(component: str = "pyradmon") -> logging.Logger:
    """
    Convenience function to get a logger.
    
    Args:
        component: Component name
        
    Returns:
        Logger instance
    """
    return PyRadmonLogger.get_logger(component=component)

