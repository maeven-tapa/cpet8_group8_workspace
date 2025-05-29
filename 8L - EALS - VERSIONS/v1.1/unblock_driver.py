import os
import sys

def unblock_dll(dll_path):
    """Remove the Zone.Identifier stream that causes DLL blocking"""
    try:
        zone_stream = dll_path + ':Zone.Identifier'
        if os.path.exists(zone_stream):
            os.remove(zone_stream)
    except:
        pass

# Unblock DLLs in the bundle directory
if hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS
    for root, dirs, files in os.walk(bundle_dir):
        for file in files:
            if file.endswith('.dll'):
                dll_path = os.path.join(root, file)
                unblock_dll(dll_path)