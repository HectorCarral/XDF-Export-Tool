import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QFileDialog, QPushButton
import export_xdf_stream as xdf_exp


class XDFExporter(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.files = None
        self.fileEdit = None
        self.streamName = None
        self.markersStreamName = None
        self.subjectNumber = None
        self.markersToWrite = None
        self.log = None
        
        self.initUI()
        
    def selectFile(self):
        self.files = QFileDialog.getOpenFileNames(filter="(*.xdf)")[0]
        self.fileEdit.setText('[' + ', '.join(self.files) + ']')
        
        
    def exportStream(self):
        self.log.append("Exporting...")
        self.log.repaint()
        QApplication.processEvents()
        
        markers = []
        if self.markersToWrite.text() is not '':
            markers = [int(x) for x in self.markersToWrite.text().split(',')]
        
        for file in self.files:
            result = xdf_exp.exportStream(file, self.streamName.text(), self.markersStreamName.text(), markers)

            self.log.append(result)
            self.log.repaint()
            QApplication.processEvents()
        
        self.log.append("Done!")
        self.log.repaint()
        QApplication.processEvents()
        

    def initUI(self):
        streamNameLabel = QLabel('Stream name')
        markersStreamNameLabel = QLabel('Markers stream name')
        markersToWriteLabel = QLabel ('Markers to write')
        logLabel = QLabel('Log')
        
        streamNameLabel.setToolTip("Name of the desired stream to export")
        markersStreamNameLabel.setToolTip("Optional: Name of the markers stream to export")
        markersToWriteLabel.setToolTip("Optional: To select only some markers to export, separated by commas")

        self.fileEdit = QLineEdit()
        self.streamName = QLineEdit()
        self.markersStreamName = QLineEdit()
        self.markersToWrite = QLineEdit()
        self.log = QTextEdit()
        
        fileSelectButton = QPushButton('Select XDF file(s)', self)
        fileSelectButton.clicked.connect(self.selectFile)
        
        exportButton = QPushButton('Export stream(s)', self)
        exportButton.clicked.connect(self.exportStream)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(fileSelectButton, 0, 0)
        grid.addWidget(self.fileEdit, 0, 1)

        grid.addWidget(streamNameLabel, 1, 0)
        grid.addWidget(self.streamName, 1, 1)

        grid.addWidget(markersStreamNameLabel, 2, 0)
        grid.addWidget(self.markersStreamName, 2, 1)
        
        grid.addWidget(markersToWriteLabel, 3, 0)
        grid.addWidget(self.markersToWrite, 3, 1)
        
        grid.addWidget(exportButton, 4, 0, 1, 2)
        
        grid.addWidget(logLabel, 5, 0)
        grid.addWidget(self.log, 5, 1, 5, 1)
        self.log.setReadOnly(True)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('XDF export tool')    
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = XDFExporter()
    sys.exit(app.exec_())