import unittest
from dockerfile_py_gen.rules.DL3044 import check_rule

class TestDL3044Check(unittest.TestCase):

    def test_ok_with_normal_env(self):
        errors = check_rule(["ENV BLA=\"blubb\"",
                             "ENV BLUBB=\"${BLA}/blubb\""])
        self.assertEqual(len(errors), 0)

    def test_fail_with_partial_match_5(self):
        errors = check_rule(["ENV BLA=\"blubb\" BLUBB=\"$BLA/$BLAFOO/blubb\""])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["code"], "DL3044")

    def test_fail_with_selfreferencing_with_curly_braces_env(self):
        errors = check_rule(["ENV BLA=\"blubb\" BLUBB=\"${BLA}/blubb\""])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["code"], "DL3044")

    def test_fail_with_selfreferencing_without_curly_braces_env(self):
        errors = check_rule(["ENV BLA=\"blubb\" BLUBB=\"$BLA/blubb\""])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["code"], "DL3044")

    def test_fail_with_full_match_1(self):
        errors = check_rule(["ENV BLA=\"blubb\" BLUBB=\"$BLA\""])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["code"], "DL3044")

    def test_fail_with_full_match_2(self):
        errors = check_rule(["ENV BLA=\"blubb\" BLUBB=\"${BLA}\""])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["code"], "DL3044")

    def test_ok_with_partial_match_6(self):
        errors = check_rule(["ENV BLA=\"blubb\" BLUBB=\"BLA/$BLAFOO/BLA\""])
        self.assertEqual(len(errors), 0)

    def test_ok_when_previously_defined_in_arg(self):
        errors = check_rule(["ARG BLA",
                             "ENV BLA=${BLA}"])
        self.assertEqual(len(errors), 0)

    def test_ok_when_previously_defined_in_env(self):
        errors = check_rule(["ENV BLA blubb",
                             "ENV BLA=${BLA}"])
        self.assertEqual(len(errors), 0)

    def test_ok_with_referencing_a_variable_on_its_own_right_hand_side(self):
        errors = check_rule(["ENV PATH=/bla:${PATH}"])
        self.assertEqual(len(errors), 0)

    def test_fail_when_referencing_a_variable_on_its_own_right_side_twice_within_the_same_env(self):
        errors = check_rule(["ENV PATH=/bla:${PATH} PATH=/blubb:${PATH}"])
        print(errors)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["code"], "DL3044")

if __name__ == "__main__":
    unittest.main()
