#!/usr/bin/env python
import sys
import threading
from steamcontroller import SteamController

class ControllerSteamController:
    def __init__(self):
        # Initialize dict that stores the controller button states. The keys corresponds to the
        # button values (sci.buttons) from the controller.The values for the triggers, pads and
        # giro's are also added to the dict.
        self.btns = {0:     {'type': 'trigger', 'name': 'LTRIG', 'value': 0}
                    ,2<< 0: {'type': 'trigger', 'name': 'RTRIG', 'value': 0} 
                    ,2<< 1: {'type': 'pad',     'name': 'LPAD_X', 'value': 0} 
                    ,2<< 2: {'type': 'pad',     'name': 'LPAD_Y', 'value': 0} 
                    ,2<< 3: {'type': 'pad',     'name': 'RPAD_X', 'value': 0} 
                    ,2<< 4: {'type': 'pad',     'name': 'RPAD_Y', 'value': 0}
                    
                    ,2<<15: {'type': 'giro',    'name': 'GPITCH', 'value': 0}
                    ,2<<16: {'type': 'giro',    'name': 'GROLL',  'value': 0}
                    ,2<<17: {'type': 'giro',    'name': 'GYAW',   'value': 0}

                    ,2<< 7: {'type': 'button',  'name': 'RT',     'value': 0}          #2^7=256
                    ,2<< 8: {'type': 'button',  'name': 'LT',     'value': 0}          #2^8=512
                    ,2<< 9: {'type': 'button',  'name': 'RB',     'value': 0}
                    ,2<<10: {'type': 'button',  'name': 'LB',     'value': 0}
                    ,2<<11: {'type': 'button',  'name': 'Y',      'value': 0}
                    ,2<<12: {'type': 'button',  'name': 'B',      'value': 0}
                    ,2<<13: {'type': 'button',  'name': 'X',      'value': 0}
                    ,2<<14: {'type': 'button',  'name': 'A',      'value': 0}
                    ,2<<19: {'type': 'button',  'name': 'BACK',   'value': 0}          #2^19=1048576
                    ,2<<20: {'type': 'button',  'name': 'STEAM',  'value': 0}
                    ,2<<21: {'type': 'button',  'name': 'START',  'value': 0}
                    ,2<<22: {'type': 'button',  'name': 'LGRIP',  'value': 0}
                    ,2<<23: {'type': 'button',  'name': 'RGRIP',  'value': 0}
                    ,2<<24: {'type': 'button',  'name': 'LPAD',   'value': 0}
                    ,2<<25: {'type': 'button',  'name': 'RPAD',   'value': 0}
                    ,2<<26: {'type': 'button',  'name': 'LPADTOUCH', 'value': 0}
                    ,2<<27: {'type': 'button',  'name': 'RPADTOUCH', 'value': 0}     #2^27=268435546
        }

        # Add additional dict that translates human friendly name to event code.
        self.btn_keys = {self.btns[x]['name']:x for x in self.btns}

        # Create device for Steam Controller
        try:
            # Create SteamController device
            self.device = SteamController(callback=self.get_events)

            # Create thread to start SteamController.run() in the background
            self.thread = threading.Thread(target=self.device.run)
            self.thread.start()
            print("Steam controller thread started")
            
        except Exception as e:
            sys.stderr.write(str(e) + '\n')

    def get_button_value(self, name):
        return self.btns[self.btn_keys[name]]['value']
    
    def get_events(self,sc,sci):
        """Get events from controller

        At each interval the all the triggers, pads giros and buttons are processed
        in this function.

        When the all the inputs are processed a callback function is called, which enables 
        further processing of the controller input.
        """
        self.btns[0]['value']    =sci.ltrig
        self.btns[2<<0]['value'] =sci.rtrig
        self.btns[2<<1]['value'] =sci.lpad_x
        self.btns[2<<2]['value'] =sci.lpad_y
        self.btns[2<<3]['value'] =sci.rpad_x
        self.btns[2<<4]['value'] =sci.rpad_y
        self.btns[2<<15]['value']=sci.gpitch
        self.btns[2<<16]['value']=sci.groll
        self.btns[2<<17]['value']=sci.gyaw

        for key in self.btns.keys():
            if self.btns[key]['type'] == "button":
                self.btns[key]['value'] = int((sci.buttons & key) > 0)


    def dump_events(self,sc,sci):
        print(sci)
         
if __name__ == '__main__':
    import time

    controller = ControllerSteamController()
    while True:
        try:
            print(".",end="", flush=True)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt")
            controller.device.addExit()
            break    

    print("Done")