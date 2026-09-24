# Log checker

Simple Python script to inspect system logs.

Usage examples:

Show last 200 lines from default system log:

```bash
python3 python_code/check_logs.py
```

Show last 100 lines and filter for the word "fail":

```bash
python3 python_code/check_logs.py --lines 100 --filter fail
```

Follow new lines and show only errors:

```bash
sudo python3 python_code/check_logs.py --follow --level error
```

Use a custom log file:

```bash
python3 python_code/check_logs.py --file /var/log/nginx/error.log --lines 50
```

Notes:

- Reading system logs may require elevated privileges (`sudo`).
- This is a simple utility for convenience and demos; for production use prefer robust log tools.
