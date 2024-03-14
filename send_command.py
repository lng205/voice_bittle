from ardSerial import connectPort, closeAllSerial, send, keepCheckingPort, threading

def initBittle():
    goodPorts = {}
    connectPort(goodPorts)
    t=threading.Thread(target = keepCheckingPort, args = (goodPorts,))
    t.start()
    send(goodPorts, ['G',0.1])
    return goodPorts

def closeBittle(goodPorts):
    closeAllSerial(goodPorts)

def sendCommand(goodPorts, command):
    send(goodPorts, [command,0.1])