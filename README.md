# Service Request Triage Assistant

A prototype that triages customer-service emails: it recommends a **category**, a **priority**, the **SLA target** and whether the email should go to a **human** or is safe to auto-draft. It compares a simple **keyword-rules baseline** with an **AI reading** (Claude) of the same email, and an **Excel dashboard** shows how often first responses met their SLA.

> **All data is synthetic.** The 300 emails, companies and people are fictional. No real customer data was used.

![SLA dashboard](images/sla_dashboard.png)

## The problem

A company that sells and repairs office equipment receives about 40 service emails a day in one shared mailbox. Two coordinators read, categorise and prioritise each one by hand. In the simulated data, **44% of first responses missed their SLA**, and the most urgent emails were the most likely to be late.

| Priority | Meaning | First-response target (SLA) | SLA met today |
|---|---|---|---|
| P1 | Equipment down, business blocked | 60 min | 34.6% |
| P2 | Degraded service, late delivery, double charge, clear complaint | 240 min | 46.1% |
| P3 | Routine request | 480 min | 63.2% |

## What is in this repo

| File | What it is |
|---|---|
| `Service_Request_Triage_Case_Study.docx` | Full write-up: method, results, failure analysis, limitations |
| `service_tickets_synthetic.csv` | 300 simulated emails with correct labels, SLA target and simulated manual response time |
| `gen_tickets.py` | Script that generates the dataset (fixed random seed, so it reproduces the CSV exactly) |
| `rules_v1.py` | Layer 1: keyword-rules classifier and evaluation |
| `tickets_rules_v1_results.csv` | Rules predictions next to the correct labels |
| `triage_assistant.html` | Source of the side-by-side demo page (rules vs AI) |
| `SLA_Dashboard.xlsx` | Formula-driven Excel dashboard with editable what-if assumptions |
| `images/` | Screenshots used in this README |

## How it works

1. **Rules (Python):** keyword lists per category and priority. Anything urgent, any complaint, and anything the rules are unsure about is routed to a human.
2. **AI reading (Claude):** the same email and the same category, priority and SLA definitions are given to Claude, which returns category, priority, routing, a one-sentence reason and a draft reply.
3. **Safeguard:** every draft reply is marked “needs human review”. Nothing is sent automatically.

## Results

**Rules on the full synthetic dataset:** 97.7% category accuracy, 89.3% priority accuracy, and all 26 urgent (P1) emails were flagged for a human. These numbers are optimistic: the data is template-based and the rules were written after seeing how it was generated.

**Seven hand-picked difficult emails, rules vs AI:**

| | Keyword rules | AI (Claude) |
|---|---|---|
| Category correct | 5 of 7 | 7 of 7 |
| Priority correct | 3 of 7 | 6 of 7 |

This is a set of difficult cases chosen after I knew where the rules struggled. It illustrates failure patterns; it is **not** a statistical measure and does not show that AI is generally more accurate.

What the failures showed:

- **Negation:** “Not urgent” was read as urgent.
- **Everyday phrases:** “as soon as possible” is not a reliable urgency signal.
- **Wrong context:** “losing orders” pushed a broken-machine email into the order queue.
- **Tone:** a polite but serious complaint was under-prioritised.
- **Typos:** one correct result was luck (“dead” appears inside the typo “deadlien”), and heavier misspellings were missed.
- **A risk AI adds:** draft replies sometimes made promises the business may not keep (for example “within the hour” or “immediate repair or replacement”), so drafts always need human review.

| Rules flag a routine email as urgent | Rules under-prioritise a complaint | Rules cannot read heavy typos |
|---|---|---|
| ![Case 1](images/case1_negation.png) | ![Case 3](images/case3_polite_complaint.png) | ![Case 7](images/case7_typos.png) |

**What-if scenario (an assumption, not a result):** the dashboard lets you set how much faster the first response would be if urgent emails were recognised and routed immediately. With the example settings (P1 60% faster, P2 30% faster), overall SLA met would rise from 55.7% to 66.3%. These time savings are my assumptions and are not measured effects.

## Run it yourself

```bash
pip install -r requirements.txt
python gen_tickets.py     # optional: regenerates service_tickets_synthetic.csv
python rules_v1.py        # prints accuracy and writes tickets_rules_v1_results.csv
```

No installation needed: both scripts also run in [Google Colab](https://colab.research.google.com) (upload the files, then run `!python rules_v1.py`).

**Demo page:** [Service Request Triage Assistant](https://claude.ai/artifact/5Xg5qmiM6P3NUJkMe2vxVP). The AI panel needs a Claude sign-in; the rules panel works without it. Opening `triage_assistant.html` on its own shows the rules panel only.

## Limitations

- Synthetic, template-based data: real emails are messier, so real accuracy would likely be lower.
- The seven-case comparison is small, hand-picked and not repeated; AI answers can vary between runs.
- SLA covers first response only, with no working-hours, weekend or holiday adjustment.
- The dashboard uses the dataset’s correct labels, not the triage tool’s output, so it shows the size of the problem rather than the tool’s accuracy.
- A real deployment would need a data-protection (GDPR) review before customer emails are sent to an AI service.

## Next steps

Run the AI on all 32 difficult emails with repeated runs; improve the rules (negation, common phrases, typo tolerance); restrict draft wording so replies acknowledge and route but never commit to repairs, refunds or timeframes; pilot with real mailbox data and a human in the loop.

## Built with

Python (pandas), Excel, and Claude. The code and dashboard were built with AI assistance (vibe coding). I defined the scenario, categories, priority and SLA rules and human-review rules, then tested the outputs against expected answers and documented the results.

**Author:** Xinyi Zhang, MSc Information Systems Management, University of Galway.
