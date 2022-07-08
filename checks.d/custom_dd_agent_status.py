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
__version__ = "1.1.0"


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
        ret = {}
        ret["max"] = self.OK
        alerts = []

        try:
            host = agent_status_data["apmStats"]["config"]["Hostname"]
            ret["host_name"] = host

            checks = agent_status_data["runnerStats"]["Checks"]
            for check_name, check_results in checks.items():
                for check_id, check_values in check_results.items():
                    for key, value in check_values.items():
                        if key == "TotalErrors":
                            if value > 0:
                                ret["max"] = self.ERROR_EXIST
                                alerts.append({
                                    "level": self.ERROR_EXIST,
                                    "item": check_name,
                                    "identifier": check_id,
                                    "details": check_values["LastError"]
                                })
                        elif key == "TotalWarnings":
                            if value > 0:
                                if ret["max"] != self.ERROR_EXIST:
                                    ret["max"] = self.WARN_EXIST
                                alerts.append({
                                    "level": self.WARN_EXIST,
                                    "item": check_name,
                                    "identifier": check_id,
                                    "details": check_values["LastWarnings"]
                                })
        except KeyError as ex_key:
            ret["max"] = self.EXCEPTION_OCCUR
            alerts.append({
                "level": self.EXCEPTION_OCCUR,
                "item": "",
                "identifier": "",
                "details": repr(ex_key)
            })
        finally:
            ret["alerts"] = alerts

        if self.DEBUG:
            print(f"DEBUG: summary={ret}")
        return ret

    def check(self, instance):
        """ check """
        agent_status_data = self.get_status()
        status_summary_data = self.put_summary(agent_status_data)

        host = status_summary_data["host_name"]
        self.gauge(
            "custom_dd_agent_check.alerts.max",
            status_summary_data["max"],
            tags=[] + self.instance.get('tags', []),
            hostname=host
        )
        alerts_count = len(status_summary_data["alerts"])
        self.count(
            "custom_dd_agent_check.alerts.count",
            alerts_count,
            tags=[] + self.instance.get('tags', []),
            hostname=host
        )
