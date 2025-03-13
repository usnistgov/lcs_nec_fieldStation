source /etc/environment

while true
do
	python3 /home/meso3/sht30/readSHT30.py $SHT_SNAME $SHT_ID $SHT_LOC
	sleep 3
done
