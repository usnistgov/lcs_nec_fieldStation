# Script to create driving json for env chamber
cd /home/meso3/co2_enrichment						# change current directory

CH_CONC=$1
CH_THRESHOLD=$2

json="{}"								# create empty json
json=$(echo $json | jq --argjson t "$CH_CONC" '.concentration |= $t')	# add concentration
json=$(echo $json | jq --argjson t "$CH_THRESHOLD" '.threshold |= $t')	# add threshold

echo $json > req_conc.json						# output json, overwriting old file
