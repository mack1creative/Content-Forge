"""
Lead Nurture AI - Core Application
Automated Follow-Up Engine for Real Estate Agents
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn

# ==================== ENUMS ====================

class LeadSource(str, Enum):
    ZILLOW = "zillow"
    FACEBOOK = "facebook"
    REALTOR = "realtor"
    REFERRAL = "referral"
    DIRECT = "direct"
    GOOGLE = "google"

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    SHOWING = "showing"
    CONTRACTED = "contracted"
    CLOSED = "closed"
    LOST = "lost"

class Channel(str, Enum):
    PHONE = "phone"
    TEXT = "text"
    EMAIL = "email"

# ==================== IN-MEMORY DATABASE ====================

leads_db = {}
interactions_db = []

# ==================== PYDANTIC MODELS ====================

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    source: LeadSource
    message: Optional[str] = None
    agent_id: str = "default"

class LeadResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: Optional[str]
    source: LeadSource
    message: Optional[str]
    status: LeadStatus
    score: int
    budget: Optional[str]
    timeline: Optional[str]
    beds_required: Optional[int]
    preapproval_status: Optional[str]
    created_at: datetime
    updated_at: datetime

# ==================== HELPER FUNCTIONS ====================

def parse_message_for_qualification(message: str) -> dict:
    """Parse lead message to extract qualification data"""
    if not message:
        return {}
    
    msg = message.lower()
    result = {}
    
    # Extract budget
    import re
    budget_match = re.search(r'\$?(\d{2,3})k', msg) or re.search(r'(\d{2,3}),?\d{3}', msg)
    if budget_match:
        result['budget'] = f"${budget_match.group(1)}k"
    
    # Extract beds
    beds_match = re.search(r'(\d+)\s*(bed|br|bedroom)', msg)
    if beds_match:
        result['beds_required'] = int(beds_match.group(1))
    
    # Extract timeline
    if 'immediate' in msg or 'asap' in msg or 'now' in msg:
        result['timeline'] = 'immediate'
    elif '1-3' in msg or 'two months' in msg or 'next 2' in msg:
        result['timeline'] = '1-3 months'
    elif '3-6' in msg or 'months' in msg:
        result['timeline'] = '3-6 months'
    elif '6+' in msg or 'year' in msg:
        result['timeline'] = '6+ months'
    
    # Extract pre-approval
    if 'pre-approval' in msg or 'preapproval' in msg or 'pre approved' in msg:
        if 'have' in msg or 'got' in msg or 'already' in msg:
            result['preapproval_status'] = 'yes'
        elif 'working' in msg or 'process' in msg:
            result['preapproval_status'] = 'in process'
    
    return result

def calculate_lead_score(lead_data: dict) -> int:
    """Calculate lead score based on qualification factors"""
    score = 0
    
    # Timeline scoring
    timeline = lead_data.get("timeline", "").lower()
    if "immediate" in timeline:
        score += 30
    elif "1-3" in timeline or "1-3mo" in timeline:
        score += 20
    elif "3-6" in timeline:
        score += 10
    elif timeline:
        score += 5
    
    # Pre-approval scoring
    preapproval = lead_data.get("preapproval_status", "").lower()
    if "yes" in preapproval:
        score += 30
    elif "in process" in preapproval or "working" in preapproval:
        score += 15
    
    # Budget clarity
    if lead_data.get("budget"):
        score += 20
    
    # Beds requirement
    if lead_data.get("beds_required"):
        score += 10
    
    return min(score, 100)

def generate_outreach_message(lead: dict, channel: Channel) -> str:
    """Generate initial outreach message based on lead data"""
    name = lead.get("name", "there")
    source = lead.get("source", "your inquiry")
    
    if channel == Channel.TEXT:
        templates = [
            f"Hey {name}! Just saw your inquiry come through from {source} - want me to send you some listings that match what you're looking for?",
            f"Hi {name}! Thanks for reaching out. I can definitely help you find what you need. What's most important to you - price, location, or size?",
            f"Hey {name}! Love that you're looking in the area. Do you have a specific neighborhood or price range in mind?"
        ]
        return templates[hash(lead.get("id", name)) % len(templates)]
    
    elif channel == Channel.EMAIL:
        return f"""Subject: Let's find your perfect home!

Hi {name},

Thanks for your interest! I'd love to help you find the right property.

Based on your inquiry, I've put together some options that might work. What specific criteria are you looking for?

Best,
Mack
Lake County Real Estate"""
    
    else:  # PHONE
        return f"Calling {name} to qualify..."

def format_lead_alert(lead: dict) -> str:
    """Format hot lead alert for agent notification"""
    return f"""🔥 HOT LEAD ALERT

Name: {lead.get('name')}
Phone: {lead.get('phone')}
Score: {lead.get('score')}/100

Details:
- Budget: {lead.get('budget', 'TBD')}
- Needs: {lead.get('beds_required', 'TBD')} bed
- Timeline: {lead.get('timeline', 'TBD')}
- Pre-approval: {lead.get('preapproval_status', 'TBD')}

Message: {lead.get('message', 'N/A')}"""

# ==================== API ENDPOINTS ====================

app = FastAPI(title="Lead Nurture AI", version="1.0.0")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Lead Nurture AI",
        "version": "1.0.0",
        "leads_processed": len(leads_db)
    }

@app.post("/webhook/lead", response_model=LeadResponse)
async def receive_lead(lead_input: LeadCreate, background_tasks: BackgroundTasks):
    """
    Receive a new lead from any source.
    Triggers AI outreach automatically.
    """
    lead_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    lead_data = {
        "id": lead_id,
        "name": lead_input.name,
        "phone": lead_input.phone,
        "email": lead_input.email,
        "source": lead_input.source.value,
        "message": lead_input.message,
        "status": LeadStatus.NEW.value,
        "score": 0,
        "budget": None,
        "timeline": None,
        "beds_required": None,
        "preapproval_status": None,
        "agent_id": lead_input.agent_id,
        "created_at": now,
        "updated_at": now,
    }
    
    leads_db[lead_id] = lead_data
    
    # Trigger AI outreach in background
    background_tasks.add_task(process_lead_outreach, lead_id)
    
    return LeadResponse(**lead_data)

async def process_lead_outreach(lead_id: str):
    """Process lead through AI qualification flow"""
    lead = leads_db.get(lead_id)
    if not lead:
        return
    
    # Parse message for qualification data
    parsed = parse_message_for_qualification(lead.get("message", ""))
    for key, value in parsed.items():
        if not lead.get(key):
            lead[key] = value
    
    # Update status
    lead["status"] = LeadStatus.CONTACTED.value
    lead["updated_at"] = datetime.utcnow()
    
    # Generate initial outreach
    response_text = generate_outreach_message(lead, Channel.TEXT)
    
    # Log interaction
    interaction = {
        "id": str(uuid.uuid4()),
        "lead_id": lead_id,
        "channel": Channel.TEXT.value,
        "direction": "outbound",
        "content": response_text,
        "timestamp": datetime.utcnow().isoformat()
    }
    interactions_db.append(interaction)
    
    # Calculate score
    score = calculate_lead_score(lead)
    lead["score"] = score
    
    # Update status based on score
    if score >= 85:
        lead["status"] = LeadStatus.QUALIFIED.value
        # In production: send agent alert here
        print(f"\n{format_lead_alert(lead)}\n")

@app.get("/leads", response_model=List[LeadResponse])
async def list_leads(status: Optional[LeadStatus] = None, limit: int = 50):
    """List all leads, optionally filtered by status"""
    leads = list(leads_db.values())
    
    if status:
        leads = [l for l in leads if l["status"] == status.value]
    
    leads.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [LeadResponse(**l) for l in leads[:limit]]

@app.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: str):
    """Get specific lead by ID"""
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadResponse(**leads_db[lead_id])

@app.get("/analytics")
async def get_analytics():
    """Get dashboard analytics"""
    leads = list(leads_db.values())
    
    total = len(leads)
    by_status = {}
    by_source = {}
    total_score = 0
    hot_leads = 0
    
    for lead in leads:
        status = lead.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        
        source = lead.get("source", "unknown")
        by_source[source] = by_source.get(source, 0) + 1
        
        total_score += lead.get("score", 0)
        
        if status == "qualified":
            hot_leads += 1
    
    return {
        "total_leads": total,
        "by_status": by_status,
        "by_source": by_source,
        "average_score": round(total_score / total, 1) if total > 0 else 0,
        "hot_leads": hot_leads,
        "interactions_today": len([i for i in interactions_db if i.get("timestamp", "").startswith(datetime.utcnow().strftime("%Y-%m-%d"))])
    }

@app.post("/trigger/call")
async def trigger_call(lead_id: str):
    """Manually trigger a call to a lead"""
    lead = leads_db.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # In production: integrate with Twilio here
    return {
        "status": "initiated",
        "lead_id": lead_id,
        "phone": lead["phone"],
        "message": "Call initiated"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
