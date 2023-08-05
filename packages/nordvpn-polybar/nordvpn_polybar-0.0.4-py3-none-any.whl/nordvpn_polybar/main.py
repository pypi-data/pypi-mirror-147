import subprocess
import sys


def get_status():
    return subprocess.run(
        ["nordvpn", "status"],
        capture_output=True
    ).stdout.decode('utf-8').strip()


def parse_output(out):
    out = out.replace('-\r', '').replace('\r', '').strip()
    res = {}
    for line in out.split('\n'):
        if ':' in line:
            key, value = line.split(':')
            res[key.strip().lower().replace(' ', '_')] = value.strip()
    return res


if __name__ == "__main__":
    format = sys.argv[1]
    data = parse_output(get_status())

    if data.get('status') == 'Connected':
        sys.stdout.write(" ")  # check icon
        sys.stdout.write(format.format(**data))
    else:
        sys.stdout.write("X Disconnected")  # cross icon

    sys.stdout.flush()
