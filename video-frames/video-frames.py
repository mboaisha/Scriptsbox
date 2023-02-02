# video-frames.py
import argparse
import cv2

def extract_frames(video_path, output_dir):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Decide the interval between frames to extract
    interval = total_frames // 10

    # Create a counter for the frame number
    count = 0

    # Loop through all frames in the video
    while True:
        # Read the next frame
        ret, frame = cap.read()

        # If there are no more frames, break the loop
        if not ret:
            break

        # If the current frame is the specified interval, save the frame
        if count % interval == 0:
            frame_path = output_dir + f"/frame_{count}.jpg"
            cv2.imwrite(frame_path, frame)

        # Increment the frame counter
        count += 1

    # Release the video capture
    cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract thumbnails or snippets of a video.")
    parser.add_argument("video_path", type=str, help="Path to the input video file.")
    parser.add_argument("output_dir", type=str, help="Path to the directory to save the output frames.")
    args = parser.parse_args()

    extract_frames(args.video_path, args.output_dir)