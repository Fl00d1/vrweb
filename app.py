from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
from random import randint
import cv2
from flask_cors import CORS
import serial
import time

#SSL Сертификат для сервера разработки
app = Flask(__name__)
CORS(app)
app.config ['SECRET_KEY'] = 'secret'

sockets = SocketIO(app)

# @sockets.on('message')
# def echo_socket(ws):
#     print(ws)

@sockets.on('test')
def echo_socket(data):
    x=int(data["x"]*120)
    y=int(-data["y"]*120)
    # print(x,y)
    # print(x+y)
    # s=str(-data["y"]*120+data["x"]*120)+";"+str(-data["y"]*120-data["x"]*120)
    s=str(str(y+x)+';'+str(y-x))
    ser.write((s).encode())
    # sockets.emit('test',{data: 'data'})


camera = cv2.VideoCapture(1)
def serialstart():
    global ser
    ser = serial.Serial('COM14',115200)
    ser.reset_input_buffer()
    ser.timeout=0.001
    ser.write_timeout=0.001
    
def gen_frames(): 
    serialstart()
    while True:
        time.sleep(0.001)
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

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#     # return ('',204)
# @sockets.on('video',namespace='/video_feed')
# def video_feed():
#     image=cv2.imread('dog.jpeg',0)
#     sockets.emit('test','dara')
#     return Response(image, mimetype='multipart/x-mixed-replace; boundary=frame')



# @app.route('/button_pressed',methods = ['POST', 'GET'])
# def button_pressed():
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#         print(data["x"],data["y"])
#         s=str(-data["y"]*120+data["x"]*120)+";"+str(-data["y"]*120-data["x"]*120)
#         ser.write(s.encode())
#         return ('OK',204)
 




    
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')



if __name__ == '__main__':
    # ser = serial.Serial('COM8',115200)
    # ser.reset_input_buffer()
    # ser.timeout=0.001
    # ser.write_timeout=0.001
    sockets.run(app,debug=True,host='0.0.0.0',port=5000)

