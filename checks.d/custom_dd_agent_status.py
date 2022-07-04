# -*- coding: utf-8 -*-

# refs https://docs.datadoghq.com/ja/developers/write_agent_check/?tabs=agentv6v7
# 次の try/except ブロックを使うと、カスタムチェックがどの Agent バージョンとも互換性を持つようになります
try:
    # 最初に、古いバージョンの Agent から基本クラスのインポートを試みます...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...失敗した場合は、Agent バージョン 6 以降で実行します
    from checks import AgentCheck

import os
import json
import pprint

# 特別な変数 __version__ の内容は Agent のステータスページに表示されます
__version__ = "1.0.0"

class CustomStatusCheck(AgentCheck):
    """ CustomStatusCheck """
    STATUS_FILE = "/etc/datadog-agent/checks.d/dd-agent_status.json"
    SUMMARY_FILE = "/etc/datadog-agent/checks.d/dd-agent_status_summary.json"

    OK = 0
    ERROR_EXIST = 2
    WARN_EXIST = 1
    EXCEPTION_OCCUR = 3

    pp = pprint.PrettyPrinter(indent=2)

    def get_status(self):
        """ get_status """
        os.system("rm -f " + self.STATUS_FILE)
        os.system("datadog-agent status -j > " + self.STATUS_FILE)

    def put_summary(self):
        """ put_summary """
        with open(self.STATUS_FILE, "r", encoding="utf-8") as read_file:
            agent_status_data = json.load(read_file)

        ret = {}
        ret["check_status"] = self.OK
        errors = []
        warnings = []

        try:
            checks = agent_status_data["runnerStats"]["Checks"]
            for check_name, check_results in checks.items():
                for check_id, check_values in check_results.items():
                    for key, value in check_values.items():
                        if key == "TotalErrors":
                            if value > 0:
                                ret["check_status"] = self.ERROR_EXIST
                                errors.append({
                                    check_name + "#" + check_id:check_values["LastError"]
                                })
                        elif key == "TotalWarnings":
                            if value > 0:
                                if ret["check_status"] != self.ERROR_EXIST:
                                    ret["check_status"] = self.WARN_EXIST
                                warnings.append({
                                    check_name + "#" + check_id:check_values["LastWarnings"]
                                })
            ret["errors"] = errors
            ret["warnings"] = warnings
        except KeyError as ex_key:
            ret["check_status"] = self.EXCEPTION_OCCUR
            ret["exceptions"] = repr(ex_key)

        #pp.pprint(ret)

        os.system("rm -f " + self.SUMMARY_FILE)
        with open(self.SUMMARY_FILE, "w", encoding="utf-8") as write_file:
            json.dump(ret, write_file)


    def check(self):
        """ check """
        self.get_status()
        self.put_summary()

        with open(self.SUMMARY_FILE, "r", encoding="utf-8") as read_file:
            status_summary_data = json.load(read_file)

        self.gauge("custom_dd_agent_check.status_value", status_summary_data["check_status"])
