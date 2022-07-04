# -*- coding: utf-8 -*-

import os
import json
import pprint

STATUS_FILE = "dd-agent_status.json"
SUMMARY_FILE = "dd-agent_status_summary.json"

os.system("rm -f " + STATUS_FILE)
os.system("datadog-agent status -j > " + STATUS_FILE)


OK = 0
ERROR_EXIST = 2
WARN_EXIST = 1
EXCEPTION_OCCUR = -1

pp = pprint.PrettyPrinter(indent=2)

with open(STATUS_FILE, "r", encoding="utf-8") as read_file:
    agent_status_data = json.load(read_file)

ret = {}
ret["check_status"] = OK
errors = []
warnings = []

try:
    checks = agent_status_data["runnerStats"]["Checks"]
    for check_name, check_results in checks.items():
        for check_id, check_values in check_results.items():
            for key, value in check_values.items():
                if key == "TotalErrors":
                    if value > 0:
                        ret["check_status"] = ERROR_EXIST
                        errors.append({check_id:check_values["LastError"]})
                elif key == "TotalWarnings":
                    if value > 0:
                        if ret["check_status"] != ERROR_EXIST:
                            ret["check_status"] = WARN_EXIST
                        warnings.append({check_id:check_values["LastWarnings"]})

    ret["errors"] = errors 
    ret["warnings"] = warnings
except KeyError as e:
    ret["check_status"] = EXCEPTION_OCCUR
    ret["exceptions"] = repr(e)

pp.pprint(ret)

os.system("rm -f " + SUMMARY_FILE)
with open(SUMMARY_FILE, "w", encoding="utf-8") as write_file:
    json.dump(ret, write_file)
