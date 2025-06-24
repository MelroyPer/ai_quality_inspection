import cv2

"""
create aruco marker and save image
"""
# Choose dictionary and marker ID
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
marker_id = 23
marker_size_pixels = 700  # Image resolution

# Generate the marker image
img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size_pixels)
cv2.imwrite("aruco_23.png", img)
