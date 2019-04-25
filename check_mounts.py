def send_alert():

    # code for sending alert

    return

if __name__ == "__main__":

    fstab = {}
    mtab = {}

    filename = '/etc/fstab'
    with open(filename) as f:
        for line in f:
            if not line.startswith('#') and not "swap" in line:
                fstab[(line.split()[1])] = (line.split()[3])

    filename = '/etc/mtab'
    with open(filename) as f:
        for line in f:
            if not line.startswith('#') and not "swap" in line:
                mount = (line.split()[1])
                if mount in fstab.keys():
                    mtab[mount] = (line.split()[3].split(',')[0])

    for kf, vf in fstab.items():
        for km, vm in mtab.items():
            if not ('ro,' in vf or ',ro' in vf or ',ro,' in vf) and vm == 'ro':
                send_alert()
