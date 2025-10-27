# 🌐 Hybrid Data Setup Guide

This guide explains how to set up and use **real travel data** for your demos using the hybrid approach.

## 📊 What is the Hybrid Approach?

The hybrid approach gives you the **best of both worlds**:

- ✅ **Real Data**: Fetched from Amadeus Travel API
- ✅ **Fast & Reliable**: Cached locally for instant access
- ✅ **No Demo Failures**: Works offline, no API rate limits during demos
- ✅ **Up-to-date**: Refresh weekly or as needed

## 🚀 Quick Start

### Step 1: Get Amadeus API Credentials

1. Go to https://developers.amadeus.com/register
2. Create a free account
3. Create a new app
4. Copy your **API Key** and **API Secret**

**Free Tier Includes:**
- 2,000 API calls per month
- Perfect for weekly data refreshes

### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
# Amadeus API Configuration
AMADEUS_API_KEY=your_actual_api_key_here
AMADEUS_API_SECRET=your_actual_api_secret_here
```

### Step 3: Install Dependencies

```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install amadeus requests-cache
```

### Step 4: Fetch Real Data

```bash
python -m app.services.real_data_fetcher --refresh
```

This will:
- ✅ Fetch real flights from Amadeus API
- ✅ Fetch real hotels
- ✅ Fetch real activities
- ✅ Cache everything in `app/data/cache/real_travel_data.json`

**Expected Output:**
```
🔄 Fetching real travel data from Amadeus API...

📍 Fetching data for Tokyo...
✅ Tokyo: 10 flights, 10 hotels, 15 activities

📍 Fetching data for Paris...
✅ Paris: 10 flights, 8 hotels, 12 activities

📍 Fetching data for New York...
✅ New York: 10 flights, 10 hotels, 14 activities

📍 Fetching data for London...
✅ London: 10 flights, 9 hotels, 13 activities

✅ Real data cached successfully!
📅 Last updated: 2025-01-27T10:30:00
```

### Step 5: Verify

```bash
python -m app.services.real_data_fetcher --check
```

Shows cache status and data freshness.

## 🎯 How It Works

### Automatic Fallback

The application **automatically** uses the best available data:

```
1. Check for cached real data
   ├─ ✅ Found → Use real data from Amadeus
   └─ ❌ Not found → Use mock data
```

### Transparency

The backend logs which data source is being used:

```python
✅ Using cached REAL travel data from Amadeus API
```

or

```python
⚠️  Using MOCK travel data (real data not cached)
```

## 📅 Maintenance

### Refresh Data Weekly

```bash
# Recommended: Refresh every Monday before your weekly demo
python -m app.services.real_data_fetcher --refresh
```

### Check Cache Age

```bash
python -m app.services.real_data_fetcher --check
```

If cache is > 7 days old, you'll see:
```
⚠️  Cached data is 10 days old. Consider refreshing.
```

## 🎬 For Your Demo

### Before Presentation

1. ✅ Refresh cached data (if > 7 days old)
2. ✅ Run `--check` to verify all destinations have data
3. ✅ Test one scenario to ensure everything works

### During Presentation

You can confidently say:

```
"The agents are working with real travel data from Amadeus API,
cached for demo reliability. The prices you see are actual market
rates from this week. In production, this would hit live APIs,
but for demos, we cache to ensure no network delays or API failures."
```

### If Asked About Data Freshness

```
"This data was refreshed [X days ago] from Amadeus. The orchestration
and AI decision-making you're seeing is 100% real-time - only the
travel inventory is cached for reliability."
```

## 🔧 Troubleshooting

### Problem: "Amadeus API not configured"

**Solution:** Check your `.env` file has valid credentials:
```bash
AMADEUS_API_KEY=actual_key_here
AMADEUS_API_SECRET=actual_secret_here
```

### Problem: "API call failed"

**Possible causes:**
- Invalid API credentials
- Rate limit exceeded (2000 calls/month on free tier)
- Network issue

**Solution:** Use mock data for now:
```bash
# Application will automatically fall back to mock data
# No changes needed
```

### Problem: "No cached data found"

**Solution:** Run refresh command:
```bash
python -m app.services.real_data_fetcher --refresh
```

## 📁 File Structure

```
backend/
├── app/
│   ├── data/
│   │   └── cache/
│   │       └── real_travel_data.json    ← Cached real data
│   └── services/
│       ├── real_data_fetcher.py         ← Fetches from Amadeus
│       ├── hybrid_data.py               ← Serves cached data
│       └── mock_data.py                 ← Fallback mock data
```

## 🎯 Benefits Summary

| Feature | Mock Data | Real APIs (Live) | Hybrid (Cached) |
|---------|-----------|------------------|-----------------|
| **Reliability** | 100% | 85% | **100%** ✅ |
| **Speed** | Instant | 2-10s | **Instant** ✅ |
| **Cost** | Free | $$ | **Free*** ✅ |
| **Real Data** | ❌ | ✅ | **✅** |
| **Offline** | ✅ | ❌ | **✅** |
| **Demo Safe** | ✅ | ❌ | **✅** |

*Free tier: 2000 API calls/month (plenty for weekly refreshes)

## 🚀 Next Steps

1. ✅ Get Amadeus API credentials
2. ✅ Update `.env` file
3. ✅ Run `--refresh` to fetch real data
4. ✅ Test your demo scenarios
5. ✅ Set weekly reminder to refresh data

## 💡 Pro Tips

1. **Refresh Sunday Night**: Fresh data for Monday demos
2. **Test After Refresh**: Run one scenario to verify
3. **Check Before Big Demos**: Ensure cache isn't stale
4. **Keep Mock Data**: It's your safety net

## ❓ FAQ

**Q: Is the AI still "real" with cached data?**
A: YES! The AI orchestration, decision-making, and swarm intelligence are 100% real. Only the travel inventory is cached.

**Q: How often should I refresh?**
A: Weekly is recommended. Travel prices don't change dramatically day-to-day.

**Q: What if I forget to refresh?**
A: Application automatically falls back to mock data. No failures!

**Q: Can I use this in production?**
A: For production, you'd call live APIs. This hybrid approach is optimized for demos.

---

**Need Help?** Check the logs or contact the development team.
