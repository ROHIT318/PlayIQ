# import moviepy
from moviepy import VideoFileClip
from moviepy.video.fx import MultiplySpeed

# Define the input video file, start time (seconds), and end time (seconds)
input_file = "test.mp4"
start_time = 10
end_time = 20
output_file = "output.mp4"

# Load the video
clip = VideoFileClip(input_file)


trimmed_clip = clip.subclipped(start_time, start_time+((start_time-end_time)*2))
trimmed_clip = MultiplySpeed(2).apply(trimmed_clip)

trimmed_clip.write_videofile(output_file)

# Close the clips
clip.close()
trimmed_clip.close()

print(f"Video cut and saved to {output_file}")