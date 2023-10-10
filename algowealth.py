# BMS Algorithm

# A break of structure is simply the process of forming a higher high on an uptrend without first creating a lower low;
# and a lower low on a downtrend without first developing a higher high. In other words, a break of structure is a change in price behavior and signals a shift in market momentum.

# in an uptrend, each successive high should be higher than the prior period’s high.
# In a downtrend, each new low should be lower than the prior period’s low

# The order is important. It’s a break of structure (BOS) only when a higher high is formed on an uptrend without first breaking the low.
# In a downtrend, it is only a break of structure when the price forms a lower low before breaking its most recent high. If any of those
# two scenarios happens, we’re looking at a Market Structure Shift (MSS) or a Change of Character (ChoCh).


import csv

num_candles = 4

with open("/home/voyager/Downloads/Volatility 50 (1s) Index (5 M) (1).csv") as fr:
	data = list(csv.DictReader(fr))

def getTrends():
	uptrends = []
	downtrends = []

	for d in range(0, len(data)):
		# Check for uptrends or downtrends in groups of num_candles
		last = d + (num_candles - 1)
		counter = d

		trends = [] # 1 up, 0 down

		# Nested loops not optimal - Find a better solution
		while counter < last:
			if (float(data[counter + 1]["High"]) - float(data[counter]["High"])) > 0:
			     # and (float(data[counter + 1]["Low"]) - float(data[counter]["Low"])) < 0:
				trends.append(1)
			# elif (float(data[counter + 1]["Low"]) - float(data[counter]["Low"])) < 0 and (float(data[counter + 1]["High"]) - float(data[counter]["High"])) < 0:
			# 	trends.append(1)
			else:
				trends.append(0)

			counter += 1

		if all(trends):
			uptrends.append((d, last))
			# print(f"Uptrend from {data[d]['Time']} to {data[last]['Time']}")

		if not any(trends):
			downtrends.append((d, last))
			# print(f"Downtrend from {data[d]['Time']} to {data[last]['Time']}")

		if (counter + 1) >= len(data):
			break

	return {"up": uptrends, "down": downtrends}


def searchBMS(trends):
	downtrend_bms = []
	uptrend_bms = []

	for u in trends.get("up"):
		ucounter = u[0]

		while ucounter <= u[1]:
			# If LL is created this is not BMS
			if (float(data[ucounter + 1]["Low"]) - float(data[ucounter]["Low"])) < 0:
				break

			ucounter += 1
		
		# Uptrend BMS if the while loop is finished
		uptrend_bms.append((data[u[0]]["Time"], data[u[1]]["Time"]))

	for d in trends.get("down"):
		dcounter = d[0]

		while dcounter <= d[1]:
			# If HH is created this is not BMS
			if (float(data[dcounter + 1]["High"]) - float(data[dcounter]["High"])) > 0:
				break

			dcounter += 1
		
		# Downtrend BMS if the while loop is finished
		downtrend_bms.append((data[d[0]]["Time"], data[d[1]]["Time"]))

	return {"up": uptrend_bms, "down": downtrend_bms}

print(searchBMS(getTrends()))

def searchFVG():
	return