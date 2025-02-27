import serial
import FreeSimpleGUI as sg
import serial.tools.list_ports
import time
from string import *
import threading


sg.user_settings_filename(path='.')  # The settings file will be in the same folder as this program

def wait_for_handshake(ser, keywords=("height")):
    start_time = time.time()
    while True:
        line = ser.readline().decode().strip()
        for keyword in keywords:
            if keyword in line:
                return True
            if time.time() - start_time > 2:
                print(f"No handshake received within 2 seconds on port {ser.port}")
                sg.popup_quick_message(f"No handshake received within 2 seconds on port {ser.port}", text_color='darkgreen', background_color='orange', font='_ 18',)
                return False
            print(f"Received text: {line}")

def find_and_connect():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=115200, timeout=2)
            if wait_for_handshake(ser, keywords = ("height","handshake")):
                sg.popup_quick_message(f"Connection Successful: {ser.port}", text_color='white', background_color='red', font='_ 22',)
                return ser
            ser.close()
        except Exception as e:
            print(f"Error connecting to port {port.device}: {e}")
    sg.popup("Connection Fail","check your device connection:\nRESTART your board...??\nUNPLUG and plug your boar again...?!!\nTURN ON Caliper...??!\n...\nthen click on button : Reconnect !!!",text_color='magenta')
    return None



# Class holding the button graphic info. At this time only the state is kept
class BtnInfo:
    def __init__(self, state=True):
        self.state = state        # Can have 3 states - True, False, None (disabled)

def sanitize_input(data):
    return ''.join([str(c) for c in data if ord(c) < 128])

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_to_port(port):
    try:
        ser = serial.Serial(port, 115200, timeout=10)
        sg.popup("Success", f"Connected to {port}")
        return ser
    except serial.SerialException as e:
        sg.popup_error("Error", f"Failed to connect to {port}: {e}")

# Settings for you to modify are the size of the element, the circle width & color and the font for the % complete
bgcwin='black'
GRAPH_SIZE = (300 , 300)          # this one setting drives the other settings
CIRCLE_LINE_WIDTH, LINE_COLOR = 20, 'yellow'
TEXT_FONT = 'Tahoma'
TEXT_FONT_V='Serif'
TEXT_FONT_U='Arial'
# Computations based on your settings above
TEXT_HEIGHT = GRAPH_SIZE[0]//4
TEXT_LOCATION = (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//1.4)
TEXT_COLOR = LINE_COLOR
TEXT_COLOR_V = 'cyan' 
TEXT_LOCATION_V= (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//2.2)
TEXT_COLOR_U = 'light green'
TEXT_LOCATION_U= (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//5.2)

def update_meter(graph_elem, val=10.11,maxval=100.00,show=[10.11,100.00,'mm','height']):
    """
    Update a circular progress meter
    :param graph_elem:              The Graph element being drawn in
    :type graph_elem:               sg.Graph
    :param percent_complete:        Percentage to show complete from 0 to 100
    :type percent_complete:         float | int
    """
    graph_elem.erase()
    arc_length = show[0]/show[1]*360+.9
    if arc_length >= 360:
        arc_length = 359.9
        pass
    arc_COLOR = get_color(val,maxval)
    percent = show[0]/show[1]*100
    arcaddedlin=CIRCLE_LINE_WIDTH#+percent//5
    
    graph_elem.draw_arc((arcaddedlin, GRAPH_SIZE[1] - arcaddedlin), (GRAPH_SIZE[0] - arcaddedlin, arcaddedlin),
                   arc_length, 0, 'arc', arc_color=arc_COLOR, line_width=arcaddedlin)
    
    graph_elem.draw_text(f'%{percent:.0f}', TEXT_LOCATION_U, font=(TEXT_FONT, -TEXT_HEIGHT), color=TEXT_COLOR)
    graph_elem.draw_text(f'{show[0]/100:.2f}', TEXT_LOCATION_V, font=(TEXT_FONT_V, -TEXT_HEIGHT), color=TEXT_COLOR_V)
    graph_elem.draw_text(f'{show[2]}', TEXT_LOCATION, font=(TEXT_FONT_U, -TEXT_HEIGHT), color=TEXT_COLOR_U)
# Set up serial communication with the Arduino
#arduino = #serial.Serial('COM7', 115200)  # Replace 'COM7' with your Arduino's serial port

# Function to determine color based on value
def get_color(value, max_value):
    ratio = value / max_value
    if ratio>=1:
        return'blue'
    elif ratio>=0.95:
        return 'red'
    elif ratio >= 0.8:
        return 'purple'
    elif ratio >= 0.6:
        return 'orange'
    elif ratio >= 0.4:
        return 'yellow'
    elif ratio >= 0.2:
        return 'lightgreen'
    else:
        return 'green'
    
def makewindow():
    # Define the GUI layout with colored squares for displaying values and control buttons
    ports = list_serial_ports()
    menu_def = [['File', ['New','Exit']],
            ['Settings', ['Select Serial Port','log on','log off']]]
    sg.theme('black')

    layout_progress_graph = [  sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key='-GRAPHH-',background_color=bgcwin),sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key='-GRAPHP-',background_color=bgcwin)]

    col_1 =[
        sg.Column([[
     sg.Frame("Control Inputs", [
    [sg.Button('Reconnect')],
        [sg.Text("Final Height:"), sg.Stretch(), sg.InputText("101.31", justification='center',key="final_height", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="height_dependency",default=True, enable_events=True)],[
        sg.Text("Final Pressure:"), sg.Stretch(),sg.InputText("105.2", justification='center',disabled=True,key="final_pressure", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="pressure_dependency",disabled=True)]
         ,[
        sg.Text("Size:"), sg.Stretch(),sg.InputText("4", justification='center',disabled=False,key="-SIZE-", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="radiosize",disabled=False)]
         ]
    , border_width=2, element_justification='stretch'),
     sg.Frame('Motor Power', [[sg.Text('11', key='-MOTOR_VAL-',size=(10,10),expand_y=True, font=('Tahoma', 48, 'bold'), justification='center', pad=(0, 40),background_color=bgcwin)]],
              size=(200, 200),background_color=bgcwin, key='MOTOR_FRAME', element_justification='center', border_width=5, relief='raised'),],],element_justification='center'),
     sg.Column([[sg.Slider(range=(0, 100), orientation='v', font=('Helvetica 20'), size=(12, 15), key='DUTY_SLIDER',change_submits=True,  enable_events=True)],], element_justification='center')]
    
    layout_control=[
    [
     sg.Button('Drain', key='DRAIN', button_color=('yellow', 'magenta'), size=(10, 2),metadata=BtnInfo(),disabled=True),
     sg.Button('Pause', key='PAUSE', button_color=('yellow', 'olive'), size=(10, 2),disabled=True,enable_events=True,change_submits=True),
     sg.Button('+', key='PUMP', button_color=('yellow', 'blue'), size=(10, 2),disabled=True),],
    [
              
     sg.Button('Stop', key='STOP', button_color=('yellow', 'red'), size=(10, 2),disabled=True),sg.Button('Run', key='RUN', button_color=('yellow', 'green'), size=(10, 2),disabled=True),],
    [sg.Button('Pump ON', key='PUMPON', button_color=('yellow', 'darkblue'), size=(10, 2),disabled=True)]]

    log_layout = [
        
        [sg.Multiline(size=(50, 20), key='-OUTPUT-',visible=False)]
        
    ]
    
    
    layout = [[sg.Menu(menu_def, tearoff=False)],
              layout_progress_graph,[sg.HorizontalSeparator()],
              col_1,[sg.HorizontalSeparator()],
              layout_control,[sg.HorizontalSeparator()],
              log_layout
        ]
    
    # Create the window
    window = sg.Window('Arduino Sensor Values and Control', layout, finalize=True, element_justification='center',location=(100, 100),background_color=bgcwin,resizable=True,sbar_frame_color='gray')
    return window



def reinterperetrecived(data='pressure:100',check='pressure'):
    cc=check.__add__(':')
    ccl = len(cc)
    dcl=len(data)
    ndata=data
    phfc = ndata.find(cc) 
    rec = 0.00
    if phfc >-1:
        nsdata=ndata[phfc:dcl]
        rec= float(data[phfc+ccl:dcl])
    return rec
def reciveddata(data=" "):
    cif=data.find('\r')
    cnf= data.find('\n')
    if cif>-1 :
        if cnf>-1:
            cif = min(cif,cnf)
    else:
        if cnf>-1:
            cif = cnf
        else:
            return



RUN_MODE=1
STOP_MODE=2
PAUSE_MODE=3
PUMP_MODE=4
DRAIN_MODE=5
IDLE_MODE=6
DONE_MODE=7
DUTYCYCLE_DEFAULT=55
global arduino
arduino = None#find_and_connect()   # type: ignore
def loopgui():
    start_time = time.time()
    btndis=True
    # Create a UserSettings object. The JSON file will be saved in the same folder as this .py file
    window_contents = sg.UserSettings(path='.', filename='mysettings.json')
    keys_to_save = ('DUTY_SLIDER','final_height')
    #arduino = find_and_connect()   # type: ignore
    
    down = graphic_off = True    
    recpressure=1.02
    recheight=0.01
    max_pressure = 250
    max_caliper = 10000
    max_duty_cycle = 255
    bgc_motor_power='green'
    pshow=[recpressure,max_pressure,'Bar','pressure']
    hshow=[recheight,max_caliper,'mm','height']
    fpressure=max_pressure
    fheight=max_caliper
    recduty=DUTYCYCLE_DEFAULT
    fduty=DUTYCYCLE_DEFAULT
    data_to_send=[]
    mode = IDLE_MODE
    mode_prev = mode
    # Maximum values for scaling (change based on your sensor range)
    loopcounter=0
    height_start=0
    height_remain=fheight-height_start
    f=[]
    window = makewindow()
    # Run the connection process in a separate thread
    

    #threading.Thread(target=run_connection, daemon=True).start()
    p_graph = window["-GRAPHP-"]
    h_graph = window["-GRAPHH-"]

    
        

    # Show log window for 2 seconds on startup
    

    # Run the connection process in a separate thread
    started=0
    # Event loop to process user interactions
    while True:
        #event, values = window.read(timeout=5)
        event, values = window.read(timeout=5)
        loopcounter+=1
        
        if event is sg.WIN_CLOSED:
            break
        elif event =='Exit':
            sg.popup_quick_message('Saving settings & Exiting', text_color='white', background_color='red', font='_ 20')
            for key in keys_to_save:
                window_contents[key] = values[key]
            break
            
        if event == 'log on':
            f.append(1)
            window['-OUTPUT-'].update(visible=True)
        elif event == 'no log':
            f.clear()
            window['-OUTPUT-'].update(visible=False)
            
        elif event == 'PUMP':
            if arduino is not None:
                arduino.write(f'c{fduty}\n'.encode())
                arduino.write(f'P100\n'.encode())
                mode=PUMP_MODE
        elif event == 'STOP':
            if arduino is not None:
                arduino.write(f'S\n'.encode())
                mode=STOP_MODE
        elif event == 'DRAIN':
            if arduino is not None:
                arduino.write(f'D\n'.encode())
            mode=DRAIN_MODE
        elif event == 'PAUSE':
            if arduino is not None:
                arduino.write(f'S\n'.encode())
                mode=PAUSE_MODE
        elif event == 'RUN':
            if arduino is not None:
                arduino.write(f'h{fheight}\n'.encode())
                arduino.write(f'c{fduty}\n'.encode())
                if mode_prev is not RUN_MODE:
                    height_start=recheight
                mode=RUN_MODE
        elif event == "-SIZE-":
            if values['radiosize']:
                if len(values["-SIZE-"])>0:
                    if float(values["-SIZE-"]):
                        fheight = float(values["-SIZE-"])*25.4*0.21
                        window["final_height"].update(f'{fheight:.2f}')
        elif event == 'Reconnect':
            if arduino is not None:
                arduino.close()
            arduino = find_and_connect()  
        elif event == 'DUTY_SLIDER':
            if arduino is not None:
                fduty=int(int(values['DUTY_SLIDER'])*2.55)
                arduino.write(f'c{fduty}\n'.encode())
            pass
        elif event == 'PUMPON':
            if arduino is not None:
                arduino.write(f'c{fduty}\n'.encode())
                arduino.write(f'P1500\n'.encode())
                mode=PUMP_MODE
        elif event == 'SaveSettings':
            filename = sg.popup_get_file('Save Settings', save_as=True, no_window=True)
            window.SaveToDisk(filename)
            # save(values)
        elif event == 'LoadSettings':
            filename = sg.popup_get_file('Load Settings', no_window=True)
            window.LoadFromDisk(filename)
            # load(form)
        
        if started==0:
            started=1
            ports = list_serial_ports()
            pshow=[recpressure,max_pressure,'Bar','pressure']
            hshow=[recheight,max_caliper,'mm','height']
            update_meter(h_graph, recheight,max_caliper,show=hshow )  
            update_meter(p_graph, recpressure,max_pressure,show=pshow )
            window['final_height'].update(f'{fheight/100:.2f}')
            window['final_pressure'].update(f'{fpressure/10:.1f}')
            window['DUTY_SLIDER'].update(fduty/2.55)
            for key in keys_to_save:
                saved_value = window_contents[key]
                window[key].update(saved_value)
            arduino = find_and_connect()
        if arduino is None:
            continue    
        #if type(values['final_pressure']) is type("10.3"):
        fpressure=float(values['final_pressure'])
        #if type(values['final_height']) is type("10.3"):
        fheight = float(values['final_height'])*100
        #if type(values['DUTY_SLIDER']) is type("10.3"):
        fduty=int(int(values['DUTY_SLIDER'])*2.55)
        
        
        # Read data from Arduino
        
        if btndis:
            if time.time() - start_time > 2:
                sg.popup("reading fail","turn on caliper ....")
        

        
        if arduino.in_waiting > 0:
            sanitized_data = read_sanitized_data(arduino=arduino).strip()
            nlc = min(sanitized_data.find('\n'),sanitized_data.find('\r'))
            while nlc>-1:
                nsdata = sanitized_data[0:nlc]
                window['-OUTPUT-'].update(f'{nsdata}\n',append=True)    
                phfc = nsdata.find("pressure:") 
                if phfc >-1:
                    nsdata=nsdata[phfc:len(nsdata)]
                    recpressure= float(nsdata[phfc+len("pressure:"):len(nsdata)])
                    pshow=[recpressure,max_pressure,'Bar','pressure']
                    update_meter(p_graph, recpressure,fpressure,show=pshow )
                    nsdata=nsdata[phfc+len("pressure:"):len(nsdata)]
                phfc = nsdata.find("height:") 
                if phfc >-1:
                    nsdata=nsdata[phfc:len(nsdata)]
                    recheight= float(nsdata[phfc+len("height:"):len(nsdata)])
                    hshow=[recheight,fheight,'mm','height']
                    update_meter(h_graph, recheight,max_caliper,show=hshow )  
                    nsdata=nsdata[phfc+len("height:"):len(nsdata)]
                phfc = nsdata.find("duty:") 
                if phfc >-1:
                    nsdata=nsdata[phfc:len(nsdata)]
                    recduty= int(nsdata[phfc+len("duty:"):len(nsdata)])/2.55
                    window['-MOTOR_VAL-'].update(f'{recduty:.0f}%')
                    window['-MOTOR_VAL-'].update(text_color=get_color(recduty,100))
                    
                    nsdata=nsdata[phfc+len("duty:"):len(nsdata)]
                    if btndis:
                        window['PUMPON'].update(disabled=False)
                        window['PUMP'].update(disabled=False)
                        window['DRAIN'].update(disabled=False)
                        window['PAUSE'].update(disabled=False)
                        window['RUN'].update(disabled=False)
                        window['STOP'].update(disabled=False)
                        btndis=False
                sanitized_data = sanitized_data[nlc+2:len(sanitized_data)]
                nlc = min(sanitized_data.find('\n'),sanitized_data.find('\r'))
            
        
         # Close the window and serial port
        if mode == RUN_MODE:
            #window['DUTY_SLIDER'].update(recduty)
            if fheight>recheight:
                arduino.write(b'R\n')    
            else:
                mode = DONE_MODE
                arduino.write(b'S\n') 
        elif mode == STOP_MODE:
            #arduino.write(b'S\n')  # Send 'S' command to Arduino
            pass
        elif mode == PUMP_MODE:
            if mode_prev is not PUMP_MODE:
                #arduino.write(b'P\n')  # Send 'P' command to Arduino
                pass

            
            
        elif mode == DRAIN_MODE:
            #arduino.write(b'D\n')  # Send 'D' command to Arduino
            pass
        elif mode == PAUSE_MODE:
            #arduino.write(b'S\n')  # Send 'S' command to Arduino
            pass
        elif mode == DONE_MODE:
            if mode_prev is RUN_MODE:
                arduino.write(b'S\n')  # Send 'S' command to Arduino
                sg.popup('Forming finished')
                mode = IDLE_MODE
                pass
        
        mode_prev = mode
    if arduino is not None:
        arduino.write(b'S\n') 
        arduino.close()
    
    window.close()
    


def is_ascii_byte(byte):
    return 0 <= byte < 128
# Function to read and sanitize data from Arduino
def read_sanitized_data(arduino):
    data = bytearray()
    while arduino.in_waiting > 0:
        byte = arduino.read()
        if is_ascii_byte(byte[0]):
            data.append(byte[0])
    return data.decode('utf-8')# Function to read and sanitize data from Arduino


def main():
    loopgui()
    
if __name__ == '__main__':
    main()
