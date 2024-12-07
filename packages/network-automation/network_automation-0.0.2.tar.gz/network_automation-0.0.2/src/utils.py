def ip_reachable(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    import platform
    import subprocess

    # Option for the number of packets as a function of
    count = '-n' if platform.system().lower() == 'windows' else '-c'
    wait = '-w' if platform.system().lower() == 'windows' else '-W'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', count, '2', wait, '5', host]

    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0
