import sys
import traceback
import pywinctl as pwc


def exception_hook(exctype, value, tb):
    # https://stackoverflow.com/questions/56991627/how-does-the-sys-excepthook-function-work-with-pyqt5
    traceback_formated = traceback.format_exception(exctype, value, tb)
    traceback_string = "".join(traceback_formated)
    print(traceback_string, file=sys.stderr)

# sys._excepthook = sys.excepthook
sys.excepthook = exception_hook

npw = pwc.getActiveWindow()
print(pwc.getAllScreens())
y = None + 1
print("DONE")
