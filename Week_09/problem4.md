Problem 4 (Medium+): Training Session

You are building a combat academy tracker. Create a TrainingSession dataclass that tracks a trainee’s scores and automatically maintains computed statistics.

1. A TrainingSession has trainee (str), discipline (str), scores (list of ints, empty by default), and two computed fields average (float) and rank (str) — that should not be constructor parameters.
2. average and rank must be computed immediately after creation and stay in sync whenever scores change. Rank is "Elite" if average ≥ 90, "Skilled" if average ≥ 70, and "Novice" otherwise.
3. add_score(self, score: int) — records a new score and ensures computed fields reflect the updated data.
4. outperforms(self, other: 'TrainingSession') -> bool — returns whether this trainee’s average exceeds another’s.

Input
t1 = TrainingSession("Duncan", "Swordsmanship", [85, 92, 78])
print(t1)
t1.add_score(95)
print(t1.average)
print(t1.rank)

t2 = TrainingSession("Feyd", "Swordsmanship", [95, 90, 98])
print(t2.rank)
print(t1.outperforms(t2))

t3 = TrainingSession("Rabban", "Swordsmanship")
print(t3.rank)

Expected Output
TrainingSession(trainee='Duncan', discipline='Swordsmanship', scores=[85, 92, 78], average=85.0, rank='Skilled')
87.5
Skilled
Elite
False
Novice