============================================================
FINAL RESULTS
============================================================
+---------------------+---------+------------+--------+-------+--------+----------+-----------+---------+
| Variant             | Score   | Accuracy   | Easy   | Med   | Hard   |   In Tok |   Out Tok | Cost    |
+=====================+=========+============+========+=======+========+==========+===========+=========+
| v1 Baseline         | 2/10    | 20%        | 1/3    | 0/4   | 1/3    |      937 |       410 | $0.0090 |
+---------------------+---------+------------+--------+-------+--------+----------+-----------+---------+
| v2 Zero-Shot CoT    | 6/10    | 60%        | 3/3    | 2/4   | 1/3    |     1247 |      4680 | $0.0739 |
+---------------------+---------+------------+--------+-------+--------+----------+-----------+---------+
| v3 Few-Shot CoT     | 8/10    | 80%        | 3/3    | 3/4   | 2/3    |     4567 |      3865 | $0.0717 |
+---------------------+---------+------------+--------+-------+--------+----------+-----------+---------+
| v4 Self-Consistency | 8/10    | 80%        | 3/3    | 3/4   | 2/3    |    17635 |     19125 | $0.3398 |
+---------------------+---------+------------+--------+-------+--------+----------+-----------+---------+
| v5 Self-Critique    | 6/10    | 60%        | 3/3    | 2/4   | 1/3    |    10537 |      8754 | $0.1629 |
+---------------------+---------+------------+--------+-------+--------+----------+-----------+---------+
Reflection:

## 1. Which technique produced the biggest accuracy improvement in your experiment? Did the results match the lecture’s claims about CoT?

The biggest improvement came from Few-Shot CoT and Self-Consistency. The baseline only got 20% accuracy, but v3 and v4 reached 80%. This matched the lecture because step-by-step reasoning helped the model solve harder math problems better.

## 2. Which technique provided the best value in terms of accuracy gained per dollar? Include your calculations.

Few-Shot CoT gave the best value because it improved accuracy a lot without using too many tokens. Self-Consistency also gave good accuracy, but it was more expensive since it used five reasoning paths for each question. So v3 was the better balance between cost and performance.

## 3. Did self-critique perform better, worse, or about the same as few-shot CoT? Explain why you think that happened.

Self-Critique performed worse than Few-Shot CoT in my results. Sometimes the model changed answers that were already correct and made them wrong. I think the review step sometimes confused the model instead of helping it.

## 4. If you were building a production math-solving agent for paying customers, which approach would you choose and why?

I would choose Few-Shot CoT because it gave good accuracy and lower cost. Self-Consistency was accurate too, but it needed many API calls which increased the cost. Few-Shot CoT seemed more practical for real users.

## 5. Review the failures in v4, if there were any. Why were those problems still difficult even after using five reasoning paths?

Some problems still failed because the model misunderstood the logic of the question. Even with five reasoning paths, the wrong answer could still appear more times. Complex logic and multi-step reasoning problems were still difficult for the model. Other then this, sometime codes are broken, so need to fix them one by one and in the last codes were properly run in each file.