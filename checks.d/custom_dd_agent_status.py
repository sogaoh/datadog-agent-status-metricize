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
__version__ = "1.3.1"


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
            host = agent_status_data["hostinfo"]["hostname"]

            loader_status_data = agent_status_data["checkSchedulerStats"]["LoaderErrors"]
            if len(loader_status_data) > 0:
                summary = {}
                summary["name"] = "LoaderErrors"
                summary["identifier"] = ""
                summary["status"] = self.WARN_EXIST
                summary["details"] = {}
                summary["details"]["loaderErrors"] = loader_status_data
                summaries.append(summary)
            else:
                summary = {}
                summary["name"] = "LoaderErrors"
                summary["identifier"] = ""
                summary["status"] = self.OK
                summary["details"] = {}
                summaries.append(summary)

            checks = agent_status_data["runnerStats"]["Checks"]
            for check_name, check_results in checks.items():
                summary = {}
                summary["status"] = self.OK
                summary["details"] = {}
                for check_id, check_values in check_results.items():
                    for key, value in check_values.items():
                        if key == "TotalErrors":
                            if value > 0:
                                summary["status"] = self.ERROR_EXIST
                                summary["details"]["error"] = check_values["LastError"]
                        if key == "TotalWarnings":
                            if value > 0:
                                if summary["status"] != self.ERROR_EXIST:
                                    summary["status"] = self.WARN_EXIST
                                summary["details"]["warnings"] = check_values["LastWarnings"]
                    summary["identifier"] = check_id
                summary["name"] = check_name
                summaries.append(summary)

            summary = {}
            summary["name"] = "KeyError"
            summary["identifier"] = ""
            summary["status"] = self.OK
            summary["details"] = {}
            summaries.append(summary)

        except KeyError as ex_key:
            summary = {}
            summary["name"] = "KeyError"
            summary["identifier"] = ""
            summary["status"] = self.EXCEPTION_OCCUR
            summary["details"] = {}
            summary["details"]["exception"] = repr(ex_key)
            summaries.append(summary)

        if self.DEBUG:
            print(f"DEBUG: summaries={summaries}")
        return {"summaries": summaries, "host_name": host}

    def check(self, instance):
        """ check """
        agent_status_data = self.get_status()
        status_summary_data = self.put_summary(agent_status_data)

        host = status_summary_data["host_name"]
        for status_summary_datum in status_summary_data["summaries"]:
            self.gauge(
                "custom_dd_agent_check.health",
                status_summary_datum["status"],
                tags=[
                        f"plugin_name:{status_summary_datum['name']}",
                    ] + self.instance.get('tags', []),
                hostname=host
            )
            #time.sleep(2)
