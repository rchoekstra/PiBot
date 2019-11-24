#!/usr/bin/env python
import evdev
import asyncio

class ControllerLogitechPrecision:
    def __init__(self, callback, input_device):
        self.callback = callback
        self.device = evdev.InputDevice(input_device)
        print(self.device)

        self.btns = {  0: {'name': 'X', 'value': 128}
                    ,  1: {'name': 'Y', 'value': 128}
                    ,  2: {'name': 'LEFT', 'value': 0}
                    ,  3: {'name': 'RIGHT', 'value': 0}
                    ,  4: {'name': 'UP', 'value': 0}
                    ,  5: {'name': 'DOWN', 'value': 0}
                    ,288: {'name': '1', 'value': 0}
                    ,289: {'name': '2', 'value': 0}
                    ,290: {'name': '3', 'value': 0}
                    ,291: {'name': '4', 'value': 0}
                    ,292: {'name': '5', 'value': 0}
                    ,293: {'name': '6', 'value': 0}
                    ,294: {'name': '7', 'value': 0}
                    ,295: {'name': '8', 'value': 0}
                    ,296: {'name': 'BACK', 'value': 0}
                    ,297: {'name': 'START', 'value': 0}
        }

        self.btn_keys = {self.btns[x]['name']:x for x in self.btns}


    async def get_events(self):
        tmp = {}
        async for event in self.device.async_read_loop():
            if event.type in (evdev.ecodes.EV_KEY, evdev.ecodes.EV_ABS):
                self.btns[event.code]['value'] = event.value

                # Recode left/right
                if event.code==0:
                    if self.btns[0]['value']==1:    # LEFT
                        self.btns[2]['value']=1
                        self.btns[3]['value']=0
                    elif self.btns[0]['value']==128: # CENTER
                        self.btns[2]['value']=0
                        self.btns[3]['value']=0
                    elif self.btns[0]['value']==255: #RIGHT
                        self.btns[2]['value']=0
                        self.btns[3]['value']=1

                # Recode up/down
                elif event.code==1:
                    if self.btns[1]['value']==1:    # UP
                        self.btns[4]['value']=1
                        self.btns[5]['value']=0
                    elif self.btns[1]['value']==128: # CENTER
                        self.btns[4]['value']=0
                        self.btns[5]['value']=0
                    elif self.btns[1]['value']==255: #DOWN
                        self.btns[4]['value']=0
                        self.btns[5]['value']=1

                #for btn in self.btns:
                #    print(self.btns[btn]['name'],': ', self.btns[btn]['value'], sep='')
                #print("")
                self.callback("input.gamepad",self.btns) # self.btns: within ControllerLogitechPrecision of PiBot?

        await asyncio.sleep(1/125) # Polling rate of 125Hz

def process_event_test(event, value):
    print(f"type: {event}")

    if event=='input.gamepad':
        print(value)

if __name__ == '__main__':
    controller = ControllerLogitechPrecision(process_event_test, '/dev/input/event2')
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(controller.get_events())
        loop.run_forever()
    except KeyboardInterrupt as e:
        print("Catched KeyboardInterrupt")

    finally:
        print("Close async loop")
        loop.close()

    