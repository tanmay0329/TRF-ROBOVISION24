#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

# Initialize global variables to store current and target coordinates
cx = 0
cy = 0


# Callback function to update current coordinates when new data is received
def coordinates_callback(msg):
    global cx, cy
    #rospy.loginfo("Received integers: %d, %d", msg.data[0], msg.data[1])
    cx = msg.data[0]
    cy = msg.data[1]

# Function to get target coordinates from user input
def get_target_coordinates():
    
    rospy.loginfo("Enter target x coordinate:")
    targetx = int(input())
    rospy.loginfo("Enter target y coordinate:")
    targety = int(input())


    
        
if __name__ == '__main__':
    
   rospy.init_node('teleop')

   pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
    
    # Subscribe to topic to receive detected coordinates
   sub = rospy.Subscriber('detected_coordinates', Int32MultiArray, coordinates_callback)
    
    # Set rate for the control loop
   rate = rospy.Rate(10)  # 10hz
   try: 

     while not rospy.is_shutdown():
        rospy.loginfo("Current coordinates: (%d, %d)", cx, cy)
        
        
        # Create Twist message to send velocity commands
        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.angular.z = 0
        rospy.loginfo("Enter target x coordinate:")
        targetx = int(input())
        rospy.loginfo("Enter target y coordinate:")
        targety = int(input())
        flag=True
        # Control loop to navigate towards the target coordinates
        while True:
            # while abs(cx - targetx) <= 2 and abs(cy - targety) <= 2:
            #     twist.linear.x = 0
            #     twist.linear.y = 0
            #     twist.linear.z = 0
            #     twist.angular.x = 0
            #     twist.angular.y = 0
            #     twist.angular.z = 0
            #     rospy.loginfo("STOP")

            # if abs(cx - targetx) <= 2 and abs(cy - targety) <= 2:
            #     # Stop if the current coordinates are within the specified range of the target coordinates
            #     twist.linear.x = 0
            #     twist.linear.y = 0
            #     twist.linear.z = 0
            #     twist.angular.x = 0
            #     twist.angular.y = 0
            #     twist.angular.z = 0
            #     rospy.loginfo("STOP")
            #     flag=False
            #     break
                
            if cx == targetx and cy == targety:
                # If the current coordinates match the target coordinates exactly, print a message and break the loop
                rospy.loginfo("Reached target coordinates exactly")
                twist.linear.x = 0
                twist.linear.y = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                pub.publish(twist)
                flag=False
                break
                
            elif cy > targety + 1:
                # Move forward if the current y-coordinate is greater than the target y-coordinate
                twist.linear.x = 0.5
                twist.linear.y = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                
                rospy.loginfo("Moving forward")
                
            elif cy < targety - 1:
                # Move backward if the current y-coordinate is less than the target y-coordinate
                twist.linear.x = -0.2
                twist.linear.y = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                rospy.loginfo("Moving backward")
                
            elif cx > targetx + 1:
                # Move left if the current x-coordinate is greater than the target x-coordinate
                twist.linear.y = 0.4
                twist.linear.x = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                rospy.loginfo("Moving left")
                
            elif cx < targetx - 1:
                # Move right if the current x-coordinate is less than the target x-coordinate
                twist.linear.y = -0.2
                twist.linear.x = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                rospy.loginfo("Moving right")
                
            else:
                # Stop if none of the conditions are met
                rospy.loginfo("No movement")
                twist.linear.x = 0
                twist.linear.y = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                pub.publish(twist)
                flag=False
                break
            
            # Publish the Twist message to control the robot
            pub.publish(twist)
            rate.sleep()
        
        # After reaching the target coordinates or stopping, reset the twist message
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        rospy.loginfo("Reached target")
        
        # Wait for a new target coordinates
        rospy.loginfo("Waiting for new target coordinates...")
        
        rate.sleep()

   except KeyboardInterrupt:
        rospy.loginfo("KeyboardInterrupt has been caught. Exiting...")
   rospy.loginfo("Thank YOU")    


































