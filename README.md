CB Timeliner
===
This script is use to export related CB events into CSV file that related to specific ProcessGUID that currently investigating. It also can be use to quickly build timeline of event that been observed/detected by Carbon Black EDR.

Dependencies
===
<li>Python3+</li>
<br/>
Required Python modules (via Pip):
<li>requests</li>
<li>json</li>
<li>csv</li>

How to Run
===
1. Change url - <b>https://<CB_Console_URL>/api/investigate/v2/orgs/<ORG_Key>/events/</b> with your CB Console URL
  * Make sure you put your ORG_KEY aswell
2. Run : 
```
python CB_Timeliner_v0.5.py
```
3. Enter your CB API Key & CB ProcessGUID
4. Result will be same on script location - **result_< ProcessGUID >.csv**

Screenshot
===
![CB Timeliner](/screenshot/CB_Timeliner_screenshot.png)

Output example:
![CB Timeliner](/screenshot/CB_Timeliner_screenshot1.png)

<br/>
How to get ProcessGUID in Carbon Black Cloud Console:

1. Go to "Take Action" -> under "More Actions", select "Share process tree":
<br/>![CB ProcessGUID1](/screenshot/CB_Timeliner_screenshot22.png)

2. ProcessGUID of interest is highlighted in blue as example below:
<br/>![CB ProcessGUID2](/screenshot/CB_Timeliner_screenshot3.png)

Changelogs
===
- v0.1   (04 Nov 2022): First version of the script.
- v0.2   (05 Nov 2022): Add user input, jq via subprocess & stuff.
- v0.3   (07 Nov 2022): Include more event_type (filemod & regmod)
- v0.4   (08 Nov 2022): Include more event_type (crossproc, modload & netconn)
- v0.5   (25 Dec 2022): Script reworked by ChatGPT from OpenAI. (No, seriously by AI)

License
===
MIT License. Copyright (c) 2022 Mohd Khairulazam. See [License](https://github.com/zam89/CB-Timeliner/blob/main/LICENSE).
