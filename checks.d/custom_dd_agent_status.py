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
import time

from datadog_checks.base.utils.subprocess_output import get_subprocess_output

# 特別な変数 __version__ の内容は Agent のステータスページに表示されます
__version__ = "2.0.0"


class CustomStatusCheck(AgentCheck):
    """ CustomStatusCheck """
    OK = 0
    ERROR_EXIST = 2
    WARN_EXIST = 1
    EXCEPTION_OCCUR = 3

    DEBUG = True \
        if os.getenv("DEBUG", "") and \
           os.getenv("DEBUG", "").lower() not in ("n", "no", "0") \
        else False

    def get_status(self):
        """ get_status """
        out, err, retcode = get_subprocess_output(
            ["datadog-agent", "status", "-j"],
            self.log,
            raise_on_empty_output=True,
        )
        if err != "":
            print((out, err, retcode))
        if self.DEBUG:
            print(f"DEBUG: status={out}")

        status = json.loads(out)
        return status

    def put_summary(self, agent_status_data):
        """ put_summary """
        summaries = []

        try:
            host = agent_status_data["apmStats"]["config"]["Hostname"]

            checks = agent_status_data["runnerStats"]["Checks"]
            for check_name, check_results in checks.items():
                summary = {}
                summary["status"] = self.OK
                summary["host_name"] = host
                summary["details"] = {}
                for check_id, check_values in check_results.items():
                    for key, value in check_values.items():
                        if key == "TotalErrors":
                            if value > 0:
                                summary["status"] = self.ERROR_EXIST
                                summary["details"]["error"] = check_values["LastError"]
                        elif key == "TotalWarnings":
                            if value > 0:
                                if summary["status"] != self.ERROR_EXIST:
                                    summary["status"] = self.WARN_EXIST
                                summary["details"]["warnings"] = check_values["LastWarnings"]
                    summary["identifier"] = check_id
                summary["name"] = check_name
                summaries.append(summary)
        except KeyError as ex_key:
            summary = {}
            summary["status"] = self.EXCEPTION_OCCUR
            summary["host_name"] = host
            summary["details"] = {}
            summary["details"]["exception"] = repr(ex_key)
            summaries.append(summary)
 
        if self.DEBUG:
            print(f"DEBUG: summary={summaries}")
        return summaries

    def check(self, instance):
        """ check """
        agent_status_data = self.get_status()
        status_summary_data = self.put_summary(agent_status_data)

        for status_summary_datum in status_summary_data:
            self.gauge(
                f"custom_dd_agent_check.{status_summary_datum['name']}.status",
                status_summary_datum["status"],
                tags=[f"identifier:{status_summary_datum['identifier']}"] +
                    self.instance.get('tags', []),
                hostname=status_summary_datum["host_name"]
            )
            time.sleep(5)
