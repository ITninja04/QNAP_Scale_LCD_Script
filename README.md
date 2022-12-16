# Truenas Scale - QNAP LCD Script

## Installation

> In this example I created a 'config' share and am executing my script from there.

```bash
    ssh root@<<TRUENAS_SCALE_IP/HOSTNAME>>
    git clone --recurse-submodules https://github.com/ITninja04/QNAP_Scale_LCD_Script.git /mnt/Main/config/qnap_scripts
    cd /mnt/Main/config/qnap_scripts
```

I've included the qnapdisplay git repo as a sub-module since I didn't want to install pip. Let's go ahead and isstall the QNAP Display module.

```bash
    python /mnt/Main/config/qnap_scripts/script_root/qnapdisplay/setup.py install
```
