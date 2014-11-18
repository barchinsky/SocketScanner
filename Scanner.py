import sys, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ConfigManager import ConfigManager
import socket

class Scanner(QWidget):
    def __init__(self, parent=None):
        super(Scanner, self).__init__(parent)

        self.cfg = ConfigManager()

        self.progressbar = QProgressBar()
        self.button = QPushButton('Start')
        self.button.clicked.connect(self.handleButton)

        self.clientIpComment = QLabel("Enter client IP:")
        self.clientIpValue = QLineEdit()
        self.clientIpValue.setText(self.cfg.getClientIp())

        self.scanRangeLbl = QLabel("Choose port range:")
        self.portFromLbl = QLabel("From")
        self.portToLbl = QLabel("To")
        self.portFromValue = QLineEdit('1')
        self.portToValue = QLineEdit('90')

        self.openedPortsLbl = QLabel('Open ports:')
        self.openedPortsValue = QLineEdit()

        self.closeBtn = QPushButton("Exit")

        self.connect(self.closeBtn,SIGNAL("clicked()"),self,SLOT("close()"))

        main_layout = QGridLayout()
        main_layout.addWidget(self.clientIpComment,0,0)
        main_layout.addWidget(self.clientIpValue,0,1)
        main_layout.addWidget(self.scanRangeLbl,1,0)
        main_layout.addWidget(self.portFromLbl,2,0)
        main_layout.addWidget(self.portFromValue,2,1)
        main_layout.addWidget(self.portToLbl,2,2)
        main_layout.addWidget(self.portToValue,2,3)
        main_layout.addWidget(self.button, 3, 0)
        main_layout.addWidget(self.progressbar, 3, 1)
        main_layout.addWidget(self.openedPortsLbl,4,0)
        main_layout.addWidget(self.openedPortsValue,4,1)
        main_layout.addWidget(self.closeBtn,4,3)
        self.setLayout(main_layout)
        self.setWindowTitle('Progress')
        self._active = False

    def handleButton(self):
        if not self._active:
            self._active = True
            self.button.setText('Stop')
            if self.progressbar.value() == self.progressbar.maximum():
                self.progressbar.reset()
            QTimer.singleShot(0, self.startLoop)
        else:
            self._active = False

    def closeEvent(self, event):
        self._active = False

    def startLoop(self):
        host= self.cfg.getClientIp()
        ports=[]
        openPorts=[]
        minimum = int(self.portFromValue.text())
        maximum = int(self.portToValue.text())

        if minimum > maximum:
            self.show_info("Minimum is bigger than maximum. Please check the values.")
            self.button.setText('Start')
            self._active = False
            self.openedPortsValue.setText('0')
            return

        self.progressbar.setMinimum(minimum)
        self.progressbar.setMaximum(maximum)
        # generate ports set
        for i in xrange(minimum,maximum+1):
            ports.append(i)

        while True:
            time.sleep(0.05)

            for port in ports:
                print port
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.settimeout(0.1)
                if not sock.connect_ex((host,port)):
                    print("Port %s is closed" % port )
                else:
                    openPorts.append(port)
                    print("Port %s is open" % port)
                    sock.close()
            
                value = port
                print 'value',value 
                self.progressbar.setValue(value)
                qApp.processEvents()
                if (not self._active or
                    value >= self.progressbar.maximum()):
                    self.savePorts(openPorts)
                    self.show_info("Scanning finished.")

            self.openedPortsValue.setText(str(len(openPorts)))
            self.button.setText('Start')
            self._active = False
            break

    def savePorts(self,openPorts):
        fileName = self.cfg.getSaveFile()+'_'+str(int(time.time()))
        with open(fileName,'w') as f:
            for port in openPorts:
                f.write(str(port)+'\n')

    def show_info(self,e):
        msgBox = QMessageBox()
        msgBox.setText(str(e))
        msgBox.setStandardButtons(QMessageBox.Ok)
        ret = msgBox.exec_();


app = QApplication(sys.argv)
bar = Scanner()
bar.show()
sys.exit(app.exec_())