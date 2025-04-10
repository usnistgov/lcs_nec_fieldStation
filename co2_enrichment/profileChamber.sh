echo "Opening valve for 1 second"
python3 /home/meso3/valve_control/open_valve.py 1
echo "Waiting 3 minutes for chamber to equalize"
sleep 3m

echo "Opening valve for 2 seconds"
python3 /home/meso3/valve_control/open_valve.py 2
echo "Waiting 3 minutes for chamber to equalize"
sleep 3m

echo "Opening valve for 3 seconds"
python3 /home/meso3/valve_control/open_valve.py 3
echo "Waiting 3 minutes for chamber to equalize"
sleep 3m

echo "Opening valve for 4 seconds"
python3 /home/meso3/valve_control/open_valve.py 4
echo "Waiting 3 minutes for chamber to equalize"
sleep 3m

echo "Opening valve for 5 seconds"
python3 /home/meso3/valve_control/open_valve.py 5
echo "Waiting 3 minutes for chamber to equalize"
sleep 3m

echo "Opening valve for 10 seconds"
python3 /home/meso3/valve_control/open_valve.py 10
echo "Waiting 3 minutes for chamber to equalize"
sleep 3m

echo "Environmental chamber profiling complete"
