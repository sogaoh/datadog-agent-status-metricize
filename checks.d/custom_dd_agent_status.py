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
__version__ = "1.5.0"


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
                summary["identifier"] = "LoaderErrors"
                summary["status"] = self.WARN_EXIST
                summary["details"] = {}
                summary["details"]["loaderErrors"] = loader_status_data
                summaries.append(summary)
            else:
                summary = {}
                summary["name"] = "LoaderErrors"
                summary["identifier"] = "LoaderErrors"
                summary["status"] = self.OK
                summary["details"] = {}
                summaries.append(summary)

            checks = agent_status_data["runnerStats"]["Checks"]
            for check_name, check_results in checks.items():
                summary = {}
                summary["status"] = self.OK
                summary["details"] = {}
                try:
                    for check_id, check_values in check_results.items():
                        #if self.DEBUG:
                        #    print(f"DEBUG: check_values={check_values}")
                        if "LastError" not in check_values:
                            raise KeyError("LastError")
                        if "LastWarnings" not in check_values:
                            raise KeyError("LastWarnings")
                        for key, value in check_values.items():
                            if key == "LastError":
                                if value != "":
                                    summary["status"] = self.ERROR_EXIST
                                    summary["details"]["error"] = check_values["LastError"]
                            if key == "LastWarnings":
                                if len(value) > 0:
                                    if summary["status"] != self.ERROR_EXIST:
                                        summary["status"] = self.WARN_EXIST
                                    summary["details"]["warnings"] = check_values["LastWarnings"]
                        summary["identifier"] = check_id
                    summary["name"] = check_name
                    summaries.append(summary)
                except KeyError as ex_key:
                    summary = {}
                    summary["name"] = "custom_dd_agent_status"
                    summary["identifier"] = f"KeyError on: {check_name}"
                    summary["status"] = self.EXCEPTION_OCCUR
                    summary["details"] = {}
                    summary["details"]["exception"] = repr(ex_key)
                    summaries.append(summary)
                finally:
                    pass

        except Exception as ex:
            summary = {}
            summary["name"] = "custom_dd_agent_status"
            summary["identifier"] = "Unexpected Response"
            summary["status"] = self.EXCEPTION_OCCUR
            summary["details"] = {}
            summary["details"]["exception"] = repr(ex)
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
                        f"identifier:{status_summary_datum['identifier']}",
                    ] + self.instance.get('tags', []),
                hostname=host
            )
            #time.sleep(2)
