import random, math
from datetime import datetime, timedelta
import pandas as pd

random.seed(2026)

companies = [
 ("Corrib Logistics Ltd","corriblogistics"),("Shannon Dental Group","shannondental"),
 ("Liffey Legal LLP","liffeylegal"),("Burren Foods Ltd","burrenfoods"),
 ("Atlantic Care Clinics","atlanticcare"),("Boyne Engineering","boyneeng"),
 ("Wicklow Print & Pack","wicklowpack"),("Lee Valley Accountants","leevalleyacc"),
 ("Dunmore Pharmacy Group","dunmorepharmacy"),("Slaney Hotels","slaneyhotels"),
 ("Nore Building Supplies","norebuild"),("Suir Veterinary Practice","suirvets"),
 ("Moy Education Trust","moyedu"),("Barrow Auto Parts","barrowauto"),
 ("Erne Property Management","erneproperty"),("Blackwater Dairy Co-op","blackwaterdairy"),
]
first = ["Aoife","Conor","Niamh","Seán","Ciara","Darragh","Orla","Eoin","Sinéad","Cian","Róisín","Declan","Aisling","Padraig","Grace","Mark","Emma","Liam","Sarah","Brian"]
last = ["Murphy","Kelly","O'Brien","Walsh","Byrne","Ryan","Doyle","McCarthy","Gallagher","Kennedy","Lynch","Murray","Quinn","Moore","Brennan"]
devices = ["multifunction printer MFP-4200","label printer LP-330","document scanner DS-12","network switch NS-24","POS terminal PT-80","large-format printer LF-900","projector PJ-550"]
sites = ["Cork office","Galway depot","Dublin head office","Limerick branch","Waterford site","Athlone clinic","Sligo store"]
work = ["print delivery dockets","process patient forms","print invoices","print shipping labels","scan signed contracts","take card payments"]

def sig(): 
    n=f"{random.choice(first)} {random.choice(last)}"; return n
def order(): return f"ORD-{random.randint(10000,99999)}"
def inv(): return f"INV-{random.randint(20000,29999)}"
def dev(): return random.choice(devices)
printers=["multifunction printer MFP-4200","label printer LP-330","large-format printer LF-900"]
def pdev(): return random.choice(printers)

# (category, priority, edge_case, subject, body)
def repair(p):
    d,s,w=dev(),random.choice(sites),random.choice(work)
    if p!="P1": d=pdev()
    if p=="P1":
        opts=[
         (f"URGENT: {d} down at {s}", f"Our {d} at {s} has stopped working completely and we cannot {w}. This is urgent, please send an engineer today.",False),
         (f"{d} not working", f"Since this morning the {d} won't power on and we can't {w} for customers. There is a full queue waiting. Can someone come out as soon as possible?",False),
         (f"No printing at all - tender deadline 3pm", f"Hi, everything stopped printing at {s} about an hour ago and we have a tender to submit by 3pm. Nobody can work around it. Please help.",False),
         (f"Re: ticket from Monday", f"Still nothing. The {d} is dead and the whole team is standing around. We are losing orders. Need someone today.",True),
        ]
    elif p=="P2":
        opts=[
         (f"{d} jamming repeatedly", f"The {d} at {s} jams every few pages. We can use the other unit but it is slowing us down. Could you arrange a repair visit this week?",False),
         (f"Streaks on printouts", f"Prints from the {d} have started to show black streaks. Still usable but not good enough to send to clients. Please advise.",False),
         (f"{d} intermittently offline", f"The {d} drops offline a few times a day. We restart it and it comes back. Can an engineer take a look?",False),
        ]
    else:
        opts=[
         (f"Routine service visit", f"Hi, our {d} at {s} is due its service. Could you let me know available dates next week?",False),
         (f"Toner running low", f"The {d} is showing a low toner warning. Please send a replacement cartridge when you can.",False),
         (f"Strange noise from {d}", f"There is a grinding noise from the {d} when printing, but it still works fine. No rush, just wanted to flag it.",False),
        ]
    s_,b_,e_=random.choice(opts); return "Repair/Fault",p,e_,s_,b_

def orders(p):
    o=order(); d=dev()
    if p=="P2":
        opts=[(f"Delivery not arrived - {o}", f"Order {o} was due yesterday and has not arrived. We need it before Friday's installation or we will have to reschedule staff. Can you check?",False),
              (f"Wrong item delivered {o}", f"We received the wrong model against {o}. We need the correct unit by Thursday for a new starter. Please advise.",False)]
    else:
        q=random.randint(2,15)
        opts=[(f"Order status {o}", f"Hi, could you tell me where order {o} is please? No rush.",False),
              (f"Change delivery address for {o}", f"Please change the delivery address on {o} to our Limerick branch. Thanks.",False),
              (f"Quote request - {q} units of {d}", f"We are looking to buy {q} units of the {d}. Could you send a quote with lead times?",False),
              (f"Remove item from {o}", f"Please remove the extra cable kit from {o}, ordered by mistake.",False)]
    s_,b_,e_=random.choice(opts); return "Order/Delivery",p,e_,s_,b_

def billing(p):
    i=inv()
    if p=="P2":
        opts=[(f"Charged twice - {i}", f"Our card was charged twice for {i}. Please refund the duplicate payment as soon as possible, our finance team needs it reconciled this week.",False)]
    else:
        opts=[(f"Query on {i}", f"Hi, the amount on {i} looks higher than the quote we agreed. Could you send a breakdown?",False),
              (f"Copy of invoice {i}", f"Can you resend {i}? We cannot find the original.",False),
              (f"Update PO number", f"Please add PO number {random.randint(4000,4999)} to {i} and resend.",False),
              (f"Credit note request", f"We returned the faulty cable kit on {i}. Please issue a credit note.",False),
              (f"Invoice and printer issue", f"{i} shows a service call we never had. Also our printer is still making noise. Can you look at both?",True)]
    s_,b_,e_=random.choice(opts); return "Billing/Invoice",p,e_,s_,b_

def technical(p):
    d=dev()
    if p=="P1":
        opts=[(f"Nobody can log in to print management", f"The print management server is down and all 60 staff are locked out of printing across sites. We need this fixed urgently.",False)]
    elif p=="P2":
        opts=[(f"Can't connect {d} after update", f"Since the Windows update last night staff cannot print from their laptops to the {d}. Some colleagues can still print from the shared PC. Please help this week.",False)]
    else:
        opts=[(f"Scan-to-email setup", f"How do I set up scan-to-email on the {d}? We have the SMTP details.",False),
              (f"Driver for Windows 11", f"Where can I download the driver for the {d} for Windows 11?",False),
              (f"Training for new staff", f"Could you run a short training session for 3 new starters on the {d}?",False),
              (f"Wi-Fi printing question", f"Is it possible to print from phones to the {d}? Not urgent.",False)]
    s_,b_,e_=random.choice(opts); return "Technical Support",p,e_,s_,b_

def complaint(p):
    if p=="P1":
        opts=[(f"Formal complaint - considering cancelling contract", f"This is the third time our issue has gone unresolved and we have lost a week of work. If it is not fixed immediately we will cancel our contract. Please escalate to your manager.",False),
              (f"Escalation", f"No one has called back in 3 days. Our director is asking why we pay for this service. We expect a call within the hour.",True)]
    else:
        opts=[(f"Very disappointed with service", f"Your engineer missed our appointment twice this month and nobody told us. This is not acceptable. Please call me.",False),
              (f"Complaint about response times", f"We emailed on Tuesday and have had no reply. This is the second time we have had to chase.",False),
              (f"Feedback on last visit", f"The engineer left the site untidy and the problem came back after one day. We would like a follow-up visit.",False)]
    s_,b_,e_=random.choice(opts); return "Complaint",p,e_,s_,b_

cat_funcs={"Repair/Fault":repair,"Order/Delivery":orders,"Billing/Invoice":billing,"Technical Support":technical,"Complaint":complaint}
cat_w={"Repair/Fault":0.30,"Order/Delivery":0.22,"Billing/Invoice":0.18,"Technical Support":0.20,"Complaint":0.10}
prio_w={
 "Repair/Fault":{"P1":0.22,"P2":0.38,"P3":0.40},
 "Order/Delivery":{"P1":0.0,"P2":0.15,"P3":0.85},
 "Billing/Invoice":{"P1":0.0,"P2":0.10,"P3":0.90},
 "Technical Support":{"P1":0.04,"P2":0.20,"P3":0.76},
 "Complaint":{"P1":0.20,"P2":0.80,"P3":0.0},
}
def pick(d): 
    return random.choices(list(d),weights=list(d.values()))[0]

def typo(t):
    chars=list(t)
    for _ in range(random.randint(2,4)):
        i=random.randint(1,len(chars)-3)
        if chars[i].isalpha() and chars[i+1].isalpha():
            chars[i],chars[i+1]=chars[i+1],chars[i]
    return "".join(chars)

days=[datetime(2026,10,d) for d in (12,13,14,15,16,19,20,21)]
day_w=[1.3,1.1,1.0,1.0,0.8,1.2,1.0,1.0]
hour_w={7:1,8:4,9:10,10:11,11:8,12:5,13:7,14:9,15:9,16:6,17:3,18:1}
sla={"P1":60,"P2":240,"P3":480}
med={"P1":80,"P2":260,"P3":420}; sig_={"P1":0.8,"P2":0.7,"P3":0.6}

rows=[]
N=300
for n in range(N):
    cat=random.choices(list(cat_w),weights=list(cat_w.values()))[0]
    pr=pick(prio_w[cat])
    c,p,edge,subj,body=cat_funcs[cat](pr)
    comp,dom=random.choice(companies); nm=sig()
    email=f"{nm.split()[0].lower().replace('é','e').replace('á','a').replace('ó','o')}.{nm.split()[1].lower().replace(chr(39),'')}@{dom}.example"
    body=f"Hi team,\n\n{body}\n\nKind regards,\n{nm}\n{comp}"
    if random.random()<0.05:
        body=typo(body); edge=True
    day=random.choices(days,weights=day_w)[0]
    h=random.choices(list(hour_w),weights=list(hour_w.values()))[0]
    ts=day+timedelta(hours=h,minutes=random.randint(0,59))
    resp=max(5,int(random.lognormvariate(math.log(med[p]),sig_[p])))
    rows.append(dict(received_at=ts,customer=comp,sender_email=email,subject=subj,body=body,
        true_category=c,true_priority=p,edge_case="Yes" if edge else "No",
        sla_target_min=sla[p],manual_first_response_min=resp))
df=pd.DataFrame(rows).sort_values("received_at").reset_index(drop=True)
df.insert(0,"ticket_id",[f"T{str(i+1).zfill(4)}" for i in range(len(df))])
df["received_at"]=df["received_at"].dt.strftime("%Y-%m-%d %H:%M")
df.to_csv("service_tickets_synthetic.csv",index=False,encoding="utf-8-sig")

print(df.shape)
print(df.true_category.value_counts())
print(df.true_priority.value_counts())
print(df.edge_case.value_counts())
df["breach"]=df.manual_first_response_min>df.sla_target_min
print(df.groupby("true_priority").breach.mean().round(2))
print("overall breach",round(df.breach.mean(),2))
print(df.groupby("true_priority").manual_first_response_min.median())
print(df.iloc[0][["subject","body"]].to_dict())
