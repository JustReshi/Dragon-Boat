import cv2
import sys
import time

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__' :

    # Set up tracker.
    # Instead of MIL, you can also use

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]

    # initialize a dictionary that maps strings to their corresponding
    # OpenCV object tracker implementations
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }

    # Read video
    video = cv2.VideoCapture("drap.mp4")

    # used to record the time when we processed last frame 
    prev_frame_time = 0
      
    # used to record the time at which we processed current frame 
    new_frame_time = 0

    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ("Cannot read video file")
        sys.exit()
    
    # Define an initial bounding box
    #bbox = (287, 23, 86, 320)

    ## Select boxes
    bboxes = []
    # Create MultiTracker object
    multiTracker = cv2.MultiTracker_create()

    # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
    # So we will call this function in a loop till we are done selecting all objects
    while True:
        # draw bounding boxes over objects
        # selectROI's default behaviour is to draw box starting from the center
        # when fromCenter is set to false, you can draw box starting from top left corner
        bbox = cv2.selectROI('MultiTracker', frame)
        bboxes.append(bbox)
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        k = cv2.waitKey(0) & 0xFF
        if (k == 113):  # q is pressed
            break

    print('Selected bounding boxes {}'.format(bboxes)) 

    #tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
    # Initialize MultiTracker 
    for bbox in bboxes:
        tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
        multiTracker.add(tracker, frame, bbox)


    # Initialize tracker with first frame and bounding box
    #ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        # time when we finish processing for this frame 
        new_frame_time = time.time() 

        # Calculating the fps 

        # fps will be number of frame processed in given time frame 
        # since their will be most of time error of 0.001 second 
        # we will be subtracting it to get more accurate result 
        fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time 

        # get updated location of objects in subsequent frames
        ok, boxes = multiTracker.update(frame)

        # draw tracked objects
        for box in boxes:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        (x, y, w, h) = [int(v) for v in boxes[0]]
        p1 = (int(x + w/2), int(y + h/2))

        (x, y, w, h) = [int(v) for v in boxes[1]]
        p2 = (int(x + w/2), int(y + h/2))

        cv2.line(frame, p1, p2, (255, 0, 0), 5) 

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # show frame
        cv2.imshow('MultiTracker', frame)


        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

    
