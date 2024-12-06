import os
import time
import threading
import subprocess
import multiprocessing as mp

from typing import List, Dict, Any

from viztracer.vizplugin import VizPluginBase


class NvsmiMonitor(VizPluginBase):
    def __init__(self, options: List[str], interval: float, gpu_id: int):
        super().__init__()
        self.action_queue = mp.Queue()
        self.data_queue = mp.Queue()
        self.options = options
        self.interval = interval
        self.gpu_id = gpu_id
        self.recordings = []
        self.pid = os.getpid()

    def support_version(self) -> str:
        return "0.15.6"

    def message(self, m_type, payload) -> Dict[str, Any]:
        if m_type == "event":
            if payload["when"] == "initialize":
                return self.generate_process()
            elif payload["when"] == "post-stop":
                return self.stop_recording()
            elif payload["when"] == "pre-save":
                return self.save_data()
            elif payload["when"] == "pre-start":
                return self.start_recording()
        elif m_type == "command":
            if payload["cmd_type"] == "terminate":
                return self.terminate()
        return {}

    def generate_process(self) -> Dict[str, Any]:
        self.process = mp.Process(
            target=NvsmiMonitorProcess(
                self.action_queue, self.data_queue, self.options, self.interval, self.gpu_id
            ),
            daemon=True,
        )
        self.process.start()
        return {}

    def start_recording(self) -> Dict[str, Any]:
        return self.send_action("start")

    def stop_recording(self) -> Dict[str, Any]:
        self.recordings.append(self.send_action("stop"))
        return {}

    def save_data(self) -> Dict[str, Any]:
        self.recordings.append(self.send_action("get-data"))
        return {"action": "handle_data", "handler": self.append_data}

    def append_data(self, data: Dict[str, List[Any]]) -> None:
        assert isinstance(data, dict)
        for recording in self.recordings:
            for k, data_points in recording.items():
                for data_point in data_points:
                    d = {
                        # required by viztracer
                        "name": k,
                        "ph": "C",
                        "ts": data_point["ts"] * (1e6),
                        "args": data_point["arg"],
                        "pid": self.pid,
                        "tid": self.pid,
                    }
                    data["traceEvents"].append(d)
        self.recordings = []

    def terminate(self) -> Dict[str, Any]:
        self.send_action("terminate")
        self.process.join()
        return {"success": True}

    def send_action(self, message: str) -> Dict[str, Any]:
        if not self.process.is_alive():
            return {}
        self.action_queue.put(message)
        data = self.data_queue.get()
        return data


class NvsmiMonitorProcess:
    def __init__(self, actions, data, options: List[str], interval: float, gpu_id: int):
        self.actions = actions
        self.data_queue = data
        self.interval = interval
        self.options = options
        self.gpu_id = gpu_id

    def read(self) -> None:
        while self.is_running:
            output = self.poller.stdout.readline()
            if output == "" and self.poller.poll() is not None:
                break
            if output:
                self.latest_output = output

    def start(self) -> None:
        self.state = "stopped"
        self.recordings = {}
        self.init_recording()
        self.is_running = True
        metrics = ",".join(self.options)
        lms = int(1000 * self.interval)
        cmd = f"nvidia-smi --query-gpu={metrics} --format=csv,noheader,nounits -i {self.gpu_id} -lms {lms}"
        self.poller = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        self.reader = threading.Thread(target=self.read)
        self.reader.start()
        self.latest_output = ""

    def __call__(self) -> None:
        self.start()
        while True:
            data = {}
            if not self.actions.empty():
                action = self.actions.get()
                if action == "start":
                    self.state = "running"
                    self.recordings["ts"].append(time.monotonic())
                elif action == "stop":
                    self.state = "stopped"
                    # to indicate the end of recording(otherwise the last data point will not be shown)
                    self.record_data()
                    # Every time we get a stop, record the data and send it back
                    # because we may never get the get-data command due to
                    # early process termination
                    data = self.pack_data()
                    self.init_recording()
                elif action == "get-data":
                    if self.state != "stopped":
                        self.state = "stopped"
                        self.record_data()
                    data = self.pack_data()
                    self.init_recording()
                elif action == "terminate":
                    self.terminate()
                    break
                self.data_queue.put(data)
            time.sleep(self.interval)
            if self.state == "running":
                self.record_data()
                self.recordings["ts"].append(time.monotonic())
        self.data_queue.put({})

    def record_data(self) -> None:
        output = self.latest_output.strip()
        if not output:
            return
        vals = output.split(", ")
        for i, k in enumerate(self.options):
            if len(vals) <= i:
                break
            self.recordings[k].append(float(vals[i]))

    def pack_data(self) -> Dict[str, Any]:
        zipped = []
        for i in range(len(self.recordings["ts"])):
            arg: Dict[str, Any] = {}
            for o in self.options:
                if len(self.recordings[o]) <= i:
                    arg = {}
                    break
                arg[o] = self.recordings[o][i]
            if not arg:
                break
            zipped.append({"ts": self.recordings["ts"][i], "arg": arg})
        data = {"NVSMI": zipped}
        return data

    def init_recording(self) -> None:
        self.recordings = {**{o: [] for o in self.options}, "ts": []}

    def terminate(self) -> None:
        self.reading = False
        self.poller.terminate()
