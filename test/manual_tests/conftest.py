# noinspection PyUnusedLocal
def pytest_ignore_collect(path, config):
    """Ignore all files in this test subdirectory."""
    return True
