BRIEF INSTRUCTIONS ON HOW CO@ ENRICHMENT WORKS

# Establishing the CO2 enrichment slope (Chamber-dependent)
- Plumb Picarro up to the environmental chamber
- Plumb the enrichment schema to the chamber. Set a constant flow rate with a needle valve (anywhere between 60-100 mL/min)
- Turn on the chamber, let CO2 concentrations stabilize inside the chamber
- Once conditions stabalize, open the valve for 1/2/3/5/10 seconds. Let the chamber stabalize each time the valve is opened
- Calculate the CO2 delta related to time opened. Complete a linear fit of the data, and rearrange the slope equation so you can get time from the requested delta

# Plumbing CO2 enrichment to the chamber
- Using short lines - keeping the pure CO2 as close as possible to the chamber
- Use 1/8" lines to feed directly into the chamber. Having a smaller diameter means less air is needed to "purge" the conditioned air

# Description of how the software/system works:
- Desired concentration and tolerance lives in a JSON file
- Program does the following:
	1) Grabs the most recent CO2 packet from the Picarro (MUST BE RUN BY THE SAME SYSTEM)
	2) Software compares desired concentrations between averaged Picarro measurement and requested concentration
	3) Software uses pre-determined slope to calculate the delta and required time to spike the chamber to the desired concentration
	4) Software opens/closes the valve for the determined time
	5) Software exports a JSON file with enrichment information (concentration increase, etc)
	6) Output gets piped to the MQTT publishing service

# Operating the enrichment system
