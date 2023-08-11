#!/usr/bin/env python3

import argparse
import websocket
import json
import time

def send_command_to_terminal(ip, port, terminal_id, command):
    ws_url = f"ws://{ip}:{port}/terminals/websocket/{terminal_id}"
    ws = websocket.create_connection(ws_url)
    
    try:
        ws.send(json.dumps(['stdin', command + '\n']))

        # Wait for multiple responses over a short period
        outputs = []
        ws.settimeout(0.5)
        end_time = time.time() + 2  # Wait for 2 seconds to collect data        
        while time.time() < end_time:
            try:
                response = ws.recv()
                data = json.loads(response)
                outputs.append(data)
            except websocket._exceptions.WebSocketTimeoutException:
                # Timeout means no more data to read, so break
                break

        return outputs

    except Exception as e:
        return [str(e)]

    finally:
        ws.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send commands to a remote terminal over WebSocket.")
    parser.add_argument("-i", "--ip", help="IP address of the terminal server", default="10.10.10.10")
    parser.add_argument("-p", "--port", help="Port of the terminal server", default="30000")
    parser.add_argument("-t", "--terminal_id", help="ID of the terminal session", default="1")
    parser.add_argument("-c", "--command", help="Command to execute", required=True)
    
    args = parser.parse_args()

    responses = send_command_to_terminal(args.ip, args.port, args.terminal_id, args.command)
    
    for response in responses:
        print(response)
