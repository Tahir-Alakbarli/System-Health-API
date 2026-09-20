import os
import socket
import time

import psutil
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        application="System Health API",
        endpoints=["/health", "/system", "/version"],
    )


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/system")
def system_information():
    return jsonify(
        hostname=socket.gethostname(),
        cpu_usage=psutil.cpu_percent(interval=0.1),
        memory_usage=psutil.virtual_memory().percent,
        disk_usage=psutil.disk_usage("/").percent,
        uptime_seconds=int(time.time() - psutil.boot_time()),
    )


@app.get("/version")
def version():
    return jsonify(version=os.getenv("APP_VERSION", "development"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
