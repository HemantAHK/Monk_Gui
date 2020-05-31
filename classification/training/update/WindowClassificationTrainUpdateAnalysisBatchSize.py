import os
import sys
import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class WindowClassificationTrainUpdateAnalysisBatchSize(QtWidgets.QWidget):

    forward_visualize = QtCore.pyqtSignal();
    backward_data_param = QtCore.pyqtSignal();


    def __init__(self):
        super().__init__()
        self.cfg_setup()
        self.title = 'Experiment {} - Analyse Batch Size Hyperparam'.format(self.system["experiment"])
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 600
        self.initUI()

    def cfg_setup(self):
        with open('base_classification.json') as json_file:
            self.system = json.load(json_file)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height);


        # Backward
        self.b1 = QPushButton('Back', self)
        self.b1.move(600,550)
        self.b1.clicked.connect(self.backward)

        # Forward
        self.b2 = QPushButton('Next', self)
        self.b2.move(700,550)
        self.b2.clicked.connect(self.forward)

        # Quit
        self.b3 = QPushButton('Quit', self)
        self.b3.move(800,550)
        self.b3.clicked.connect(self.close)


        
        self.l1 = QLabel(self);
        self.l1.setText("1. Analysis name:");
        self.l1.move(20, 20);

        self.e1 = QLineEdit(self)
        self.e1.move(170, 20);
        self.e1.resize(200, 25);
        self.e1.setText(self.system["analysis"]["batch_size"]["analysis_name"]);


        self.l2 = QLabel(self);
        self.l2.setText("2. Percent Data:");
        self.l2.move(420, 20);

        self.e2 = QLineEdit(self)
        self.e2.move(570, 20);
        self.e2.setText(self.system["analysis"]["batch_size"]["percent"]);



        self.l3 = QLabel(self);
        self.l3.setText("3. Sizes list:");
        self.l3.move(20, 70);

        self.e3 = QLineEdit(self)
        self.e3.move(170, 70);
        self.e3.setText(self.system["analysis"]["batch_size"]["list"]);


        self.l4 = QLabel(self);
        self.l4.setText("4. Num epochs:");
        self.l4.move(420, 70);

        self.e4 = QLineEdit(self)
        self.e4.move(570, 70);
        self.e4.setText(self.system["analysis"]["batch_size"]["epochs"]);


        self.b5 = QPushButton('Start Experiment', self)
        self.b5.move(20, 150)
        self.b5.clicked.connect(self.start)


        self.l5 = QLabel(self);
        self.l5.setText("Experiment Not Started");
        self.l5.resize(200, 25)
        self.l5.move(250, 150);


        self.b6 = QPushButton('Stop Experiment', self)
        self.b6.move(600, 150)
        self.b6.clicked.connect(self.stop)



        self.te1 = QTextBrowser(self);
        self.te1.move(20, 220);
        self.te1.setFixedSize(800, 300);
        self.te1.setText(self.system["analysis"]["batch_size"]["analysis"]);

    

        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.finished.connect(self.finished)



    def start(self):
        self.l5.setText("Experiment Running")
        self.te1.setText("");

        self.system["analysis"]["batch_size"]["analysis_name"] = self.e1.text();
        self.system["analysis"]["batch_size"]["percent"] = self.e2.text();
        self.system["analysis"]["batch_size"]["list"] = self.e3.text();
        self.system["analysis"]["batch_size"]["epochs"] = self.e4.text();

        with open('base_classification.json', 'w') as outfile:
            json.dump(self.system, outfile)

        if self.system["datatype"] == "image" and self.system["labeltype"] == "single":
            os.system("cp cfg/classification/update/analyse_batch_size.py .");
            os.system("cp cfg/classification/update/analyse_batch_size.sh .");

        self.process.start('bash', ['analyse_batch_size.sh'])
        self.append("Process PID: " + str(self.process.pid()) + "\n");


    def stop(self):
        self.l5.setText("Experiment Interrupted")
        self.process.kill();
        self.append("Experiment Stopped\n")
        QMessageBox.about(self, "Experiment Status", "Interrupted");


    def finished(self):
        pass;


    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        if("Completed" in text):
            self.l5.setText("Experiment Completed");
        self.system["analysis"]["batch_size"]["analysis"] += text;
        self.append(text)


    def stderrReady(self):
        text = str(self.process.readAllStandardError().data(), encoding='utf-8')
        QMessageBox.about(self, "Experiment Status", "Errors Found");
        self.tb1.setText("Errors Found");
        self.append(text)


    def append(self, text):
        cursor = self.te1.textCursor()  
        self.te1.ensureCursorVisible() 
        cursor.movePosition(cursor.End)
        cursor.insertText(text)






    def forward(self):        
        with open('base_classification.json', 'w') as outfile:
            json.dump(self.system, outfile)
        self.forward_visualize.emit();


    def backward(self):
        with open('base_classification.json', 'w') as outfile:
            json.dump(self.system, outfile)
        self.backward_data_param.emit();


    



'''
app = QApplication(sys.argv)
screen = WindowClassificationTrainUpdateAnalysisBatchSize()
screen.show()
sys.exit(app.exec_())
'''