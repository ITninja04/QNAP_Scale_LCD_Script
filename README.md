# Truenas Scale - QNAP LCD Script

## Installation

> In this example I created a 'config' share and am I executing my script from there.

```bash
ssh root@<<TRUENAS_SCALE_IP/HOSTNAME>>
```

```bash
git clone https://github.com/ITninja04/QNAP_Scale_LCD_Script.git /mnt/Main/config/qnap_scripts
```

```bash
cd /mnt/Main/config/qnap_scripts
```

```bash
# Install dependencies (py-serial for example)
python setup.py install
```

```bash
chmod a+x launcher.sh && chmod a+x start_daemon.sh
```

```bash
./start_daemon.sh
```
