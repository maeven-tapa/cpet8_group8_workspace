import win32com.client
import pythoncom

class FingerprintEventHandler:
    def OnCapture(self, *args):
        print("Fingerprint captured successfully!")

class FingerprintDemo:
    def __init__(self):
        print("Initializing ZKFinger SDK...")
        self.zkfinger = win32com.client.Dispatch("ZKFPEngXControl.ZKFPEngX")
        self.event_handler = win32com.client.WithEvents(self.zkfinger, FingerprintEventHandler)

        if self.zkfinger.InitEngine() == 0:
            print("Fingerprint engine initialized successfully.")
            device_count = self.zkfinger.SensorCount
            print(f"Number of connected fingerprint sensors: {device_count}")
        else:
            print("Failed to initialize fingerprint engine.")
            return

    def capture_fingerprint(self):
        print("Capturing fingerprint image...")
        self.zkfinger.BeginCapture()
        print("Waiting for fingerprint capture event...")
        while True:
            pythoncom.PumpWaitingMessages()

    def close_engine(self):
        print("Fingerprint engine closed.")
        self.zkfinger.EndEngine()

if __name__ == "__main__":
    demo = FingerprintDemo()
    try:
        demo.capture_fingerprint()
    except KeyboardInterrupt:
        demo.close_engine()
