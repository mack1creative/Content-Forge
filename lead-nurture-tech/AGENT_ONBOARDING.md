# Setting Up Lead Nurture AI for an Agent
## Step-by-Step Guide + Agent Experience

---

## Part 1: Setup Steps

### Phase 1: Pre-Requisites (You handle this)

| Step | What | Who Does It |
|------|------|-------------|
| 1 | Create Twilio account | You |
| 2 | Get phone number, Account SID, Auth Token | You |
| 3 | Create SendGrid account | You |
| 4 | Get SendGrid API key | You |
| 5 | Add env vars to Render dashboard | You |

### Phase 2: Connect Agent (You + Agent)

| Step | What | Agent Does | Time |
|------|------|------------|------|
| 1 | Give agent webhook URL | Nothing | 1 min |
| 2 | Agent connects lead sources | Updates Zillow/Realtor settings to send webhooks | 5 min |
| 3 | Agent provides: team name, agent phone, notification preferences | Fills short form | 2 min |
| 4 | Test with 1 sample lead | You | 2 min |

### Phase 3: Go Live

| Step | What | Time |
|------|------|------|
| 1 | Agent starts sending leads to webhook | Ongoing |
| 2 | AI responds within 30 seconds | Automatic |
| 3 | You monitor dashboard for hot leads | Daily check |

---

## Part 2: Agent Visualization

### What the Agent SEES

#### 1. Dashboard (Web or App)
```
┌─────────────────────────────────────────────────────────────┐
│  LEAD NURTURE AI         │  Agent: [Team Name]  │  Logout  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 TODAY'S METRICS                                         │
│  ┌──────────┬──────────┬──────────┬──────────┐             │
│  │ 24 Leads │ 8 Hot    │ 6 Showings│ $2.1M    │             │
│  │   Today  │ Qualified │  Booked   │ Pipeline │             │
│  └──────────┴──────────┴──────────┴──────────┘             │
│                                                             │
│  🔥 HOT LEADS (Score 85+)                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Michael Chen    │ 90/100 │ +352 555-0199 │ IMMEDIATE  │ │
│  │ Looking: 4BR/$400k Clermont                             │ │
│  │ [Call Now]  [Schedule Showing]  [View Details]         │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Lisa Ray       │ 90/100 │ +352 555-0777 │ IMMEDIATE    │ │
│  │ Looking: 3BR/$325k Clermont                             │ │
│  │ [Call Now]  [Schedule Showing]  [View Details]         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  📋 ALL LEADS (12)                                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ ● Sarah Johnson  55/100  Warm   Message sent           │ │
│  │ ● John Smith     40/100  Cold   No response           │ │
│  │ ● Tom Hardy     70/100  Warm   In nurture             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 2. Text Message Alert (Hot Lead)
```
📱 TEXT from Lead Nurture AI:

🔥 HOT LEAD ALERT

Name: Michael Chen
Phone: (352) 555-0199
Score: 90/100

Budget: $400k | Beds: 4 | Timeline: Immediate
Pre-approval: YES

Message: "I'm ready to buy ASAP. Have my 
pre-approval letter. Looking for 4 bed in 
Clermont under $400k"

Suggested Script:
"Hi Michael! I saw you're ready to buy - 
I've got some great listings that match. 
When can we get you in for a showing?"
```

#### 3. Email Digest (Morning)
```
Subject: Morning Lead Digest - 8 Hot Leads Today

Good morning! Here's your lead summary:

🔥 HOT LEADS (Require Immediate Action)
1. Michael Chen - 90/100 - (352) 555-0199
2. Lisa Ray - 90/100 - (352) 555-0777
3. David Kim - 87/100 - (352) 555-0333

📋 WARM LEADS (Nurture)
- Sarah Johnson - 55/100 - In sequence
- Tom Hardy - 70/100 - Day 3 follow-up

📊 THIS WEEK
- Total Leads: 156
- Hot: 24 (15%)
- Showings Booked: 18
- Contracts Written: 4

[View Full Dashboard →]
```

---

## Part 3: Agent's Daily Workflow

### Morning (2 min)
Check hot leads → Call the top 3 → Schedule showings

### During the Day
- Get text alerts for new hot leads
- AI handles all follow-up automatically

### Weekly
Review dashboard → Adjust nurture sequences if needed

### What the Agent NEVER Has to Do:
❌ Manually text leads
❌ Remember to follow up
❌ Enter data into CRM
❌ Write listing descriptions
❌ Send market updates manually

---

## Part 4: Connecting Lead Sources

### Zillow
1. Go to Zillow Lead Builder
2. Edit lead notification settings
3. Add webhook URL: `https://content-forge-yugd.onrender.com/webhook/lead`

### Realtor.com
1. Account Settings → Lead Routing
2. Add custom webhook

### Facebook Ads
1. Go to Facebook Lead Forms
2. Set up automated webhook delivery

### Referral
1. Agent enters lead manually or forwards email

---

## Summary for Agent

| What | Cost |
|------|------|
| Monthly Subscription | $249/mo |
| What It Does | Auto-responds to every lead within 30 seconds |
| What They Get | Text/email alerts for hot leads, dashboard |
| What They Do | Show houses, close deals |
| What They Save | ~10 hours/week on follow-up |

---

*Ready to onboard your first agent? Let me know and I'll walk through the exact form to collect their info.*