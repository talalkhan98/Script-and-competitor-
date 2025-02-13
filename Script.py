import streamlit as st
import requests
import openai

# Load API keys from Streamlit Secrets
API_KEY = st.secrets["AIzaSyCf4HTDktCFoquRQUlAw4jYtdkFcgsUOdc"]
OPENAI_API_KEY = st.secrets["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"]
openai.api_key = OPENAI_API_KEY

st.title("🚀 AI YouTube Script Generator")

# Input: Competitor Video URL
competitor_url = st.text_input("Enter Competitor's YouTube Video URL")
your_title = st.text_input("Enter Your Video Title")

if st.button("Analyze Competitor & Generate Better Script"):
    try:
        # Extract Video ID Safely
        if "v=" in competitor_url:
            video_id = competitor_url.split("v=")[-1].split("&")[0]
        else:
            st.error("❌ Invalid YouTube URL! Please enter a correct video link.")
            st.stop()

        # Fetch competitor video details
        video_details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={API_KEY}"
        response = requests.get(video_details_url)

        if response.status_code != 200:
            st.error("❌ YouTube API request failed! Check your API key or limit.")
            st.stop()

        video_data = response.json()

        if "items" not in video_data or not video_data["items"]:
            st.error("❌ Invalid Competitor Video! Please check the URL.")
            st.stop()

        competitor_video = video_data["items"][0]

        # Extract competitor video details
        comp_title = competitor_video["snippet"]["title"]
        comp_description = competitor_video["snippet"]["description"]
        comp_duration = competitor_video["contentDetails"]["duration"]
        comp_views = int(competitor_video["statistics"]["viewCount"])

        # Display Competitor Video Details
        st.subheader("🔍 Competitor Video Analysis")
        st.write(f"**🎬 Title:** {comp_title}")
        st.write(f"**📄 Description:** {comp_description[:200]}...")
        st.write(f"**⏳ Duration:** {comp_duration}")
        st.write(f"**👀 Views:** {comp_views}")

        # AI: Extract Keywords
        keywords_prompt = f"Extract the most important keywords from this video description:\n\n{comp_description}"
        keywords_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": keywords_prompt}]
        )
        keywords = keywords_response["choices"][0]["message"]["content"].strip()

        st.subheader("🔑 Extracted Keywords")
        st.write(keywords)

        # AI: Generate an Improved Script
        script_prompt = f"""
        Write an engaging, SEO-optimized YouTube script based on the title: "{your_title}".
        - Make it more detailed than the competitor's script.
        - Include a strong call-to-action at the end.
        - Use the following keywords: {keywords}.
        """
        script_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": script_prompt}]
        )
        script = script_response["choices"][0]["message"]["content"].strip()

        st.subheader("📝 AI-Generated Script")
        st.write(script)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
