#!bin/sh
find /home/pi/git/dank-fridge/files_to_delete -type f -name "dank_fridge_$(date -d "$(date +%Y-%m)-15 last month" '+%Y_%-m')*" -exec rm {} +
find /home/pi/git/dank-fridge/files_to_delete -type f -name "batch_log*" -exec rm {} +

