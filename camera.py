import numpy as np 
import cv2
import geom_util as geom


class Camera:

    angle = None ;
    shift = None ;

    def startCamera(self):
        cap = cv2.VideoCapture(0)

       


        
        while True:
            ret,frame = cap.read()
            
            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            
        
        cap.release()
        cv2.destroyAllWindows()


    def FindBlackLine(self):

        cap = cv2.VideoCapture(0)

        while True:
            ret,frame = cap.read()

            blur = cv2.GaussianBlur(frame,(7,7),0)
            gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]



            cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(frame, cnts, -1, (0,255,0), 3)
            c = None
            if len(cnts) > 0 and cnts != None:
                c = max(cnts,key = cv2.contourArea)
            
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            box = geom.order_box(box)
            
            cv2.drawContours(frame,[box],0,(0,0,255),2)

            p1, p2 = geom.calc_box_vector(box)

            cv2.line(frame, p1, p2, (0, 255, 0), 3)


            h,w = frame.shape[:2]

            angle = geom.get_vert_angle(p1, p2, w, h)
            shift = geom.get_horz_shift(p1[0], w)

            self.set_angle(angle)
            self.set_shift(shift)

            # cv2.imshow("frame",frame)

            print(angle)

        
            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
    def set_angle(self,var):
        self.angle = var ;


    def set_shift(self,var):
        self.shift = var

    
    def get_angle(self):
        return self.angle

    def get_shift(self):
        return self.shift





