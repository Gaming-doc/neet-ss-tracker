import plan as P
from data import main, qrp, qrp_recall_by_day
P.avail["Nephro"] = 18
PYQ = {9: "NEET SS 2022 PYQ (150 Qs)", 17: "NEET SS 2023 PYQ (150 Qs)", 24: "NEET SS 2024 PYQ (150 Qs)"}

def build(cap=140):
    plan = {d: [] for d in range(1, 29)}
    plan[1] = P.ss[1]; plan[2] = P.ss[2]
    queue = [[b, P.merged[b], 0] for b in P.order if not b.startswith("Cardio")]
    for d in range(3, 29):
        room = 0 if d in PYQ else (cap if d < 28 else 200)
        for item in queue:
            if room <= 0: break
            b, tot, done = item
            if done >= tot or P.avail_day(b) > d: continue
            take = min(tot - done, room)
            if 0 < tot - done - take < 12: take = tot - done
            if take < 15 and take < tot - done: break
            label = b if (take == tot and done == 0) else f"{b} (Q{done+1}–{done+take})"
            plan[d].append((label, take)); item[2] += take; room -= take
    assert sum(t - dn for _, t, dn in queue) == 0
    return plan

SS = build()
def day2_rest():
    return [("Cardio: Pulm HTN",47),("Cardio: Myocarditis & CMP",27),("Cardio: DVT & PE",51),("CVS: Arrhythmias",14)]

rows = []
for d in range(2, 29):
    if d == 2:
        bl = {"A": [], "B": [], "C": []}
        mods = day2_rest()
    else:
        bl = P.blocks(d); mods = None
    rows.append(dict(day=d, date=P.date(d), blocks=bl, mods=mods,
        main=sum(n for _, n in P.main[d]), ss=SS[d], ssn=sum(n for _, n in SS[d]),
        qrp=[(k, *qrp[k]) for k in qrp_recall_by_day[d]], qrpn=sum(qrp[k][1] for k in qrp_recall_by_day[d]),
        pyq=PYQ.get(d)))
if __name__ == "__main__":
    tm = 53 + 162 + sum(r["main"] for r in rows)
    tss = sum(r["ssn"] for r in rows) + 95
    print("main", tm, "ss", tss, "qrp", 44 + sum(r["qrpn"] for r in rows))
    for r in rows:
        print(r["day"], r["date"].strftime("%a %b %d"), r["main"], r["ssn"], r["qrpn"], r["pyq"] or "")
        if r["mods"] is None:
            for b in "ABC": print("   ", b, r["blocks"][b])
        print("    SS", r["ss"])
