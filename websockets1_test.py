from flask import Flask, render_template,Response
from flask_socketio import SocketIO
import cv2
import time

app = Flask(__name__)

app.config ['SECRET_KEY'] = 'secret'

sockets = SocketIO(app)

# # @sockets.on('message')
# def echo_socket(ws):
#     print(ws)
@sockets.on('test')
def echo_socket(data):
    print(data)
camera = cv2.VideoCapture(1)
def gen_frames(): 
    while True:
        time.sleep(0.01)
        success, frame = camera.read()  
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

@app.route('/video_feed')
def video_feed():
    print('e')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def echo_test():
    return render_template('echo_test.html')

if __name__ == '__main__':
    sockets.run(app,debug=True)