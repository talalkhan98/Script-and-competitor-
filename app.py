import streamlit as st
import requests
import openai
from datetime import datetime, timedelta

# 🔑 Enter Your API Keys Here
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"  # Replace with your actual API key
OPENAI_API_KEY = "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"    # Replace with your actual OpenAI API key

# URLs
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

# Streamlit App Title
st.title("🚀 YouTube Viral Topics & AI Optimization Tool")

# Input Fields
days = st.number_input("🔍 Search for Viral Topics in the Last (1-30 Days):", min_value=1, max_value=30, value=7)

# List of Trending Keywords
keywords = [
    "Trending News", "Viral TikTok", "YouTube Shorts Trends",
    "MrBeast Challenge", "Tech Unboxing", "Reddit Stories", 
    "Crime Documentaries", "AI Technology", "Space Exploration"
]

# Fetch Data Button
if st.button("🔥 Find Viral Topics Now"):
    try:
        # Calculate date range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        # Iterate over Keywords
        for keyword in keywords:
            st.write(f"🔍 Searching for: **{keyword}**")

            # YouTube API Search
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": YOUTUBE_API_KEY,
            }
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            if "items" not in data:
                st.warning(f"❌ No videos found for: {keyword}")
                continue

            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]

            # Fetch Video Statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": YOUTUBE_API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            if "items" not in stats_data:
                st.warning(f"⚠️ Failed to fetch video statistics for: {keyword}")
                continue

            # Process Video Data
            for video, stat in zip(videos, stats_data["items"]):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:150]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))

                # Store Results
                all_results.append({
                    "Title": title,
                    "Description": description,
                    "URL": video_url,
                    "Views": views
                })

        # Display Results
        if all_results:
            st.success(f"🎯 Found {len(all_results)} trending videos!")
            for result in all_results:
                st.markdown(f"""**🎬 {result['Title']}**  
🔗 [Watch Video]({result['URL']})  
👀 Views: {result['Views']}""")
                st.write("---")

        else:
            st.warning("🚫 No viral videos found in this search range.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# AI Optimization Section
st.header("🤖 AI-Powered Title & Hashtag Generator")

title_input = st.text_input("✍️ Enter Video Title:")
if st.button("🚀 Generate AI-Optimized Title & Hashtags"):
    if title_input:
        openai.api_key = OPENAI_API_KEY
        prompt = f"Generate an engaging YouTube title and hashtags for: {title_input}"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response["choices"][0]["message"]["content"]
            st.success("✅ AI-Generated Title & Hashtags:")
            st.write(result)
        except Exception as e:
            st.error(f"⚠️ OpenAI API Error: {e}")
    
    else:
        st.warning("⚠️ Please enter a video title first!")
