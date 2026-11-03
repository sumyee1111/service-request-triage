import re
import pandas as pd

df = pd.read_csv("service_tickets_synthetic.csv")

# ---------- Layer 1: keyword rules ----------
CATEGORY_KEYWORDS = {
    "Complaint": ["complaint", "disappointed", "not acceptable", "cancel our contract", "escalat",
                  "chase", "no reply", "unresolved", "feedback", "missed our appointment", "director"],
    "Billing/Invoice": ["invoice", "inv-", "credit note", "refund", "charged", "po number", "payment", "billing"],
    "Order/Delivery": ["order", "ord-", "delivery", "delivered", "quote", "arrive", "shipping address"],
    "Technical Support": ["how do i", "driver", "set up", "setup", "training", "wi-fi", "log in",
                          "connect", "print management", "windows", "is it possible"],
    "Repair/Fault": ["not working", "down", "jam", "streak", "noise", "toner", "service visit",
                     "stopped", "offline", "engineer", "repair", "dead", "power on", "service"],
}
TIE_ORDER = ["Complaint", "Billing/Invoice", "Order/Delivery", "Technical Support", "Repair/Fault"]

P1_KEYWORDS = ["urgent", "cancel our contract", "escalat", "locked out", "completely", "as soon as possible", "dead"]
P2_KEYWORDS = ["jam", "streak", "offline", "not arrived", "charged twice", "missed", "wrong item",
               "disappointed", "complaint", "chase", "slowing us down", "cannot print", "can't connect", "this week"]

def classify(subject, body):
    text = f"{subject} {body}".lower()
    subj = subject.lower()
    scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        s = 0
        for kw in kws:
            if kw in subj: s += 2
            elif kw in text: s += 1
        scores[cat] = s
    best = max(scores.values())
    if best == 0:
        return "Unclassified", "P3", True
    top = [c for c in TIE_ORDER if scores[c] == best]
    cat = top[0]
    tie = len(top) > 1

    if any(k in text for k in P1_KEYWORDS):
        pr = "P1"
    elif any(k in text for k in P2_KEYWORDS):
        pr = "P2"
    else:
        pr = "P3"

    # human-review rule: anything urgent, any complaint, or an unsure category
    needs_human = pr == "P1" or cat == "Complaint" or tie or best < 2
    return cat, pr, needs_human

res = df.apply(lambda r: classify(r["subject"], r["body"]), axis=1, result_type="expand")
df["pred_category"], df["pred_priority"], df["needs_human"] = res[0], res[1], res[2]
df["category_ok"] = df.pred_category == df.true_category
df["priority_ok"] = df.pred_priority == df.true_priority
df.to_csv("tickets_rules_v1_results.csv", index=False, encoding="utf-8-sig")

# ---------- Evaluation ----------
print("Category accuracy:", round(df.category_ok.mean(), 3))
print("Priority accuracy:", round(df.priority_ok.mean(), 3))
print("\nBy edge_case:\n", df.groupby("edge_case")[["category_ok", "priority_ok"]].mean().round(2))
print("\nCategory accuracy by true category:\n", df.groupby("true_category").category_ok.mean().round(2))
print("\nPriority confusion (rows=true, cols=pred):\n", pd.crosstab(df.true_priority, df.pred_priority))
print("\nP1 recall (true P1 predicted P1):",
      round(((df.true_priority=="P1")&(df.pred_priority=="P1")).sum()/(df.true_priority=="P1").sum(),2))
print("P1 caught by human-review flag:",
      round(((df.true_priority=="P1")&(df.needs_human)).sum()/(df.true_priority=="P1").sum(),2))
print("Share flagged for human:", round(df.needs_human.mean(), 2))
print("\nUnclassified:", (df.pred_category=="Unclassified").sum())
