import pyrealsense2 as rs
import numpy as np
import cv2

# Captured photos path
path_out_rgb = './Camera_Calib/caps_rgb/rgb_{}.png'
path_out_depth = './Camera_Calib/caps_depth/depth_{}.png'

pipe = rs.pipeline()
cfg  = rs.config()

cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)

pipe.start(cfg)

cap_num = 20 # number of photos to be captured
num = 0

while True:
    frame = pipe.wait_for_frames()
    depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,
                                     alpha = 0.5), cv2.COLORMAP_JET)

    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    k = cv2.waitKey(5)

    if (k == cap_num) or (k == ord('q')):
        break

    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite(path_out_rgb.format(num), color_image)
        cv2.imwrite(path_out_depth.format(num), depth_cm)
        print("Photo saved!")
        num += 1

    cv2.imshow('rgb', color_image)
    cv2.imshow('depth', depth_cm)

pipe.stop()