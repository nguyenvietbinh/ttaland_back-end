#!/usr/bin/env python3
import boto3
import time
import json
from datetime import datetime, timedelta

def tail_lambda_logs(function_name, duration_minutes=5):
    """
    Tail logs từ Lambda function
    """
    cloudwatch = boto3.client('logs')
    
    # Tính thời gian bắt đầu
    start_time = int((datetime.now() - timedelta(minutes=duration_minutes)).timestamp() * 1000)
    
    print(f"Tailing logs for {function_name}...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Lấy danh sách log streams
            streams_response = cloudwatch.describe_log_streams(
                logGroupName=f"/aws/lambda/{function_name}",
                orderBy='LastEventTime',
                descending=True
            )
            
            if not streams_response['logStreams']:
                print("No log streams found")
                time.sleep(5)
                continue
            
            # Lấy events từ stream mới nhất
            for stream in streams_response['logStreams'][:3]:  # 3 streams gần nhất
                events_response = cloudwatch.get_log_events(
                    logGroupName=f"/aws/lambda/{function_name}",
                    logStreamName=stream['logStreamName'],
                    startTime=start_time
                )
                
                for event in events_response['events']:
                    timestamp = datetime.fromtimestamp(event['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] {event['message']}")
            
            time.sleep(5)  # Chờ 5 giây trước khi check lại
            
    except KeyboardInterrupt:
        print("\nStopped tailing logs")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python tail_lambda_logs.py <function-name>")
        sys.exit(1)
    
    function_name = sys.argv[1]
    tail_lambda_logs(function_name)