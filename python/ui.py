import serial
import FreeSimpleGUI as sg
import serial.tools.list_ports
from string import *

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
    if ratio==1:
        return'blue'
    elif ratio>=1:
        return 'purple'
    elif ratio >= 0.8:
        return 'red'
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
    menu_def = [['File', ['Exit']],
            ['Settings', ['Select Serial Port']]]
    
    layout_t=[[sg.Frame("Monitoring", [
        [sg.Graph(canvas_size=(200, 200), graph_bottom_left=(0, 0), graph_top_right=(200, 200), key="-GRAPHH-", background_color='white'), 
         sg.Graph(canvas_size=(200, 200), graph_bottom_left=(0, 0), graph_top_right=(200, 200), key="-GRAPHP-", background_color='white')]
    ], border_width=2)],]

    layout_progress_graph = [  sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key='-GRAPHH-',background_color=bgcwin),sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key='-GRAPHP-',background_color=bgcwin)]

    col_1 =[
        sg.Column([[
     sg.Frame("Control Inputs", [[sg.Combo(ports, key='-PORT-', size=(20, 1))],
    [sg.Button('Connect')],
        [sg.Text("Final Height:"), sg.Stretch(), sg.InputText("", justification='center',key="final_height", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="height_dependency",default=True, enable_events=True)],[
        sg.Text("Final Pressure:"), sg.Stretch(),sg.InputText("", justification='center',disabled=True,key="final_pressure", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="pressure_dependency",disabled=True)]
         ,[
        sg.Text("Final forming:"), sg.Stretch(),sg.InputText("", justification='center',disabled=True,key="final_form", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="pressure_dependency",disabled=True)]
         ]
    , border_width=2, element_justification='stretch'),
     sg.Frame('Motor Power', [[sg.Text('', key='-MOTOR_VAL-', font=('Helvetica', 24, 'bold'), justification='center', pad=(0, 70))]],
              size=(200, 200), background_color='green', key='MOTOR_FRAME', element_justification='center', border_width=5, relief='raised'),],],element_justification='center'),
     sg.Column([[sg.Slider(range=(0, 100), orientation='v', size=(12, 15), key='DUTY_SLIDER', enable_events=True)],], element_justification='left')]
    
    layout_control=[
    [sg.Button('Pump', key='PUMP', button_color=('yellow', 'blue'), size=(10, 2)),sg.Button('Pause', key='PAUSE', button_color=('yellow', 'orange'), size=(10, 2)),
     sg.Button('Drain', key='DRAIN', button_color=('yellow', 'magenta'), size=(10, 2),metadata=BtnInfo())],
    [sg.Button('Run', key='RUN', button_color=('yellow', 'green'), size=(10, 2)),
              
     sg.Button('Stop', key='STOP', button_color=('yellow', 'red'), size=(10, 2))],
    [sg.Button('Pump ON', key='PUMP', button_color=('yellow', 'blue'), size=(10, 2))]]

    layout = [layout_progress_graph,
         [sg.Menu(menu_def, tearoff=False)],
         col_1,layout_control
    ]

    # Create the window
    window = sg.Window('Arduino Sensor Values and Control', layout, finalize=True, element_justification='center',location=(100, 100),background_color=bgcwin)
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
def loopgui():
    
    arduino = None   # type: ignore
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
    
    window = makewindow()
    p_graph = window["-GRAPHP-"]
    h_graph = window["-GRAPHH-"]
    # Event loop to process user interactions
    while True:
        event, values = window.read(timeout=5)
        loopcounter+=1
        
        if event in (sg.WIN_CLOSED, 'Quit'):
            break

        if event == 'PUMP':
            
            arduino.write(f'c{fduty}\n'.encode())
            arduino.write(f'P100\n'.encode())
            mode=PUMP_MODE
        elif event == 'STOP':
            arduino.write(f'S\n'.encode())
            mode=STOP_MODE
        elif event == 'DRAIN':
            arduino.write(f'D\n'.encode())
            mode=DRAIN_MODE
        elif event == 'PAUSE':
            arduino.write(f'S\n'.encode())
            mode=PAUSE_MODE
        elif event == 'RUN':
            arduino.write(f'h{fheight}\n'.encode())
            
            arduino.write(f'c{fduty}\n'.encode())
            if mode_prev is not RUN_MODE:
                height_start=recheight
            mode=RUN_MODE
        elif event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Select Serial Port':
            ports = list_serial_ports()
            window['-PORT-'].update(values=ports)
        elif event == 'Connect':
            selected_port = values['-PORT-']
            if selected_port:
                if arduino is not None:
                    arduino.close()
                arduino = connect_to_port(selected_port)
            else:
                sg.popup_error("Error", "Please select a port")
        elif event == 'DUTY_SLIDER':
            arduino.write(f'c{fduty}\n'.encode())
            pass
        
        if loopcounter==1:
            ports = list_serial_ports()
            window['-PORT-'].update(values=ports)
            pshow=[recpressure,max_pressure,'Bar','pressure']
            hshow=[recheight,max_caliper,'mm','height']
            update_meter(h_graph, recheight,max_caliper,show=hshow )  
            update_meter(p_graph, recpressure,max_pressure,show=pshow )
            window['final_height'].update(fheight/100)
            window['final_pressure'].update(fpressure/10)
        if arduino is None:
            continue    
        
        fpressure=float(values['final_pressure'])
        fheight = float(values['final_height'])*100
        fduty=int(int(values['DUTY_SLIDER'])*2.55)
        # Read data from Arduino
        
        
        

        
        if arduino.in_waiting > 0:
            sanitized_data = read_sanitized_data(arduino=arduino).strip()
            nlc = min(sanitized_data.find('\n'),sanitized_data.find('\r'))
            while nlc>-1:
                nsdata = sanitized_data[0:nlc]

                phfc = nsdata.find("pressure:") 
                if phfc >-1:
                    nsdata=nsdata[phfc:len(nsdata)]
                    recpressure= float(nsdata[phfc+len("pressure:"):len(nsdata)])
                    pshow=[recpressure,max_pressure,'Bar','pressure']
                    update_meter(p_graph, recpressure,max_pressure,show=pshow )
                    nsdata=nsdata[phfc+len("pressure:"):len(nsdata)]
                phfc = nsdata.find("height:") 
                if phfc >-1:
                    nsdata=nsdata[phfc:len(nsdata)]
                    recheight= float(nsdata[phfc+len("height:"):len(nsdata)])
                    hshow=[recheight,max_caliper,'mm','height']
                    update_meter(h_graph, recheight,max_caliper,show=hshow )  
                    nsdata=nsdata[phfc+len("height:"):len(nsdata)]
                phfc = nsdata.find("duty:") 
                if phfc >-1:
                    nsdata=nsdata[phfc:len(nsdata)]
                    recduty= float(nsdata[phfc+len("duty:"):len(nsdata)])/2.55
                    window['-MOTOR_VAL-'].update(f'{recduty:.0f}%')
                    nsdata=nsdata[phfc+len("duty:"):len(nsdata)]
                sanitized_data = sanitized_data[nlc+2:len(sanitized_data)]
                nlc = min(sanitized_data.find('\n'),sanitized_data.find('\r'))
            
        
         # Close the window and serial port
        if mode == RUN_MODE:
            
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
