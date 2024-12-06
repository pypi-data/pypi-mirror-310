import os
import tempfile


# Common test utilities
def create_temp_log_file():
    temp_dir = tempfile.mkdtemp()
    return os.path.join(temp_dir, "test.log")


# Common test fixtures
TEST_LOG_LEVELS = [10, 20, 30, 40, 50]  # DEBUG, INFO, WARNING, ERROR, CRITICAL
