import os
import streamlit as st
from Homepage import set_sidebar_visibility

st.title('AI Fitness Trainer: Squats Analysis')

# Prefer a repo-relative sample video; fall back to an uploader in deployments
repo_paths = [
	os.path.join("sample_videos", "output_sample.mp4"),
	"output_sample.mp4",
]

sample_path = None
for p in repo_paths:
	if os.path.exists(p):
		sample_path = p
		break

if sample_path:
	st.video(sample_path)
else:
	st.info("No local sample video found. Upload one to preview the demo or add ./sample_videos/output_sample.mp4 to the repo.")
	uploaded = st.file_uploader("Upload a sample video", type=["mp4", "mov", "webm"])
	if uploaded is not None:
		st.video(uploaded)
    

