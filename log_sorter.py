class LogSorter:
    def __init__(self):
        self.line = ""
        self.widget = None
        
    def setWidgetLog(self, widget):
        self.widget = widget
        
    def addLog(self, text):
        self.widget.insertPlainText(text + "\n")