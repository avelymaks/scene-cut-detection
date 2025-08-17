import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load video
video_path = '[PUT_VIDEO_FILE_PATH_HERE]'
cap = cv2.VideoCapture(video_path)

# Sensitivity threshold for hard cut detection (tune as needed)
hist_thresh = 0.3

# Frame counter
frame_count = 0
cut_frames = []

# Get the first frame
ret, prev_frame = cap.read()
if not ret:
    print("Failed to load video.")
    exit()

# Convert the first frame to HSV (better lighting handling)
prev_hist = cv2.calcHist([cv2.cvtColor(prev_frame, cv2.COLOR_BGR2HSV)], [0], None, [180], [0, 180])
prev_hist = cv2.normalize(prev_hist, prev_hist).flatten()

# Loop through the frames of the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the current frame to HSV and get histogram
    curr_hist = cv2.calcHist([cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)], [0], None, [180], [0, 180])
    curr_hist = cv2.normalize(curr_hist, curr_hist).flatten()

    # Compare histograms using Bhattacharyya distance (a measure of similarity)
    diff = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_BHATTACHARYYA)

    # If the difference exceeds the threshold, a scene cut is detected
    if diff > hist_thresh:
        print(f"Hard cut detected at frame {frame_count + 1}")
        cut_frames.append(frame_count + 1)  # Add the frame number +1 to mark the start of the next clip

        # Save the histograms as images
        plt.figure()
        plt.title(f"Histogram at frame {frame_count + 1}")
        plt.xlabel("Hue value")
        plt.ylabel("Frequency")
        plt.bar(np.arange(0, 180), prev_hist, width=1)
        plt.savefig(f"histogram_{frame_count + 1}.png")
        plt.close()

    # Update the previous histogram for the next comparison
    prev_hist = curr_hist
    frame_count += 1

cap.release()

# Output the detected cut frames
print("Cut frames:", cut_frames)

# Create a directory to save the clips
output_dir = os.path.splitext(os.path.basename(video_path))[0]  # Use video name as directory name
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Reload the video for splitting
cap = cv2.VideoCapture(video_path)

clip_number = 1

# For each cut frame, split the video
for i in range(len(cut_frames)):
    start_frame = cut_frames[i]
    end_frame = cut_frames[i + 1] if i + 1 < len(cut_frames) else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Open the video again to extract the frames for the clips
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Prepare to write the clip to a new file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    clip_filename = os.path.join(output_dir, f"clip_{clip_number}.mp4")
    out = cv2.VideoWriter(clip_filename, fourcc, 30, (int(cap.get(3)), int(cap.get(4))))

    # Write frames to the new clip
    for frame_idx in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    # Release the video writer for the current clip
    out.release()

    print(f"Creating {clip_filename} from frame {start_frame} to {end_frame}")
    clip_number += 1

cap.release()  # Close the video capture object

print("Video splitting complete.")
