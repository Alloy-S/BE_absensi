from datetime import datetime
import argparse

def valid_time(s):
    try:
        return datetime.strptime(s, "%H:%M:%S").time()
    except ValueError:
        raise argparse.ArgumentTypeError("Format waktu harus HH:MM:SS")
    
def valid_time_no_second(s):
    try:
        return datetime.strptime(s, "%H:%M").time()
    except ValueError:
        raise argparse.ArgumentTypeError("Format waktu harus HH:MM")
    
def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("Format tanggal harus YYYY-MM-DD")