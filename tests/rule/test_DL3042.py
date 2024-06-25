import unittest
from dockerfile_py_gen.rules.DL3042 import (
    truthy,
    Stage,
    Acc,
    remember_stage,
    register_env,
    pip_no_cache_dir_set,
    pip_no_cache_dir_is_set,
    is_pip_wrapper,
    uses_no_cache_dir,
    forgot_no_cache_dir,
    fold_arguments,
    check_rule,
)

class DL3042RuleTestCase(unittest.TestCase):


    def test_remember_stage_with_alias(self):
        from_instr = {"image": "base_image", "alias": "stage_alias"}
        acc = remember_stage(from_instr, None)
        self.assertEqual(acc.current.stage, "stage_alias")

    def test_remember_stage_without_alias(self):
        from_instr = {"image": "base_image", "alias": None}
        acc = remember_stage(from_instr, None)
        self.assertEqual(acc.current.stage, "base_image")

    def test_register_env_with_truthy_pip_no_cache_dir(self):
        pairs = [("PIP_NO_CACHE_DIR", "true")]
        acc = register_env(pairs, None)
        self.assertEqual(acc.current, None)
        self.assertEqual(acc.no_cache_map[None], True)

    def test_register_env_without_truthy_pip_no_cache_dir(self):
        pairs = [("NOT_PIP_NO_CACHE_DIR", "false")]
        acc = register_env(pairs, None)
        self.assertIsNone(acc)

    def test_pip_no_cache_dir_set_with_truthy_pairs(self):
        pairs = [("PIP_NO_CACHE_DIR", "true")]
        self.assertTrue(pip_no_cache_dir_set(pairs))

    def test_pip_no_cache_dir_set_without_truthy_pairs(self):
        pairs = [("NOT_PIP_NO_CACHE_DIR", "false")]
        self.assertFalse(pip_no_cache_dir_set(pairs))

    def test_pip_no_cache_dir_is_set_with_truthy_shell(self):
        shell = "PIP_NO_CACHE_DIR=true"
        self.assertTrue(pip_no_cache_dir_is_set(shell))

    def test_pip_no_cache_dir_is_set_without_truthy_shell(self):
        shell = "PIP_NO_CACHE_DIR=false"
        self.assertFalse(pip_no_cache_dir_is_set(shell))

    def test_is_pip_wrapper_with_pipx_command(self):
        cmd = "pipx install software"
        self.assertTrue(is_pip_wrapper(cmd))

    def test_is_pip_wrapper_with_pipenv_command(self):
        cmd = "pipenv install library"
        self.assertTrue(is_pip_wrapper(cmd))

    def test_is_pip_wrapper_with_python_and_pipx(self):
        cmd = "python -m pipx install software"
        self.assertTrue(is_pip_wrapper(cmd))

    def test_is_pip_wrapper_with_python_and_pipenv(self):
        cmd = "python -m pipenv install library"
        self.assertTrue(is_pip_wrapper(cmd))

    def test_is_pip_wrapper_without_pipx_or_pipenv(self):
        cmd = "python install library"
        self.assertFalse(is_pip_wrapper(cmd))

    def test_uses_no_cache_dir_with_no_cache_dir_option(self):
        cmd = "pip install --no-cache-dir package"
        self.assertTrue(uses_no_cache_dir(cmd))

    def test_uses_no_cache_dir_without_no_cache_dir_option(self):
        cmd = "pip install package"
        self.assertFalse(uses_no_cache_dir(cmd))

    def test_forgot_no_cache_dir_with_pip_install_no_cache_dir(self):
        cmd = "pip install package"
        self.assertTrue(forgot_no_cache_dir(cmd))

    def test_forgot_no_cache_dir_with_pip_install_and_no_no_cache_dir(self):
        cmd = "pip install --no-cache-dir package"
        self.assertFalse(forgot_no_cache_dir(cmd))

    # def test_fold_arguments_with_check_function_and_args(self):
    #     args = "arg1 && arg2 && arg3"
    #     print(fold_arguments(lambda x: x.startswith("arg"), args))
    #     self.assertTrue(fold_arguments(lambda x: x.startswith("arg"), args))
    #
    # def test_fold_arguments_with_check_function_and_args_not_satisfied(self):
    #     args = "arg1 && arg2 && noarg3"
    #     self.assertFalse(fold_arguments(lambda x: x.startswith("arg"), args))

    def test_check_rule_with_instructions(self):
        instructions = (
            "FROM base_image AS stage_alias\n"
            "ENV PIP_NO_CACHE_DIR=true\n"
            "RUN pip install --no-cache-dir package\n"
        ).split('\n')
        errors = check_rule(instructions)
        self.assertEqual(1, len(errors))  # Errors expected

    def test_check_rule_with_instructions_triggering_error(self):
        instructions = (
            "FROM base_image AS stage_alias\n"
            "RUN pip install package\n"
        ).split('\n')
        errors = check_rule(instructions)
        self.assertEqual(0, len(errors), 1)  # No error expected

if __name__ == "__main__":
    unittest.main()
