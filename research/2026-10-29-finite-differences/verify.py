"""Exact finite checks; the general proofs are in note.md."""

from math import comb, factorial


def alternating_sum(n, m):
    return sum((-1) ** (n - j) * comb(n, j) * j**m for j in range(n + 1))


def partition_counts(limit):
    counts = [[0] * (limit + 1) for _ in range(limit + 1)]
    counts[0][0] = 1
    for m in range(1, limit + 1):
        for n in range(1, m + 1):
            counts[m][n] = n * counts[m - 1][n] + counts[m - 1][n - 1]
    return counts


def main():
    limit = 12
    counts = partition_counts(limit)
    pairs = 0
    for n in range(limit + 1):
        for m in range(limit + 1):
            actual = alternating_sum(n, m)
            expected = factorial(n) * counts[m][n]
            if actual != expected:
                raise AssertionError((n, m, actual, expected))
            pairs += 1

    polynomial_cases = 0
    for degree in range(8):
        # Leading coefficient 3, with lower coefficients 1 through degree.
        coefficients = list(range(1, degree + 1)) + [3]
        for n in range(degree, 9):
            actual = sum(
                (-1) ** (n - j)
                * comb(n, j)
                * sum(c * j**k for k, c in enumerate(coefficients))
                for j in range(n + 1)
            )
            expected = 3 * factorial(n) if n == degree else 0
            if actual != expected:
                raise AssertionError((degree, n, actual, expected))
            polynomial_cases += 1

    print(f"PASS: {pairs} alternating-sum / partition-count pairs (0 <= n,m <= {limit}).")
    print(f"PASS: {polynomial_cases} polynomial finite-difference cases.")
    print("Finite checks support the examples; see note.md for proofs.")


if __name__ == "__main__":
    main()
