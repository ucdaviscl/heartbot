import json
import sys
import csv
import re

log_file_path = sys.argv[1]
csv_file_path = sys.argv[2]

with open(log_file_path, "r") as file:
    json_data = file.read()

logs = json.loads(json_data)

data = []

for log_entry in logs:
    if 'jsonPayload' in log_entry:
        json_payload = log_entry['jsonPayload']
        
        if 'queryInput' in json_payload and 'text' in json_payload['queryInput']:
            query_input_text = json_payload['queryInput']['text']['text']
            id = log_entry['labels']['session_id']
            timestamp = log_entry['timestamp']
            date = timestamp[:len('yyyy-mm-dd')]
            time = timestamp[len('yyyy-mm-ddT'):len('yyyy-mm-ddThh:mm:ss')]
            print(f"{id} {date} {time} USER {query_input_text}")
            data.append([id, date, time, 'USER    ', query_input_text])
        
        # Check for "responseMessages" and print text from each item
        if 'queryResult' in json_payload and 'responseMessages' in json_payload['queryResult']:
            id = json_payload['queryResult']['diagnosticInfo']['Session Id']
            timestamp = log_entry['timestamp']
            date = timestamp[:len('yyyy-mm-dd')]
            time = timestamp[len('yyyy-mm-ddT'):len('yyyy-mm-ddThh:mm:ss')]
            for response_message in json_payload['queryResult']['responseMessages']:
                if "text" in response_message:
                    for response_text in response_message['text']['text']:
                        print(f"{date} {time} {id} HEARTBOT {response_text}")
                        data.append([id, date, time, 'HEARTBOT', response_text])

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)
