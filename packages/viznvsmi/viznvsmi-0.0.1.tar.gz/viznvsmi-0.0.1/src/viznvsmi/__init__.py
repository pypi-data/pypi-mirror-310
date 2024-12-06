import subprocess
import argparse

from .monitor import NvsmiMonitor

__version__ = "0.0.1"


def _add_options(parser: argparse.ArgumentParser) -> None:
    result = subprocess.run(["nvidia-smi", "--help-query-gpu"], capture_output=True, text=True)
    out, err = result.stdout, result.stderr
    if err:
        raise RuntimeError(err)
    for metric_line in out.split("\n\n"):
        mtrc, *desc = metric_line.split("\n", 2)
        if mtrc.startswith("\""):
            opts, help = tuple(m[1:-1] for m in mtrc.split() if m and m.startswith("\"")), "\n".join(desc)
            if opts:
                parser.add_argument(*("--" + o for o in opts), dest=opts[0], help=help, action="store_true")


def get_vizplugin(arg: str) -> NvsmiMonitor:
    parser = argparse.ArgumentParser(prog="viznvsmi")
    parser.add_argument("-i", help="GPU id")
    parser.add_argument("-f", help="The frequency of sampling", default=50)
    _add_options(parser)
    inputs = parser.parse_args(arg.split()[1:])
    options = [k for k, v in vars(inputs).items() if v and k not in "fi"]
    interval = 1 / float(inputs.f)
    gpu_id = int(inputs.i)
    return NvsmiMonitor(options, interval, gpu_id)
