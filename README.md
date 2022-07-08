# datadog-agent-status-metricize
Sample script to make `datadog-agent status` custom metrics

## Pre-Requirements

- Sign up https://www.datadoghq.com/   
    - `Free Trial` is available in 14 days.
- Datadog Agent installed.
    - refs https://docs.datadoghq.com/getting_started/agent/
- Python 3 installed.


## Get Started

```bash
cd ${your_appropriate_directory}
```

```bash
git clone https://github.com/sogaoh/datadog-agent-status-metricize
cd datadog-agent-status-metricize
```

```bash
sudo cp -p conf.d/custom_dd_agent_status.yaml /etc/datadog-agent/conf.d/
sudo chown dd-agent:dd-agent /etc/datadog-agent/conf.d/custom_dd_agent_status.yaml
```

```bash
sudo cp -p checks.d/custom_dd_agent_status.py /etc/datadog-agent/checks.d/
sudo chown dd-agent:dd-agent /etc/datadog-agent/checks.d/custom_dd_agent_status.py
```

```bash
sudo systemctl restart datadog-agent
```

### Check configuration(s)

```bash
sudo -u dd-agent -- datadog-agent configcheck
```

### Run script

```bash
sudo -u dd-agent -- datadog-agent check custom_dd_agent_status
```


## development 

### How to `testing` 

```bash
cd ${/path/to/datadog-agent-status-metricize}/checks.d
```

```bash
python3 -m venv .venv
.venv/bin/pip3 install -r requirements-dev.lock
```

```bash
env PYTHONPATH=. .venv/bin/python3 -m unittest test_custom_dd_agent_status.py
```


#### (DEBUG mode)

```bash
env PYTHONPATH=. DEBUG=1 .venv/bin/python3 -m unittest test_custom_dd_agent_status.py
```