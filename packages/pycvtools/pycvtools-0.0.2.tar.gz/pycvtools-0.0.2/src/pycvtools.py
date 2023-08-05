
import cv2
import os


def vd2img(inputfile, Snap_No = 1):
    for inpt in os.listdir(inputfile):
        try:
            a = inputfile+"/"+inpt
        except:
            a = inputfile+"\\"+inpt
        cap = cv2.VideoCapture(a)
        i = 0

        while(cap.isOpened()):
            ret, frame = cap.read()
            
            # This condition prevents from infinite looping
            # incase video ends.
            if ret == False:
                break
            
            # Save Frame by Frame into disk using imwrite method
            if i//Snap_No ==  0:
                name = inpt.split(".")[0]
                cv2.imwrite(name+str(i)+'.jpg', frame)
                i += 1
            else:
                i += 1


        cap.release()
        cv2.destroyAllWindows()
    

