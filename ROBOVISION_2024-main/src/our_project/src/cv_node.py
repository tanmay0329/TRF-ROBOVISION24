#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String
import numpy as np
import json

class ImageProcessor:
    def __init__(self):
        rospy.init_node('image_processor_node', anonymous=True)

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Subscribe to the image_raw topic
        self.subscription = rospy.Subscriber(
            '/camera/color/image_raw',
            Image,
            self.image_callback,
            queue_size=10
        )

        # Publisher for coordinates
        self.coord_publisher = rospy.Publisher('/detected_coordinates', Int32MultiArray, queue_size=10)

    def image_callback(self, msg):
        try:
            # Convert the ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            # Perform color masking to detect green regions
            green_lower = np.array([40, 40, 40])  # Adjust these values according to your green color range
            green_upper = np.array([80, 255, 255]) # Adjust these values according to your green color range
            hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_image, green_lower, green_upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
            # Draw bounding boxes around detected green regions
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center_x=x+w//2
                center_y=y+h//2
                print(x,w,y,h)
                coordinates_dict = None
                cv2.putText(cv_image,f'Center:({center_x},{center_y})',(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
                # coordinates_dict = {'x': int(center_x), 'y': int(center_y), 'width':int(w), 'height': int(h)}
                msg = Int32MultiArray(data=[center_x, center_y])
                self.coord_publisher.publish(msg)
            # Convert the dictionary to a JSON string
            # coordinates_json = json.dumps(coordinates_dict)

            # Publish the JSON string
            # self.coord_publisher.publish(coordinates_json)

            # Display the image
            cv2.imshow("Camera Image 2", cv_image)
            cv2.waitKey(1)

        except Exception as e:
            rospy.logerr("Error processing the image: %s" % str(e))

def main():
    image_processor_node = ImageProcessor()
    rospy.spin()

if __name__ == '__main__':
    main()
