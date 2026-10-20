# System Information Script

Name: Pranav Bharadwaj

Enrollment number: **24bcs10006**

The script asks for a name and note, prints the date, host, user, disk usage,
and running processes, then saves the process list to
`system-report/process.log`. It creates the directory and file with `mkdir`
and `touch`, and uses `>` to write the process list.

## Run

From this directory:

```bash
bash system_info.sh
```

## Captured output

This run was made on 9 October 2026 on the homework machine. `df` rows and
processes vary by system.

```text
Name: Pranav Bharadwaj
Note: DevOps homework verification
Date: Fri Oct  9 21:43:56 IST 2026
Host: omarchy
User: pranav

Disk use:
Filesystem        Size  Used Avail Use% Mounted on
/dev/mapper/root  475G   64G  411G  14% /
tmpfs             7.7G     0  7.7G   0% /dev
efivarfs          246K  143K   99K  60% /sys/firmware/efi/efivars
run               7.7G  2.8M  7.7G   1% /run
none              1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
none              1.0M     0  1.0M   0% /run/credentials/systemd-resolved.service
tmpfs             1.6G   56M  1.5G   4% /run/user/1000
tmpfs             7.7G  248M  7.5G   4% /tmp
/dev/mapper/root  475G   64G  411G  14% /var/cache/pacman/pkg
/dev/mapper/root  475G   64G  411G  14% /home
/dev/mapper/root  475G   64G  411G  14% /var/log
/dev/nvme0n1p1    2.0G  268M  1.8G  14% /boot
dev               7.6G     0  7.6G   0% /dev/tty
tmpfs             7.7G     0  7.7G   0% /tmp/codex-daemon-1000
tmpfs             7.7G     0  7.7G   0% /tmp/.git
tmpfs             7.7G     0  7.7G   0% /tmp/.agents
tmpfs             7.7G     0  7.7G   0% /tmp/.codex
tmpfs             7.7G     0  7.7G   0% /home/pranav/Projects/devopsHomework/.agents
tmpfs             7.7G     0  7.7G   0% /home/pranav/Projects/devopsHomework/.codex

Running processes (first 10 lines):
    PID    PPID COMMAND         %CPU %MEM
      1       0 codex           28.5  0.1
      2       1 bash             0.0  0.0
     10       2 bash             0.0  0.0
     18      10 ps               0.0  0.0

Process list saved to: /home/pranav/Projects/devopsHomework/02-shell-scripting/system-information-script/system-report/process.log
```

The saved process file contains PID, parent PID, process name, CPU, and memory
usage, without full command-line arguments that could contain private values.
