"""Exercise denominator, format and paired-detection edge cases."""
import unittest
import numpy as np
from abstention_audit import audit


class AuditCases(unittest.TestCase):
    def test_optional_answers_and_format_denominators(self):
        forced={'correct_choice':np.array([1,2,3,4]),'actual_choice':np.array([1,1,3,4]),'conditional_choice':np.array([1,1,3,4])}
        optional={'correct_choice':forced['correct_choice'],'actual_choice':np.array([2,5,-1,4])}
        r=audit(forced,optional)
        self.assertEqual((r['coverage'],r['abstention'],r['invalid']),(.5,.25,.25))
        self.assertEqual(r['accuracy_on_answered_questions'],.5)
        self.assertEqual(r['forced_accuracy_among_answered'],1.)
        self.assertEqual(r['abstention_given_forced_wrong'],1.)
        self.assertEqual(r['abstention_given_forced_correct'],0.)

    def test_alternate_label_and_empty_answer_set(self):
        forced={'correct_choice':np.array([1,2]),'actual_choice':np.array([1,2]),'conditional_choice':np.array([1,2])}
        r=audit(forced,{'correct_choice':forced['correct_choice'],'actual_choice':np.array([6,6])},6)
        self.assertEqual(r['abstention'],1.)
        self.assertIsNone(r['accuracy_on_answered_questions'])

    def test_equal_extreme_detection_rates_are_finite(self):
        forced={'correct_choice':np.array([1,2,-1,-1]),'actual_choice':np.ones(4),'conditional_choice':np.ones(4)}
        r=audit(forced,{'correct_choice':forced['correct_choice'],'actual_choice':np.full(4,5)})
        self.assertEqual(r['d_prime'],0.)
        self.assertLess(r['criterion'],0.)
        self.assertTrue(np.isfinite(r['criterion']))

    def test_question_order_is_checked(self):
        f={'ids':['a','b'],'correct_choice':np.array([1,1]),'actual_choice':np.ones(2),'conditional_choice':np.ones(2)}
        a={'ids':['b','a'],'correct_choice':np.array([1,1]),'actual_choice':np.ones(2)}
        with self.assertRaises(AssertionError):audit(f,a)


if __name__=='__main__':unittest.main()
