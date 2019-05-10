def pytest_ignore_collect(path, config):
    return 'manual_tests' in str(path)
