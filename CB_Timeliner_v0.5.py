#!/usr/bin/env python
#
# CB Timeliner v0.5 (on 25 Dec 2022)
# Any issue/suggestion, please email to M.Khairulazam@gmail.com
#
# Changelogs
# ----------
# v0.1   (04 Nov 2022): First version of the script.
# v0.2   (05 Nov 2022): Add user input, jq via subprocess & stuff.
# v0.3   (07 Nov 2022): Include more event_type (filemod & regmod)
# v0.4   (08 Nov 2022): Include more event_type (crossproc, modload & netconn)
# v0.5   (25 Dec 2022): Script reworked by ChatGPT from OpenAI. (No, seriously by AI)
#
# Instructions
# ------------
# 1. Change url - https://<CB_Console_URL>/api/investigate/v2/orgs/<ORG_Key>/events/ with your CB Console URL
# 2. Run : python CB_Timeliner.py
# 3. Enter your API Key & CB ProcessGUID
# 4. Result will be in 2 format: result_<ProcessGUID>.json & CB_Timeline_<ProcessGUID>.csv

import requests
import json
import csv

banner = """
 ██████ ██████      ████████ ██ ███    ███ ███████ ██      ██ ███    ██ ███████ ██████      ██    ██  ██████     ███████ 
██      ██   ██        ██    ██ ████  ████ ██      ██      ██ ████   ██ ██      ██   ██     ██    ██ ██  ████    ██      
██      ██████         ██    ██ ██ ████ ██ █████   ██      ██ ██ ██  ██ █████   ██████      ██    ██ ██ ██ ██    ███████ 
██      ██   ██        ██    ██ ██  ██  ██ ██      ██      ██ ██  ██ ██ ██      ██   ██      ██  ██  ████  ██         ██ 
 ██████ ██████         ██    ██ ██      ██ ███████ ███████ ██ ██   ████ ███████ ██   ██       ████    ██████  ██ ███████ 
"""
print(banner)

# Get CB API key & ProcessGUID to process
api_key = input("Enter your API key: ")
process_guid = input("Please enter CB ProcessGUID: ")

print("\nProcessing result...")

# Set your CB URL here. Don't forget to set your ORGS_KEY
api_url = "https://test.conferdeploy.net/api/investigate/v2/orgs/ORGS_KEY/events/" + process_guid + "/_search"

# Define your query criteria
query_criteria = json.dumps({
  "criteria": {
    "event_type": [
      "scriptload",
      "childproc",
      "fileless_scriptload",
      "filemod",
      "regmod",
      "crossproc",
      "modload",
      "netconn"
    ]
  },
  "fields": [
    "event_timestamp, event_type, childproc_name, childproc_cmdline, scriptload_name, scriptload_content, fileless_scriptload_cmdline, filemod_name, filemod_action, modload_name, regmod_name, regmod_action, childproc_md5, childproc_sha256, scriptload_md5, scriptload_sha256, fileless_scriptload_sha256, modload_md5, modload_sha256, crossproc_name, crossproc_api, crossproc_sha256, childproc_pid, process_pid, childproc_username, netconn_action, modload_action, netconn_domain, netconn_local_ipv4, netconn_local_port, netconn_remote_ipv4, netconn_remote_port, netconn_protocol"
  ],
  "sort": [
    {
      "field": "event_timestamp",
      "order": "asc"
    }
  ]
})

# Execute the query
headers = {
  'X-Auth-Token': api_key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", api_url, headers=headers, data=query_criteria)

# Check the response status code to make sure the query was successful
if response.status_code == 200:
    # Parse the list of events from the response
    events = response.json()["results"]

    # Open a CSV file for writing
    with open("result_" + process_guid +".csv", "w", newline="") as csvfile:
        # Create a CSV writer object with the desired field names
        writer = csv.DictWriter(csvfile, fieldnames=["event_timestamp", "event_type", "childproc_name", "childproc_cmdline", "scriptload_name", "scriptload_content", "fileless_scriptload_cmdline", "filemod_name", "filemod_action", "modload_name", "regmod_name", "regmod_action", "childproc_md5", "childproc_sha256", "scriptload_md5", "scriptload_sha256", "fileless_scriptload_sha256", "modload_md5", "modload_sha256", "crossproc_name", "crossproc_api", "crossproc_sha256", "childproc_pid", "process_pid", "childproc_username", "netconn_action", "modload_action", "netconn_domain", "netconn_local_ipv4", "netconn_local_port", "netconn_remote_ipv4", "netconn_remote_port", "netconn_protocol"])

        # Write the header row
        writer.writeheader()

        # Iterate through the list of events
        for event in events:
            # Write the event data to the CSV file, mapping the API response keys to the desired field names
            writer.writerow(event)
    
    print("\nDone!")
else:
    print("Error executing query")
