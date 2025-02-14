import streamlit as st
import requests
import openai
from datetime import datetime, timedelta

# 🔑 API Keys (Replace with your actual keys)
YOUTUBE_API_KEY = "AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"
OPENAI_API_KEY = "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"

# Streamlit App Title
st.title("🚀 YouTube Viral Topics & AI Optimization Tool")

# Validate OpenAI API Key
if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
    st.error("⚠️ OpenAI API Key is missing! Please add a valid key.")
else:
    openai.api_key = OPENAI_API_KEY

# Input Fields
days = st.number_input("🔍 Search for Viral Topics in the Last (1-30 Days):", min_value=1, max_value=30, value=7)

# Define Trending Keywords
keywords = ["Trending News", "Viral TikTok", "YouTube Shorts Trends", "AI Technology"]

# Button to Fetch Data
if st.button("🔥 Find Viral Topics Now"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        for keyword in keywords:
            st.write(f"🔍 Searching for: **{keyword}**")

            # YouTube API Request
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": YOUTUBE_API_KEY,
            }
            response = requests.get("https://www.googleapis.com/youtube/v3/search", params=search_params)
            data = response.json()

            if "items" not in data:
                st.warning(f"❌ No videos found for: {keyword}")
                continue

            for video in data["items"]:
                video_id = video["id"]["videoId"]
                title = video["snippet"]["title"]
                url = f"https://www.youtube.com/watch?v={video_id}"

                all_results.append({"Title": title, "URL": url})

        # Display Results
        if all_results:
            st.success(f"🎯 Found {len(all_results)} trending videos!")
            for result in all_results:
                st.markdown(f"""**🎬 {result['Title']}**  
🔗 [Watch Video]({result['URL']})""")
                st.write("---")
        else:
            st.warning("🚫 No viral videos found.")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API Request Error: {e}")

    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")

# AI Title & Hashtag Generator
st.header("🤖 AI-Powered Title & Hashtag Generator")

title_input = st.text_input("✍️ Enter Video Title:")
if st.button("🚀 Generate AI-Optimized Title & Hashtags"):
    if title_input:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"Generate an engaging YouTube title and hashtags for: {title_input}"}]
            )
            result = response["choices"][0]["message"]["content"]
            st.success("✅ AI-Generated Title & Hashtags:")
            st.write(result)
        except openai.error.OpenAIError as e:
            st.error(f"⚠️ OpenAI API Error: {e}")
    else:
        st.warning("⚠️ Please enter a video title first!")
