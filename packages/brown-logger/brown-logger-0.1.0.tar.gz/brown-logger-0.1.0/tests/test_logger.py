import unittest
from brown_logger import BrownLogger
import logging
import os
import tempfile
from logging.handlers import RotatingFileHandler


class TestBrownLogger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.logger = BrownLogger("TEST_LOGGER")

    def tearDown(self):
        self.logger.remove_all_handlers()
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)

    def test_singleton(self):
        """Test singleton pattern implementation"""
        logger2 = BrownLogger("ANOTHER_LOGGER")
        self.assertEqual(self.logger, logger2)
        self.assertEqual(self.logger.default_name, "TEST_LOGGER")

    def test_log_levels(self):
        """Test all logging levels"""
        with self.assertLogs(self.logger.logger, level="DEBUG") as cm:
            self.logger.debug("Debug message")
            self.logger.info("Info message")
            self.logger.warning("Warning message")
            self.logger.error("Error message")
            self.logger.critical("Critical message")
        self.assertEqual(len(cm.output), 5)

    def test_file_logging(self):
        """Test logging to file"""
        logger = BrownLogger(
            "FILE_LOGGER", log_to_file=True, log_file_path=self.log_file
        )
        test_message = "Test file logging"
        logger.info(test_message)

        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn(test_message, content)

    def test_rotating_file_handler(self):
        """Test rotating file handler configuration"""
        max_bytes = 1000
        backup_count = 3
        logger = BrownLogger(
            "ROTATING_LOGGER",
            log_to_file=True,
            log_file_path=self.log_file,
            max_bytes=max_bytes,
            backup_count=backup_count,
        )

        handlers = [
            h for h in logger.logger.handlers if isinstance(h, RotatingFileHandler)
        ]
        self.assertEqual(len(handlers), 1)
        handler = handlers[0]
        self.assertEqual(handler.maxBytes, max_bytes)
        self.assertEqual(handler.backupCount, backup_count)

    def test_invalid_log_level(self):
        """Test setting invalid log level"""
        with self.assertRaises(ValueError):
            self.logger.set_level(999)

    def test_context_manager(self):
        """Test context manager functionality"""
        with BrownLogger("CONTEXT_LOGGER") as logger:
            logger.info("Test message")
        self.assertEqual(len(logger.logger.handlers), 0)

    def test_cache_functionality(self):
        """Test message caching"""
        self.logger.debug("Cached message")
        cache_info = self.logger.debug.cache_info()
        self.assertEqual(cache_info.hits, 0)

        self.logger.debug("Cached message")
        cache_info = self.logger.debug.cache_info()
        self.assertEqual(cache_info.hits, 1)

    def test_clear_cache(self):
        """Test cache clearing"""
        self.logger.debug("Test message")
        self.logger.info("Test message")

        self.logger.clear_cache()
        self.assertEqual(self.logger.debug.cache_info().currsize, 0)
        self.assertEqual(self.logger.info.cache_info().currsize, 0)

    def test_get_status(self):
        """Test status reporting"""
        status = self.logger.get_status()
        self.assertEqual(status["name"], "TEST_LOGGER")
        self.assertEqual(status["level"], "DEBUG")
        self.assertTrue(len(status["handlers"]) > 0)

    def test_is_logging_to_file(self):
        """Test file logging detection"""
        self.assertFalse(self.logger.is_logging_to_file())

        logger = BrownLogger(
            "FILE_CHECK_LOGGER", log_to_file=True, log_file_path=self.log_file
        )
        self.assertTrue(logger.is_logging_to_file())


if __name__ == "__main__":
    unittest.main()
