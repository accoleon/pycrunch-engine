# TODO: Make configurable
py_test_exclusions = [
    '*_pytest/*',
    '*site-packages/*',
    '*.pytest_cache/*',
    '*pytest_support/interception_plugin.py',

]

coverage_6_exclusions = [
    '**_pytest/**',
    '**site-packages/**',
    '**.pytest_cache/**',
    '**pytest_support/interception_plugin.py',

]

exclude_list = py_test_exclusions + [
    '*PyCharm.app/Contents/helpers/pydev/pydevd_file_utils.py',
    '*PyCharm.app/Contents/helpers/pydev/_pydevd_bundle/pydevd_comm.py',
    '*PyCharm.app/Contents/helpers/pydev/_pydevd_frame_eval/pydevd_frame_tracing.py',
    '*PyCharm.app/Contents/helpers/pydev/_pydevd_frame_eval/pydevd_modify_bytecode.py',
    '*PyCharm.app/Contents/plugins/python/helpers/pydev/*',
    '*site-packages/werkzeug/serving.py',
    '*runner/test_runner.py',
    '*runner/single_test_execution_result.py',
    '*plugins/pytest_support/hot_reload.py',
    '*plugins/pytest_support/pytest_runner_engine.py',
    '*runner/interception.py',
    '*pycrunch/introspection/*',
    '*pycrunch/shared/models.py'

]

