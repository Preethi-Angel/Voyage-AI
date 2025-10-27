# 🚀 Amadeus API Quick Start Guide

## ✅ **What Test Data We're Using**

Based on [Amadeus Test Data Catalog](https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/test-data/), we're using **guaranteed test cities** that always return data:

### **Cities in Our Demo:**
- 🇫🇷 **Paris, France** (PAR)
- 🇬🇧 **London, UK** (LON)
- 🇺🇸 **New York, USA** (NYC)
- 🇹🇭 **Bangkok, Thailand** (BKK)

### **Why These Cities?**
✅ Amadeus **guarantees** these work in TEST mode
✅ Cover diverse destinations (Europe, Asia, North America)
✅ Mix of short/long haul flights
✅ Rich activity data available

---

## 📝 **Step-by-Step Setup**

### **Step 1: Get Your TEST API Credentials**

1. Go to: https://developers.amadeus.com/my-apps
2. Click on your app name
3. Find the **"Test"** section (NOT Production)
4. Copy these two values:
   ```
   API Key: xxxxxxxxxxxxxxxxxxx
   API Secret: yyyyyyyyyyyyyyyyyyy
   ```

### **Step 2: Add to .env File**

Edit `/Users/preethiangels/Documents/Tech_Talk_2025/travel-agent-demo/backend/.env`:

```bash
# Amadeus API Configuration (TEST Environment)
AMADEUS_API_KEY=paste_your_test_api_key_here
AMADEUS_API_SECRET=paste_your_test_api_secret_here
```

**Important:** Use **TEST** credentials, not Production!

### **Step 3: Install Amadeus SDK**

```bash
cd /Users/preethiangels/Documents/Tech_Talk_2025/travel-agent-demo/backend
source venv/bin/activate
pip install amadeus requests-cache
```

### **Step 4: Fetch Test Data**

```bash
python -m app.services.real_data_fetcher --refresh
```

**Expected Output:**
```
🔄 Fetching real travel data from Amadeus TEST API...
📚 Using Amadeus guaranteed test data cities

📍 Fetching data for Paris...
✅ Paris: 10 flights, 8 hotels, 15 activities

📍 Fetching data for London...
✅ London: 10 flights, 9 hotels, 13 activities

📍 Fetching data for New York...
✅ New York: 10 flights, 10 hotels, 14 activities

📍 Fetching data for Bangkok...
✅ Bangkok: 10 flights, 7 hotels, 12 activities

✅ Real data cached successfully!
```

### **Step 5: Verify**

```bash
python -m app.services.real_data_fetcher --check
```

**Expected Output:**
```
📊 Cached Data Status:
   Last Updated: 2025-01-27T15:30:00
   Destinations: paris, london, new york, bangkok

   paris:
      Flights: 10
      Hotels: 8
      Activities: 15
```

### **Step 6: Start Backend**

```bash
uvicorn app.main:app --reload
```

**Look for this line:**
```
✅ Using cached REAL travel data from Amadeus API
```

### **Step 7: Check Health Endpoint**

```bash
curl http://localhost:8000/health
```

**Should return:**
```json
{
  "status": "healthy",
  "data_source": {
    "source": "Cached Real Data (Amadeus API)",
    "last_updated": "2025-01-27T15:30:00",
    "destinations": ["paris", "london", "new york", "bangkok"]
  }
}
```

---

## ✅ **You're Done!**

Your application now uses **real Amadeus test data**:
- ✅ Professional-grade travel data
- ✅ Unlimited API calls (test mode)
- ✅ Free forever
- ✅ Realistic prices and routes
- ✅ Cached for fast, reliable demos

---

## 🎬 **For Your Demo**

### **What to Say:**

```
"We're using the Amadeus Travel API - the same infrastructure
powering Booking.com and Expedia. For demo reliability, we're
using their test environment with cached data. This gives us
realistic travel data without worrying about API rate limits
or network issues during the presentation."
```

### **If Asked About Data:**

**Q: "Is this real data?"**
**A:** "It's Amadeus test data - professional-grade synthetic data that
mimics real travel inventory. In production, we'd switch to their live
API for current market rates. The AI orchestration you're seeing is
100% real."

**Q: "How often is it refreshed?"**
**A:** "Weekly. Test data is stable, so we don't need daily updates.
Production mode would query live APIs for each request."

---

## 🔧 **Troubleshooting**

### **Problem: "Amadeus API not configured"**

**Check:**
```bash
cat .env | grep AMADEUS
```

**Should show:**
```
AMADEUS_API_KEY=your_key_here
AMADEUS_API_SECRET=your_secret_here
```

**Fix:** Make sure you copied TEST credentials (not Production)

---

### **Problem: "Authentication failed"**

**Cause:** Wrong credentials or Production credentials in TEST mode

**Fix:**
1. Go back to https://developers.amadeus.com/my-apps
2. Make sure you're copying from **"Test"** section
3. Regenerate keys if needed
4. Update `.env` file

---

### **Problem: "No results found"**

**Cause:** Using non-test cities or wrong airport codes

**Fix:** We've pre-configured guaranteed test cities (PAR, LON, NYC, BKK)
No changes needed!

---

## 📊 **Test vs Production**

| Feature | TEST (Current) | PRODUCTION |
|---------|----------------|------------|
| **API Calls** | Unlimited, Free | 2000 free, then $$ |
| **Data** | Synthetic (realistic) | Live market rates |
| **Best For** | Demos, Testing | Production apps |
| **Setup** | Instant | Requires approval |
| **Credentials** | From "Test" section | From "Production" section |

✅ **We're using TEST** - perfect for your demo!

---

## 🎯 **Supported Demo Scenarios**

With the current test data, you can demo:

✅ **Paris Trip** - European getaway
✅ **London Trip** - UK travel
✅ **New York Trip** - US destination
✅ **Bangkok Trip** - Asian adventure
✅ **Multi-city** - Paris + London combo

All guaranteed to work with realistic data!

---

## 💡 **Pro Tips**

1. **Refresh weekly**: `python -m app.services.real_data_fetcher --refresh`
2. **Check before demos**: `python -m app.services.real_data_fetcher --check`
3. **Test endpoint**: Try `curl http://localhost:8000/health` to verify
4. **Backup plan**: Mock data is still available as automatic fallback

---

## 🆘 **Need Help?**

- **Amadeus Docs**: https://developers.amadeus.com/docs
- **Test Data Guide**: https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/test-data/
- **Support**: https://developers.amadeus.com/support

---

**You're all set!** 🎉

Now run the refresh command and you'll have professional Amadeus data for your demos!
