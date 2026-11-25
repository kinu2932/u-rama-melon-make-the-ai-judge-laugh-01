#!/usr/bin/env python3
"""Local grader mirror for 'Make the AI Judge Laugh'.

Round-robin duel tournament over 14 candidate one-liners.
Each candidate is scored 0-5 on the judge brief's four criteria, in the
brief's priority order, with weights truth=3, surprise=3, tightness=2,
freshness=2. Every pair plays twice (both orders, like the real judge);
winner takes the game, margin = score gap scaled 1-5. Deterministic:
no randomness, no time, no network. Run 3x and diff the outputs.
"""
import json

# (text, truth, surprise, tightness, freshness) — scores are the rubric
# judgements encoded once, here; the tournament itself is pure arithmetic.
CANDIDATES = [
    ("I told my boss I work best under pressure, so now every deadline is a surprise party nobody invited me to.", 4, 4, 3, 3),
    ("Our office printer only works when nobody needs it, which is why HR keeps it next to the fire extinguisher.", 5, 3, 3, 3),
    ("My calendar is just meetings about meetings, with a 15-minute meeting to discuss why we have so many meetings.", 5, 2, 4, 2),
    ("We have an open-plan office so everyone can hear exactly how little work gets done, out loud, in surround sound.", 4, 3, 3, 3),
    ("My boss said his door is always open, so I walked in and found out it is open because the hinges broke in 2019.", 4, 4, 3, 4),
    ("The printer jammed again, so IT filed a ticket to fix the ticket system, which is also jammed.", 4, 4, 4, 4),
    ("I asked for a raise and my manager gave me a standing desk, because apparently standing is the new salary.", 4, 4, 4, 4),
    ("Our team-building exercise was trust falls, which is ironic because nobody here trusts the Wi-Fi.", 4, 4, 4, 3),
    ("I put 'excellent communicator' on my CV because I can say 'per my last email' in seven tones of voice.", 5, 4, 4, 4),
    ("My out-of-office reply is the most honest thing I have written all year, and it is automated.", 4, 3, 4, 3),
    ("The office plant died, so HR held a wellness seminar about it instead of watering the next one.", 4, 4, 3, 4),
    ("I survived another meeting that should have been an email by pretending my camera froze for 47 minutes.", 5, 3, 4, 3),
    ("Our boss calls it synergy; the rest of us call it four people doing one person's job while he takes the credit.", 5, 2, 3, 2),
    ("The coffee machine broke, so now the whole office communicates exclusively through passive-aggressive sticky notes.", 4, 3, 3, 3),
]

WEIGHTS = (3, 3, 2, 2)


def total(c):
    return sum(s * w for s, w in zip(c[1:], WEIGHTS))


def main():
    for i, c in enumerate(CANDIDATES, 1):
        assert 1 <= len(c[0]) <= 199, f"candidate {i} length {len(c[0])}"
        assert "\n" not in c[0], f"candidate {i} not one line"
    totals = {i: total(c) for i, c in enumerate(CANDIDATES, 1)}
    wins = {i: 0 for i in totals}
    points = {i: 0.0 for i in totals}
    games = []
    for a in range(1, len(CANDIDATES) + 1):
        for b in range(a + 1, len(CANDIDATES) + 1):
            # two calls, one in each order — same deterministic verdict both ways
            for _order in (0, 1):
                gap = totals[a] - totals[b]
                if gap > 0:
                    winner, loser = a, b
                elif gap < 0:
                    winner, loser = b, a
                else:
                    winner = None
                margin = min(5, max(1, abs(gap) // 2)) if gap else 0
                if winner is None:
                    points[a] += 0.5
                    points[b] += 0.5
                else:
                    wins[winner] += 1
                    points[winner] += 0.5 + margin / 10.0
                    points[loser] += 0.5 - margin / 10.0
            games.append((a, b, totals[a], totals[b]))
    ranking = sorted(totals, key=lambda i: (-points[i], -wins[i], totals[i], i))
    out = {
        "candidates": [
            {"n": i, "chars": len(c[0]), "truth": c[1], "surprise": c[2],
             "tightness": c[3], "freshness": c[4], "total": totals[i],
             "wins": wins[i], "points": round(points[i], 2), "text": c[0]}
            for i, c in enumerate(CANDIDATES, 1)
        ],
        "ranking": ranking,
        "winner": ranking[0],
        "games_played": len(games) * 2,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
