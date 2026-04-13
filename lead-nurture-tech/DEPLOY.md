# Deployment Guide: Lead Nurture AI

## Quick Deploy to Render (Free)

### Option 1: One-Click Deploy
1. Go to: https://dashboard.render.com/deploy
2. Connect your GitHub account
3. Select this repo: `mack1creative/Content-Forge`
4. Set branch: `master`
5. Root directory: `lead-nurture-tech`
6. Build command: `pip install -r requirements.txt`
7. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
8. Click Deploy

### Option 2: Manual Deploy
```bash
# Clone the repo
git clone https://github.com/mack1creative/Content-Forge.git
cd Content-Forge/lead-nurture-tech

# Create .env file (copy from .env.example and fill in)
cp .env.example .env

# Deploy to Render via their CLI or dashboard
```

---

## After Deploy: Get Your Webhook URL

Once deployed, you'll get a URL like:
`https://lead-nurture-ai.onrender.com`

**Your webhook endpoint:**
```
POST https://lead-nurture-ai.onrender.com/webhook/lead
```

---

## Twilio Setup (For SMS/Phone)

### Step 1: Create Twilio Account
1. Go to https://www.twilio.com
2. Sign up for free account
3. Verify your phone number

### Step 2: Get Credentials
From Twilio Console (https://console.twilio.com):

| Credential | Where to Find |
|------------|---------------|
| Account SID | Console → Account → Dashboard |
| Auth Token | Console → Account → Dashboard |
| Phone Number | Console → Phone Numbers → Get a Number |

### Step 3: Update .env
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

---

## SendGrid Setup (For Emails)

### Step 1: Create SendGrid Account
1. Go to https://sendgrid.com
2. Sign up for free account
3. Verify sender identity (single sender)

### Step 2: Get API Key
- Settings → API Keys → Create API Key
- Copy the key (only shown once!)

### Step 3: Update .env
```
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## OpenAI Setup (For AI Responses)

### Step 1: Get API Key
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy the key (only shown once!)

### Step 2: Update .env
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Testing the Webhook

Once deployed, test with:

```bash
curl -X POST https://YOUR-APP.onrender.com/webhook/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Lead",
    "phone": "+13525550142",
    "email": "test@example.com",
    "source": "facebook",
    "message": "Interested in Clermont homes"
  }'
```

Expected response:
```json
{
  "id": "uuid-here",
  "name": "Test Lead",
  "status": "new",
  ...
}
```

---

## Checklist

- [ ] Deploy to Render
- [ ] Get webhook URL
- [ ] Create Twilio account (phone, SMS)
- [ ] Create SendGrid account (email)
- [ ] Get OpenAI API key
- [ ] Add all env vars to Render dashboard
- [ ] Test webhook with curl
- [ ] Find beta agent
- [ ] Connect agent's leads