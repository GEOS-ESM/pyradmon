"""Tests for the centralized logging system."""

import pytest
import logging
import tempfile
from pathlib import Path
import sys

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'offline'))
from utils.logging_config import setup_logging, get_logger, PyRadmonLogger


class TestSetupLogging:
    """Tests for setup_logging function."""
    
    def test_creates_log_directory(self):
        """Test that setup_logging creates the log directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / 'new_log_dir'
            
            setup_logging(
                log_dir=log_dir,
                log_filename='test.log',
                component='test_create_dir'
            )
            
            assert log_dir.exists()
    
    def test_creates_log_file(self):
        """Test that setup_logging creates a log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                component='test_create_file'
            )
            
            # Write a log message to ensure file is created
            logger.info("Test message")
            
            log_file = Path(tmpdir) / 'test.log'
            assert log_file.exists()
    
    def test_returns_logger_instance(self):
        """Test that setup_logging returns a logger instance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                component='test_returns_logger'
            )
            
            assert isinstance(logger, logging.Logger)
    
    def test_logger_name_includes_component(self):
        """Test that logger name includes the component name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                component='mycomponent'
            )
            
            assert 'mycomponent' in logger.name
    
    def test_log_message_written_to_file(self):
        """Test that log messages are written to the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                component='test_write_msg',
                console_output=False  # Disable console to avoid test noise
            )
            
            test_message = "This is a test log message"
            logger.info(test_message)
            
            # Force flush
            for handler in logger.handlers:
                handler.flush()
            
            log_file = Path(tmpdir) / 'test.log'
            log_contents = log_file.read_text()
            
            assert test_message in log_contents


class TestGetLogger:
    """Tests for get_logger function."""
    
    def test_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger('test_component')
        assert logger is not None
    
    def test_returns_same_logger_for_same_component(self):
        """Test that get_logger returns the same logger for the same component."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # First setup a logger
            setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                component='same_component'
            )
            
            # Get it again
            logger1 = get_logger('same_component')
            logger2 = get_logger('same_component')
            
            assert logger1 is logger2


class TestPyRadmonLogger:
    """Tests for PyRadmonLogger class."""
    
    def test_is_initialized_returns_bool(self):
        """Test that is_initialized returns a boolean."""
        result = PyRadmonLogger.is_initialized()
        assert isinstance(result, bool)
    
    def test_is_initialized_true_after_setup(self):
        """Test that is_initialized returns True after setup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                component='init_test'
            )
            
            assert PyRadmonLogger.is_initialized() == True


class TestLoggingLevels:
    """Tests for different logging levels."""
    
    def test_info_level(self):
        """Test INFO level logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                level='INFO',
                component='level_info',
                console_output=False
            )
            
            logger.info("Info message")
            logger.debug("Debug message")  # Should not appear
            
            for handler in logger.handlers:
                handler.flush()
            
            log_contents = (Path(tmpdir) / 'test.log').read_text()
            
            assert "Info message" in log_contents
            assert "Debug message" not in log_contents
    
    def test_debug_level(self):
        """Test DEBUG level logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = setup_logging(
                log_dir=tmpdir,
                log_filename='test.log',
                level='DEBUG',
                component='level_debug',
                console_output=False
            )
            
            logger.debug("Debug message")
            
            for handler in logger.handlers:
                handler.flush()
            
            log_contents = (Path(tmpdir) / 'test.log').read_text()
            
            assert "Debug message" in log_contents

