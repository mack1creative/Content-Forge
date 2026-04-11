# Lead Nurture AI - Technical Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        LEAD NURTURE AI                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Zillow  │    │ Facebook │    │  Realtor │    │ Referral │  │
│  │    API   │    │   Ads    │    │   .com   │    │  Source  │  │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘  │
│       │               │               │               │         │
│       └───────────────┴───────────────┴───────────────┘         │
│                               │                                  │
│                       ┌───────▼───────┐                         │
│                       │  Webhook API  │                         │
│                       │  (Lead In)    │                         │
│                       └───────┬───────┘                         │
│                               │                                  │
│       ┌───────────────────────┼───────────────────────┐        │
│       │                       │                       │        │
│  ┌────▼────┐            ┌─────▼─────┐           ┌─────▼────┐   │
│  │  Phone  │            │    Text   │           │  Email   │   │
│  │ Twilio  │            │  Twilio   │           │ SendGrid │   │
│  └────┬────┘            └─────┬─────┘           └─────┬────┘   │
│       │                        │                       │        │
│       └────────────────────────┼───────────────────────┘        │
│                                │                                 │
│                       ┌────────▼────────┐                       │
│                       │   AI Processing │                       │
│                       │   (OpenAI)      │                       │
│                       └────────┬────────┘                       │
│                                │                                 │
│       ┌────────────────────────┼────────────────────────┐       │
│       │                        │                        │       │
│  ┌────▼────┐            ┌─────▼─────┐           ┌─────▼────┐  │
│  │ CRM     │            │ Calendar  │           │Dashboard │  │
│  │ Update  │            │ Booking   │           │ Display  │  │
│  └─────────┘            └───────────┘           └──────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Webhook Receiver (Python/FastAPI)
- Receives leads from any source
- Validates and normalizes data
- Queues for processing

### 2. Lead Processor (Python)
- Determines best channel (phone first, then text, then email)
- Generates AI prompts based on lead source/message
- Calls OpenAI API for response generation

### 3. Communication Layer
- **Phone**: Twilio Voice API
- **SMS**: Twilio SMS API  
- **Email**: SendGrid API

### 4. AI Brain (OpenAI GPT-4)
- System prompt: Real estate agent persona
- Lead qualification logic
- Response generation
- Calendar scheduling logic

### 5. CRM Integration
- HubSpot, Salesforce, Zoho, or custom
- Creates/updates lead records
- Logs all interactions

### 6. Dashboard
- Real-time lead status
- Performance metrics
- Agent notifications

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11 + FastAPI |
| AI | OpenAI GPT-4o |
| Phone/SMS | Twilio |
| Email | SendGrid |
| Database | PostgreSQL (Supabase) |
| Hosting | Railway / Render / Fly.io |
| CRM | HubSpot API |
| Calendar | Google Calendar API |

---

## API Endpoints

### POST /webhook/lead
Receive new lead from any source

### POST /webhook/test
Test endpoint

### GET /leads
List all leads

### GET /leads/{id}
Get lead details

### POST /trigger/call
Manually trigger a call

### GET /analytics
Get performance metrics

---

## Data Model

### Lead
- id: UUID
- name: string
- phone: string
- email: string
- source: string
- message: string
- status: enum (new, contacted, qualified, showing, contracted, closed, lost)
- score: integer (0-100)
- budget: string
- beds_required: integer
- timeline: string
- preapproval_status: string
- created_at: timestamp
- updated_at: timestamp
- agent_id: UUID

### Interaction
- id: UUID
- lead_id: UUID
- channel: enum (phone, text, email)
- direction: enum (inbound, outbound)
- content: text
- timestamp: timestamp

### Appointment
- id: UUID
- lead_id: UUID
- scheduled_at: timestamp
- status: enum (scheduled, confirmed, completed, cancelled)
- notes: text