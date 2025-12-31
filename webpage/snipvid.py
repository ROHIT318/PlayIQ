from moviepy import VideoFileClip
from moviepy.video.fx import MultiplySpeed
import streamlit as st
import os
import tempfile
import datetime

st.title("SnipVid")

col1, col2 = st.columns([1, 1.2])

if os.path.join(os.getcwd(), "Utility") == False:
    os.mkdir(os.path.join(os.getcwd(), "Utility"))

if os.path.join(os.getcwd()+"\\Utility\\", "Video Clips") == False:
    os.mkdir(os.path.join(os.getcwd()+"\\Utility\\", "Video Clips"))

with col1:
    with st.container(border=True):
        vid = st.file_uploader("Upload Video: ", type=["mp4"])
        temp_filename = None
        if vid:
            st.video(vid, width=500)
            video_bytes = vid.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
                tmpfile.write(video_bytes)
                temp_filename = tmpfile.name



with col2:
    with st.container(border=True):
        clip_name = st.text_input("Enter a standard name for the clips: ")
        no_cuts = st.number_input("Number of clips from the selected video: ", step=1)

        for i in range(no_cuts):
            col1, col2 = st.columns(2)
            with col1:
                st.number_input("Start Time: ", key=f"start_{i}", step=1)
            with col2:
                st.number_input("End Time: ", key=f"end_{i}", step=1)

        for i in range(no_cuts):
            invalid_str = ""
            start_time = st.session_state[f"start_{i}"]
            end_time = st.session_state[f"end_{i}"]
            if start_time >= end_time:
                invalid_str = "Invalid time given and clip won't be created...."
            st.write(f"For clip number {i+1}, start and end time are '{start_time}' and '{end_time}'." + f"{invalid_str}")

st.divider()

if st.button("Create Clip(s)"):
    # st.write("Creating clips....")
    output_file = ""

    for i in range(no_cuts):

        video_columns = st.columns(no_cuts)

        if temp_filename and no_cuts and st.session_state[f"start_{i}"]:
            clip = VideoFileClip(temp_filename, audio=False)
            # clip = VideoFileClip(vid.getvalue())
            start_time = st.session_state[f"start_{i}"]
            end_time = st.session_state[f"end_{i}"]
            trimmed_clip = clip.subclipped(start_time, start_time+((end_time-start_time)*2))
            trimmed_clip = MultiplySpeed(2).apply(trimmed_clip)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpout:
                trimmed_clip.write_videofile(tmpout.name, audio=False)
                video_bytes = open(tmpout.name, "rb").read()
                # st.video(video_bytes, width=200)

            output_filename = clip_name + "_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + str(start_time) + str(end_time) + ".mp4"
            output_filepath = os.path.join(os.getcwd(), "PlayIQ", "webpage", "Utility", "Video Clips", output_filename)
            trimmed_clip.write_videofile(output_filepath)
        else:
            st.write("Enter number of clips and their respective cut times....")

        clip.close()
        trimmed_clip.close()

if clip_name:
    video_clips_folder = os.path.join(os.getcwd(), "PlayIQ", "webpage", "Utility", "Video Clips")
    all_files_url = os.scandir(video_clips_folder)
    req_clips_url = []
    for file in all_files_url: 
        if clip_name in file.name and file.is_dir()==False:
            req_clips_url.append(video_clips_folder + "\\" + file.name)
    st.write(req_clips_url)