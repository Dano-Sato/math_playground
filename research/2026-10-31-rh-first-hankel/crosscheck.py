"""Non-rigorous independent numerical cross-check, not part of the certificate.

Run after certify.py:
    python research/2026-10-31-rh-first-hankel/crosscheck.py
Requires mpmath (available in this session); no randomness; precision 50 and 80.
Computes Taylor coefficients directly from gamma*zeta rather than the kernel.
"""

from pathlib import Path
from math import factorial
import json
import sys
import mpmath as mp


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    folder = Path(__file__).resolve().parent
    cert = json.loads((folder / "certificate.json").read_text(encoding="utf-8"))
    lines = ["# 별도 경로 수치 대조", "",
             f"- mpmath {mp.__version__}; 정밀도 50, 80자리; 난수 없음.",
             "- 이 결과는 수치 관찰이며 오차 인증의 근거가 아니다.",
             "- gamma·zeta 정의에서 t=0의 8차 Taylor 계수를 직접 계산한다.", ""]
    previous = None
    for precision in (50, 80):
        with mp.workdps(precision):
            def xi(t):
                s = mp.mpf("0.5") + 1j * t
                return s * (s - 1) * mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s) / 2

            coefficients = mp.taylor(xi, 0, 8)
            raw = [mp.re(coefficients[2 * k]) * (-1) ** k * factorial(2 * k) / 2 for k in range(5)]
            a = [mp.re(coefficients[2 * k] / coefficients[0]) for k in range(5)]
            m = []
            for n in range(4):
                m.append(-(n + 1) * a[n + 1] - sum(a[j] * m[n - j] for j in range(1, n + 1)))
            determinants = [m[0] * m[2] - m[1] ** 2, m[1] * m[3] - m[2] ** 2]
            boxes = cert["half_line_integrals"] + cert["log_derivative_moments"] + [cert["D0"], cert["D1"]]
            values = raw + m + determinants
            scale = mp.mpf(cert["scale_denominator"])
            for value, box in zip(values, boxes):
                assert mp.mpf(box["lower_numerator"]) / scale < value < mp.mpf(box["upper_numerator"]) / scale
            if previous is not None:
                assert max(abs(x - y) for x, y in zip(values, previous)) < mp.mpf("1e-42")
            previous = values
            lines += [f"- {precision}자리: 11개 수치가 인증 구간 안에 있음 PASS",
                      f"  D0 ≈ {mp.nstr(determinants[0], 28)}, D1 ≈ {mp.nstr(determinants[1], 28)}"]
    lines += ["- 두 정밀도 결과의 최대 절대 차이 < 10^-42: PASS", ""]
    output = "\n".join(lines)
    (folder / "crosscheck.md").write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
