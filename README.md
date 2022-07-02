# datadog-agent-status-metricize
Sample script to make `datadog-agent status` a custom metric

## Pre-Requirements
- Sign up https://www.datadoghq.com/   
    - `Free Trial` is available in 14 days.
- Datadog Agent installed.
    - refs https://docs.datadoghq.com/getting_started/agent/

## Get Started

```
cd ${your_appropriate_directory}
git clone https://github.com/sogaoh/datadog-agent-status-metricize
cd datadog-agent-status-metricize

sudo cp -p conf.d/custom_dd-agent_status.yaml /etc/datadog-agent/conf.d/
sudo chown dd-agent:dd-agent /etc/datadog-agent/conf.d/custom_dd-agent_status.yaml

sudo cp -p checks.d/custom_dd-agent_status.py /etc/datadog-agent/checks.d/
sudo chown dd-agent:dd-agent /etc/datadog-agent/checks.d/custom_dd-agent_status.py

sudo systemctl restart datadog-agent
```

### Check configuration(s)

```
sudo -u dd-agent -- datadog-agent configcheck

sudo -u dd-agent -- datadog-agent check custom_dd-agent_status
```


## Note 

### How to `single` script run

```
cd /path/to/datadog-agent-status-metricize
sudo chown -R dd-agent:dd-agent single
cd single

sudo -u dd-agent python3 custom_dd-agent_status.py
```
