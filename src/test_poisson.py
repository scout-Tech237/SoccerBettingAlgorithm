from math import exp, factorial

def poisson_pmf(k, lam):
    return (exp(-lam) * (lam ** k)) / factorial(k)

lambda_home = 1.6
lambda_away = 0.9

for goals in range(6):
    print(f"Home scoring {goals}: {poisson_pmf(goals, lambda_home):.4f}")

print()

for goals in range(6):
    print(f"Away scoring {goals}: {poisson_pmf(goals, lambda_away):.4f}")