# scene-cut-detection
This project provides a Python script for detecting hard cuts (scene changes) in a video using histogram comparison and splitting the video into clips at those cuts.

This was inspired by Adobe Premiere Pro's 'Scene Edit Detection'.
I'm working on a lightweight, minimal, open source video editor and I want it to be easy to use, as well as have some of the more advanced features from Premiere Pro.
The final version of this app will be written in Rust, but I started in Python so here's some of the code I wrote for it.

It works by:
Converting frames to HSV color space (better handling of lighting changes).
Computing Hue histograms of consecutive frames.
Measuring the Bhattacharyya distance between histograms.
Marking frames where the difference exceeds a threshold (hist_thresh).
Saving histograms of cut frames as PNGs (for debugging/visualization).
Splitting the video into clips based on detected cuts.

Features:
Detects hard scene cuts automatically.
Splits video into separate clips at detected cuts.
Saves histogram visualizations of detected cut points.
Easy to configure threshold (hist_thresh) for sensitivity.

Requirements:
Make sure you have the following installed:
```
pip install opencv-python numpy matplotlib
```

Usage:
Clone or download this repository.
Place your video file in the project folder.
Open the script and update the following line with your video path:
```
video_path = '[PUT_VIDEO_FILE_PATH_HERE]'
```

And then run the script:
```
python3 scene_splitter.py
```

You can adjust the sensitivity of the cut detection by tuning this parameter:
```
hist_thresh
```
The default value (0.3) is what worked well for me, but your results may vary. Feel free to play around with it.
A lower value is more sensitive, and a higher value is less sensitive.

Video Codec:
Currently uses ```.mp4``` for the output, but it can be changed to another format if needed.


You can comment out the code that spits out the histogram images - I left them in because they're just fun to look at. But they're completely unnecessary.

