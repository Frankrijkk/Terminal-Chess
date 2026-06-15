import os
import sys
if __name__ == "__main__":
    if len(sys.argv) >1:
        port = sys.argv[1]
    else:
        port = 8080
    os.system(f"uvicorn terminal_chess_server:app --host 0.0.0.0 --port {port}")