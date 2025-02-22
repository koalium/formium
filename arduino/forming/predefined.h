#ifndef PREDEFINE_H
#define PREDEFINED_H

//
//
#define pwm_motor_off  0
#define pwm_motor_max   255
#define relay_motor_on    1
#define relay_motor_off   0
#define relay_valve_on    1
#define relay_valve_off   0

#define PUMP   1
#define  DUMP  0


#define  DEPEND_PRESSURE  3
#define DEPENDE_HEIGHT   5


#define  HANDLE_RUN      7
#define  HANDLE_PUMP     23
#define  HANDLE_PAUSE    31
#define  HANDLE_DRAIN    41
#define  HANDLE_IDLE     17
#define  HANDLE_PUMPING  53
#define  HANDLE_DUTY     71
#define  HANDLE_HHEIGHT  79
#define  HANDLE_HPRESSURE  73
#define  HANDLE_DEPEND  37
#define  HANDLE_DUMP     41
#define  HANDLE_NAM     59
#define  HANDLE_HAND     61
#define  HANDLE_REC     67


const uint8_t input_size = 64;

char input[input_size];


bool echo = false;
//
int mode = HANDLE_IDLE;
uint8_t dependence = DEPENDE_HEIGHT;

bool handshaked = false;


const int pin_relay_motor_ = 4;
const int pin_pwm_motor = 5;
const int pin_relay_valve = 3;


long prev_caliper_value = 0;
long curr_caliper_value=0;
long start_caliper_value = 0;
long final_caliper_value = 0;
long forming_final_height_value = 2331;
//
long prev_pressure_value = 0;
long curr_pressure=0;
long start_pressure = 0;
long final_pressure = 8033;
long forming_final_pressure_value = 7700;
//
int prev_duty = 0;
int duty = 100;
//


const int duty_max_allowable = 255;
//
const char client_ ='w';
const char server_ = 'W';

const char _pump = 'P';
const char _dump = 'D';
const char _run = 'R';
const char _pause = 'S';
const char _fheight = 'h';
const char _fpressure = 'p';
const char _depend = 'd';
const String _duty = "duty";
const char _handshake = 'H';
const char _name = 'N';
const String _height = "height";
const String _pressure = "pressure";
const String _mode = "mood";
const char _Mode = 'M';
const char _JobDone = 'J';
const char _eol = 0x35;
const char _mol = (byte) 255;
const char _psb = 0x66;
const char _peb = 0x52;
const char _instruction = 0x40;
const char _data = 0x60;

const uint32_t dtime_done =3000;
uint32_t ptime =0;
uint32_t stime =0;
uint32_t ctime =0;
uint32_t ftime =0;


struct sysFlags{
uint8_t pumpstate:1;
uint8_t drainValveState:1;
uint8_t dependPressure:1;
uint8_t dependHeight:1;
uint8_t updateCaliper:1;
uint8_t updatPressure:1;
uint8_t updateDuty:1;
uint8_t caliperReading:1;
uint8_t caliperSending:1;
uint8_t pressureReading:1;
uint8_t pressureSending:1;
uint8_t dutyReading:1;
uint8_t dutySending:1;
uint8_t manualMode:1;
uint8_t autoMode:1;
uint8_t handshaked:1;
uint8_t handshaking:1;
} flg;

struct sysData{
uint8_t pumpDuty;
uint32_t caliperValue;
uint32_t pressureValue;
} data,startData,formingData,readData,currData,reciveData;

struct sysState{
uint8_t run:1;
uint8_t pause:1;
uint8_t stop:1;
uint8_t idle:1;

uint32_t startTime;

};

void initAtStart(){
flg.autoMode = 0;
flg.caliperReading = 0;
flg.dutyReading=0;
flg.caliperSending=0;
flg.pressureReading=0;
flg.dependPressure=0;
flg.dependHeight=0;
flg.pressureSending=0;
flg.updatPressure=0;
flg.updateDuty=0;
flg.updateCaliper=0;
flg.drainValveState=0;
flg.pumpstate=0;
data.caliperValue=0;
data.pressureValue=0;
data.pumpDuty=0;
flg.handshaked=0;
flg.handshaking=0;

}
const int pin_seg_a = 7;
const int pin_seg_b = 7;
const int pin_seg_c = 7;
const int pin_seg_d = 7;
const int pin_seg_e = 7;
const int pin_seg_f = 7;
const int pin_seg_g = 7;
const int pin_seg_dot = 7;
const int pin_abode_green = 7;
const int pin_abode_red = 7;


#define seg_a_on()
#define seg_a_off()
#define seg_b_on()
#define seg_b_off()
#define seg_c_on()
#define seg_c_off()
#define seg_d_on()
#define seg_d_off()
#define seg_e_on()
#define seg_e_off()
#define seg_f_on()
#define seg_f_off()
#define seg_g_on()
#define seg_g_off()
#define seg_dot_on()
#define seg_dot_off()
#define green_on()
#define green_off()
#define red_on()
#define red_off()



#endif