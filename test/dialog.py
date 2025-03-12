import serial
import os
import time



STATUS = {
    
    "INACTIVE" : "c,STATUS,INACTIVE", #In this state the device has never been contacted by the VMC
    "DISABLED" : "c,STATUS,DISABLED", # The device has communicated with the VMC but waiting to be enabled
    "ENABLED" : "c,STATUS,ENABLED", # Device enabled by the VMC, waiting for a vending request
    "VEND" : "c,STATUS,VEND", # The device gets c,STATUS,VEND,<amount>,<product ID> when a product has been selected on the VMC
    "IDLE" : "c,STATUS,IDLE", # Session goes back to IDLE when the device is waiting for the VMC to end session
    "DISPENSED" : "c,VEND,SUCCESS", #This message is received when the vending machine has successfully dispensed the product
    "FAIL2DISPENSE" : "c,ERR,VEND 3", #This message is received when the vending machine couldn't dispense the product (e.g coffee machine out of water, or coil machine with empty coil)
}

AUTHORIZE_VEND = "C,VEND," # Prefix to send to authorize a vend request in VEND state (e.g. C,VEND,<requested_amount>)
DENY_VEND = "C,STOP" #Message to send to deny a vend request from the vending machine




#### Serial Port functions to interact with MDB USB/Pi Hat

def openSerial():
    global ser
    ser = serial.Serial() #Create Serial Object
    ser.baudrate = 115200 #Set the appropriate BaudRate
    ser.timeout = 50 #The maximum timeout that the program waits for a reply. If 0 is used, the pot is blocked until readline returns
    ser.port = '/dev/tty.usbmodem01' # Specify the device file descriptor, on windows use "COMX"
    ser.open() #Open the serial connection



def write2Serial(msg):
    global ser
    #DEBUG print("Sending " + msg)
    ser.write((msg+"\n").encode()) #Write the message to send encoded in Binary
    ser.flush()
    


def readSerial():
    global ser
    s = ser.readline().decode("ascii").strip("\n").strip("\r") # Read the response

    if s:
        #DEBUG print("Read:" + s)
        return s
    return ""
    
#### Utilities ###########################

#Function to print to console
def print2Console(msg):
    clearConsole()
    print("\r" + msg,end="\r")



#Function to clear the console to wipe previous messages
def clearConsole():
    
    if os.name in ('nt', 'dos'): #Windows
        os.system("cls")
    else: 
        os.system("clear") #Linux
#### Cashless API Related Functions ######


def initCashlessDevice():
    write2Serial("C,0") #It is advised to shut down cashless while initializing
    write2Serial("C,1")






if __name__ == '__main__':

    openSerial()

    initCashlessDevice()

    while True:
        time.sleep(1) #Wait for 1 second
        rcv = readSerial()

        if rcv == STATUS["INACTIVE"] or rcv == STATUS["DISABLED"]:
            print2Console("Waiting for vending machine...")
        
        elif rcv == STATUS["ENABLED"]:
            print2Console("Please select product on vending machine.")
        
        elif STATUS["VEND"] in rcv:
            vendAmt = rcv.split(",")[3] #c,STATUS,VEND,<amount>,<product_id>
            prodId = rcv.split(",")[4] #In case the product ID Is to be used for anything

            clearConsole()
            while True:
                
                i = input("\rPress v to pay " + vendAmt + " or x to cancel")
                
                if i == "v":
                    write2Serial(AUTHORIZE_VEND + vendAmt)
                    print2Console("Waiting product dispense...")
                    break
                elif i == "x":
                    write2Serial(DENY_VEND)
                    print2Console("Transaction ancelled by user.")
                    break


                clearConsole()
                continue

            
        elif rcv == STATUS["DISPENSED"]:
            print2Console("Product dispensed!")

        elif rcv == STATUS["FAIL2DISPENSE"]:
            print2Console("Product failed to dispense.")
        elif rcv == STATUS["IDLE"]:
            print2Console("Transaction finished.")
        else:
            continue