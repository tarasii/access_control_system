[ -e stoprfid ] && rm stoprfid
stdbuf -oL python ./readrfid.py >> log/rfid.log &