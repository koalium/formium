import serial
import FreeSimpleGUI as sg
import serial.tools.list_ports
from string import *





def sanitize_input(data):
    return ''.join([str(c) for c in data if ord(c) < 128])

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_to_port(port):
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        sg.popup("Success", f"Connected to {port}")
        return ser
    except serial.SerialException as e:
        sg.popup_error("Error", f"Failed to connect to {port}: {e}")

# Set up serial communication with the Arduino
#arduino = #serial.Serial('COM7', 115200)  # Replace 'COM7' with your Arduino's serial port

# Function to determine color based on value
def get_color(value, max_value):
    ratio = value / max_value
    if ratio >= 0.8:
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
    layout = [
         [sg.Menu(menu_def, tearoff=False)],
         [sg.Text('Select a serial port:')],
    [sg.Combo(ports, key='-PORT-', size=(20, 1))],
    [sg.Button('Connect')],
    [sg.Text('Sensor Values', font=('Helvetica', 20), justification='center', expand_x=True)],
    
    [sg.Column(
        [[sg.Slider(range=(0, 255), orientation='v', size=(10, 10), key='FPRESSURE_SLIDER', enable_events=True)],], element_justification='center'),
        sg.Column([[
     sg.Frame('Pressure', [[sg.Text('', key='PRESSURE_VAL', font=('Helvetica', 24, 'bold'), justification='center', pad=(0, 70))]],
              size=(200, 200), background_color='green', key='PRESSURE_FRAME', element_justification='center', border_width=5, relief='raised'),
     sg.Frame('Caliper', [[sg.Text('', key='CALIPER_VAL', font=('Helvetica', 24, 'bold'), justification='center', pad=(0, 70))]],
              size=(200, 200), background_color='green', key='CALIPER_FRAME', element_justification='center', border_width=5, relief='raised')],],element_justification='center'),
     sg.Column([[sg.Slider(range=(0, 255), orientation='v', size=(10, 10), key='FHEIGHT_SLIDER', enable_events=True)],], element_justification='center')],


    [sg.Text('_' * 80, text_color='grey', pad=(5, 5), expand_x=True)],
    [sg.Frame('Duty Cycle', [[sg.ProgressBar(100, orientation='h', size=(20, 20), key='DUTY_CYCLE_BAR')],
                             [sg.Slider(range=(0, 255), orientation='h', size=(20, 20), key='DUTY_CYCLE_SLIDER', enable_events=True)]], 
              element_justification='center', expand_x=True)],
    [sg.Text('Control', font=('Helvetica', 20), justification='center', expand_x=True)],
    [sg.Button('Pump ON', key='PUMP', button_color=('white', 'blue'), size=(10, 2)),
     sg.Button('Pump OFF', key='STOP_PUMP', button_color=('white', 'blue'), size=(10, 2))],
    [sg.Button('Dump ON', key='DUMP', button_color=('white', 'orange'), size=(10, 2)),
     sg.Button('Dump OFF', key='STOP_DUMP', button_color=('white', 'orange'), size=(10, 2))],
    [sg.Button('Quit', button_color=('white', 'red'), size=(10, 2))]
    ]

    # Create the window
    window = sg.Window('Arduino Sensor Values and Control', layout, finalize=True, element_justification='center')
    return window

def loopgui():
    # Maximum values for scaling (change based on your sensor range)
    arduino = serial.Serial('COM7', 115200) 
    max_pressure = 1023
    max_caliper = 1023
    max_duty_cycle = 255
    window = makewindow()
    # Event loop to process user interactions
    while True:
        event, values = window.read(timeout=100)

        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        
        
        if arduino.in_waiting > 0:
            sanitized_data = read_sanitized_data(arduino=arduino).strip()
            
            
            if sanitized_data.find("f:"):
                window['PRESSURE_VAL'].update(sanitized_data[sanitized_data.find("f:")+2:len(sanitized_data)])
            
            

        if event == 'PUMP':
            arduino.write(b'PUMP\n')  # Send 'PUMP' command to Arduino
        elif event == 'STOP_PUMP':
            arduino.write(b'STOP_PUMP\n')  # Send 'STOP_PUMP' command to Arduino
        elif event == 'DUMP':
            arduino.write(b'DUMP\n')  # Send 'DUMP' command to Arduino
        elif event == 'STOP_DUMP':
            arduino.write(b'STOP_DUMP\n')  # Send 'STOP_DUMP' command to Arduino
        elif event == 'DUTY_CYCLE_SLIDER':
            duty_cycle_value = values['DUTY_CYCLE_SLIDER']
            arduino.write(f'DUTY:{int(duty_cycle_value)}\n'.encode())
        elif event == 'FPRESSURE_SLIDER':
            fpressure_value = values['FPRESSURE_SLIDER']
            arduino.write(f'FPRESSURE:{int(fpressure_value)}\n'.encode())
        elif event == 'FHEIGHT_SLIDER':
            fheight_value = values['FHEIGHT_SLIDER']
            arduino.write(f'FHEIGHT:{int(fheight_value)}\n'.encode())
        elif event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Select Serial Port':
            ports = list_serial_ports()
            window['-PORT-'].update(values=ports)
        elif event == 'Connect':
            selected_port = values['-PORT-']
            if selected_port:
                arduino.close()
                arduino = connect_to_port(selected_port)
            else:
                sg.popup_error("Error", "Please select a port")
        # Read data from Arduino
        
    # Close the window and serial port
    window.close()
    arduino.close()


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

loopgui()