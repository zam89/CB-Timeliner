#!/usr/bin/env python
#
# CB Timeliner v0.4 (on 08 Nov 2022)
# Any issue/suggestion, please email to M.Khairulazam@gmail.com
#
# Changelogs
# ----------
# v0.1   (04 Nov 2022): First version of the script.
# v0.2   (05 Nov 2022): Add user input, jq via subprocess & stuff.
# v0.3   (07 Nov 2022): Include more event_type (filemod & regmod)
# v0.4   (08 Nov 2022): Include more event_type (crossproc, modload & netconn)
#
# Instructions
# ------------
# 1. Change url - https://<CB_Console_URL>/api/investigate/v2/orgs/<ORG_Key>/events/ with your CB Console URL
# 2. Run : python CB_Timeliner.py
# 3. Enter your API Key & CB ProcessGUID
# 4. Result will be in 2 format: result_<ProcessGUID>.json & CB_Timeline_<ProcessGUID>.csv

import requests
import json
import subprocess

banner = """
 ██████ ██████      ████████ ██ ███    ███ ███████ ██      ██ ███    ██ ███████ ██████      ██    ██  ██████     ██   ██ 
██      ██   ██        ██    ██ ████  ████ ██      ██      ██ ████   ██ ██      ██   ██     ██    ██ ██  ████    ██   ██ 
██      ██████         ██    ██ ██ ████ ██ █████   ██      ██ ██ ██  ██ █████   ██████      ██    ██ ██ ██ ██    ███████ 
██      ██   ██        ██    ██ ██  ██  ██ ██      ██      ██ ██  ██ ██ ██      ██   ██      ██  ██  ████  ██         ██ 
 ██████ ██████         ██    ██ ██      ██ ███████ ███████ ██ ██   ████ ███████ ██   ██       ████    ██████  ██      ██ 
"""
print(banner)

apikey = input("Enter your API key: ")
processguid = input("Please enter CB ProcessGUID: ")

print("\nProcessing result...")

url = "https://test.conferdeploy.net/api/investigate/v2/orgs/XXXXXXXX/events/" + processguid + "/_search"

payload = json.dumps({
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
    "event_timestamp, event_type, childproc_name, childproc_cmdline, scriptload_name, scriptload_content, fileless_scriptload_cmdline, filemod_name, filemod_action, modload_name, regmod_name, regmod_action, childproc_md5, childproc_sha256, scriptload_md5, scriptload_sha256, fileless_scriptload_sha256, modload_md5, modload_sha256, childproc_pid, process_pid, childproc_username, netconn_action, modload_action, netconn_domain, netconn_local_ipv4, netconn_local_port, netconn_remote_ipv4, netconn_remote_port, netconn_protocol"
  ],
  "sort": [
    {
      "field": "event_timestamp",
      "order": "asc"
    }
  ]
})
headers = {
  'X-Auth-Token': apikey,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

with open("result_" + processguid +".json", "w") as f:
    f.write(response.text)
    f.close()

subprocess.call(["jq -r '[\"event_timestamp\",\"event_type\",\"childproc_name\",\"childproc_cmdline\",\"scriptload_name\",\"scriptload_content\",\"fileless_scriptload_cmdline\",\"filemod_name\",\"filemod_action\",\"modload_name\",\"regmod_name\",\"regmod_action\",\"childproc_md5\",\"childproc_sha256\",\"scriptload_md5\",\"scriptload_sha256\",\"fileless_scriptload_sha256\",\"modload_md5\",\"modload_sha256\",\"childproc_pid\",\"process_pid\",\"childproc_username\",\"netconn_action\",\"modload_action\",\"netconn_domain\",\"netconn_local_ipv4\",\"netconn_local_port\",\"netconn_remote_ipv4\",\"netconn_remote_port\",\"netconn_protocol\"], (.results[] | [.event_timestamp, .event_type, .childproc_name, .childproc_cmdline, .scriptload_name, .scriptload_content, .fileless_scriptload_cmdline, .filemod_name, ([.filemod_action[]?] | join(\"\n\")), .modload_name, .regmod_name, ([.regmod_action[]?] | join(\"\n\")), .childproc_md5, .childproc_sha256, .scriptload_md5, .scriptload_sha256, .fileless_scriptload_sha256, .modload_md5, .modload_sha256, .childproc_pid, .process_pid, .childproc_username, .netconn_action, .modload_action, .netconn_domain, .netconn_local_ipv4, .netconn_local_port, .netconn_remote_ipv4, .netconn_remote_port, .netconn_protocol]) | @csv' result_" + processguid + ".json > CB_Timeline_" + processguid + ".csv"], shell=True)

print("\nDone!")
