Smoking Detection System V2.0
This is a Smoking Detection System that uses YOLO (You Only Look Once) for object detection and OpenCV for video processing. It can detect smoking in real-time from a camera feed or by uploading images and videos. The system provides a graphical user interface (GUI) built using Tkinter, and it plays an alert sound when smoking is detected.

Features
Real-Time Camera Feed: Detect smoking in a live video stream using your webcam.
Image Upload: Upload images for smoking detection.
Video Upload: Upload video files for smoking detection.
Results Display: Display the detection results (coordinates and confidence) in a table.
Alert Sound: Play an alert sound when smoking is detected with confidence above 70%.
Multi-Camera Support: Allows you to select different available cameras for detection.
Requirements
Make sure you have the following libraries installed:

opencv-python
pygame
ultralytics
tkinter
Pillow (PIL)
numpy
You can install the necessary Python packages using the following command:

pip install opencv-python pygame ultralytics Pillow numpy
Setup
Clone the repository or download the project folder.
Ensure you have a YOLO model (.pt file) to load for object detection. You can modify the model_path variable in the code to point to your model.
By default, the code looks for a model called best.pt in the same directory.
If you don't have the model, you can use a pretrained YOLOv7 model or train your own model for smoking detection.
Make sure you have an audio file named smock.mp3 in the directory to play the alert sound when smoking is detected. You can replace it with any other .mp3 file.
Running the Application
1. Start the Application
Run the script using:

`python smock.py`

2. GUI Controls
Start Camera: Opens a camera feed for real-time smoking detection.
Stop Camera: Stops the camera feed.
Upload Image: Upload an image to detect smoking in the uploaded image.
Upload Video: Upload a video file for smoking detection in the video.

3. Results
The detected results (file name, coordinates, confidence) will be shown in a table on the right side of the GUI.

4. Alert
If smoking is detected with a confidence greater than or equal to 70%, an alert sound will play.
Known Issues
If you receive a "cannot open camera" error, make sure your camera is properly connected and accessible.
The program supports up to 4 cameras (camera 0 to camera 3). If you have more cameras, you may need to modify the code to handle additional devices.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Authors
Miss小远 – Initial work
Acknowledgments
YOLO – For providing a state-of-the-art object detection model.
OpenCV – For video processing.
Tkinter – For the graphical user interface.
Pillow (PIL) – For image handling.
