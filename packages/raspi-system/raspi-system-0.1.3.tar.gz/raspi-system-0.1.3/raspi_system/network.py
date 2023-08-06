

import subprocess


def wifi_ssid():
    result = subprocess.check_output(['iwgetid', '-s'])
    result = result.encode().strip()
    return result


if __name__ == '__main__':
    print(wifi_ssid())
