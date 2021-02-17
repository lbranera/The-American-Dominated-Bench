import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_justices_precw(data):
	justices = []
	data = pd.read_csv('justices.csv')
	for row in data.itertuples():
	if(row[5]!="Incumbent"):
		american_period_end = datetime(1936, 2, 1)
		justice_start = datetime.strptime(row[4], '%B %d, %Y')

		if(justice_start<=american_period_end):
			justices.append(row)

	return justices

def in_justices_data(roll_no, justices):
	for justice in justices:
		if(roll_no == justice["roll_no"]):
			return True

	return False

def add_term(roll_no, start, end, justices):
	for i in range(len(justices)):
		if(roll_no == justices[i]["roll_no"]):
			justices[i]["term2"] = {"start":start, "end": end}
			return justices

def justices_data(data):
	justices = []
	for i in range(len(data)):
		temp = {"roll_no": data[i][1], "name": data[i][2], "nationality": data[i][3], "term1": {"start":data[i][4], "end": data[i][5]}}
		if ( in_justices_data(data[i][1], justices) ):
			justices = add_term(data[i][1], data[i][4], data[i][5], justices)
		else:
			justices.append(temp)

	return justices

def get_dates(justices):
	dates = []
	for justice in justices:
		start = datetime.strptime(justice["term1"]["start"], '%B %d, %Y')
		end = datetime.strptime(justice["term1"]["end"], '%B %d, %Y') + timedelta(days=1)
		dates.append(start)
		dates.append(end)
		if("term2" in justice):
			start = datetime.strptime(justice["term2"]["start"], '%B %d, %Y')
			end = datetime.strptime(justice["term2"]["end"], '%B %d, %Y')  + timedelta(days=1)
			dates.append(start)
			dates.append(end)

	return dates

def get_justices_by_date(date, justices):
	bench = []
	for justice in justices:
		justice_start = datetime.strptime(justice["term1"]["start"], '%B %d, %Y')
		justice_end = datetime.strptime(justice["term1"]["end"], '%B %d, %Y')
		if( justice_start<=date and date<=justice_end ):
			bench.append(justice)
		elif("term2" in justice):
			justice_start = datetime.strptime(justice["term2"]["start"], '%B %d, %Y')
			justice_end = datetime.strptime(justice["term2"]["end"], '%B %d, %Y')
			if( justice_start<=date and date<=justice_end ):
				bench.append(justice)

	return bench

def count_filipinos(bench):
	filipinos = 0
	for justice in bench:
		if(justice["nationality"]=="Filipino"):
			filipinos+=1

	return filipinos


justices = get_justices_precw() #SC Justices who served during the pre-commonwealth period.

print("FIRST PART:")
justices = justices_data(justices)

americans = filipinos = 0
for justice in justices:
	print(justice)
	if(justice["nationality"]=="Filipino"):
		filipinos+=1
	else:
		americans+=1

print("No. of Filipinos:",filipinos)
print("No. of Americans:",americans)


print("SECOND PART:")
dates = get_dates(justices)
dates = list(set(dates))
dates.sort()
dates = dates[:len(dates)-6]
benches = []

for date in dates:
	new_bench = get_justices_by_date(date, justices)
	benches.append(new_bench)

str_dates = [date.strftime('%B %d, %Y') for date in dates]

filipinos = []
americans = []
for i in range(len(benches)):
	print("Bench #"+str(i), str_dates[i])
	for justice in benches[i]:
		print("\t",justice)

	cf = count_filipinos(benches[i])
	ca = len(benches[i]) - cf
	filipinos.append(cf)
	americans.append(ca)
	print("\t No. of Filipinos:", cf)
	print("\t No. of Americans:", ca)


plt.title('Philippine Supreme Court Bench from June 15, 1901 to February 2, 1936 by Nationality')
plt.plot(str_dates, filipinos, marker='o', label = "Filipinos")
plt.plot(str_dates, americans, marker='o', label = "Americans")
plt.xlabel('Dates')
plt.ylabel('Cardinality')
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()