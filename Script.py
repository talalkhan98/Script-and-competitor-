import streamlit as st
import requests
import openai
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Fetch API keys correctly
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# ✅ Validate API Keys
if not OPENAI_API_KEY or not YOUTUBE_API_KEY:
    st.error("❌ API keys are missing! Please check your `.env` file.")
    st.stop()

# ✅ Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

st.title("🚀 AI YouTube Script Generator")

# Input fields
competitor_url = st.text_input("Enter Competitor's YouTube Video URL")
your_title = st.text_input("Enter Your Video Title")

if st.button("Analyze Competitor & Generate Better Script"):
    try:
        # ✅ Extract Video ID from URL
        if "v=" in competitor_url:
            video_id = competitor_url.split("v=")[-1].split("&")[0]
        else:
            st.error("❌ Invalid YouTube URL format!")
            st.stop()

        # ✅ Fetch competitor video details
        video_details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={YOUTUBE_API_KEY}"
        response = requests.get(video_details_url)
        video_data = response.json()

        if "items" not in video_data or not video_data["items"]:
            st.error("❌ Invalid competitor video URL or API limit reached.")
            st.stop()

        competitor_video = video_data["items"][0]

        # ✅ Extract competitor video details
        comp_title = competitor_video["snippet"]["title"]
        comp_description = competitor_video["snippet"]["description"]
        comp_duration = competitor_video["contentDetails"]["duration"]
        comp_views = int(competitor_video["statistics"]["viewCount"])

        # ✅ Display competitor video details
        st.subheader("🔍 Competitor Video Analysis")
        st.write(f"**🎬 Title:** {comp_title}")
        st.write(f"**📄 Description:** {comp_description[:200]}...")
        st.write(f"**⏳ Duration:** {comp_duration}")
        st.write(f"**👀 Views:** {comp_views}")

        # ✅ AI: Extract Keywords
        keywords_prompt = f"Extract the most important SEO keywords from this YouTube video description:\n\n{comp_description}"
        keywords_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": keywords_prompt}]
        )
        keywords = keywords_response["choices"][0]["message"]["content"]

        st.subheader("🔑 Extracted Keywords")
        st.write(keywords)

        # ✅ AI: Generate an Improved Script
        script_prompt = f"""
        Write a detailed, engaging, and SEO-optimized YouTube video script based on the title: "{your_title}".
        - Make it longer and more detailed than the competitor's script.
        - Use Immediate Validation of the Title’s Claim in the hook.
        - Incorporate these SEO keywords: {keywords}.
        - Include a strong call-to-action (CTA) at the end.
        """

        script_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": script_prompt}]
        )

        script = script_response["choices"][0]["message"]["content"]

        st.subheader("📝 AI-Generated Script")
        st.write(script)

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
import os
import streamlit as st
import openai
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Fetch API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# ✅ Validate API Keys
if not OPENAI_API_KEY or not YOUTUBE_API_KEY:
    st.error("❌ API keys are missing! Please check your `.env` file.")
    st.stop()

# ✅ Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

st.title("🚀 AI YouTube Script Generator")

# ✅ User Inputs
competitor_url = st.text_input("Enter Competitor's YouTube Video URL")
your_title = st.text_input("Enter Your Video Title")

if st.button("Analyze Competitor & Generate Better Script"):
    st.write("Processing...")
