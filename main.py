from flask import Flask, Response, render_template
from flask import request
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)
# fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=True)
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
thr = 99


def generate_frames():
    while True:
        success, frame = camera.read()
        frame = fgbg.apply(frame)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/my_func', methods=['POST', 'GET'])
def my_func():
    global thr
    thr = request.form["threshold"]
    thr = int(thr)


def generate_frames1():
    while True:
        success, frame = camera.read()
        # frame = fgbg.apply(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(frame, thr, 255, cv2.THRESH_BINARY)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video1')
def video1():
    return Response(generate_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=False)