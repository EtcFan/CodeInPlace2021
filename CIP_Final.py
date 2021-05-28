
import csv as csv
import math as math
import pandas as pd 

def main():
    print("")
    file = pick_file()
    while True: 
        if file == "":
            break
        print("")
        print ('Please only use the following date stucture')
        print ('YYYY-MM-DD')
        start_date = start(file)
        end_date = end(file)#ask for users start and end dates and gives back all dates inbetween
        #Needs to check if the date extists. If not, ask again.
        print("") 
        benchmarks = ask_benchmarks() #ask for users benchmarks
        print("") 
        data = look_up(file, start_date, end_date) #looks up the data for the corresponding dates
        variance = calc_var(data, benchmarks)
        growth = calc_gro(data, benchmarks) 
        avg_vol = calc_vol(data)
        #print (data) #tries if dataframe workes
        print("")
        file = pick_file()
    print("")
    print("Thank you for trying this program!")
    print("")
    
def pick_file():
    file_in = input("Enter a file, or press enter to finish: ")
    if file_in == "": 
        return file_in
    else:
        file = file_in + ".csv"
        return file
                
def start(file):
    start_in = input("Enter your start date: ")
    data = pd.read_csv(file, index_col='Date', parse_dates= True)
    while True:
        if start_in in data.index:
            return start_in
        else:
            start_in = input("Enter a different start date: ")

def end(file):
    end_in = input("Enter your end date: ")
    data = pd.read_csv(file, index_col='Date', parse_dates= True)
    while True:
        if end_in in data.index:
            return end_in
        else:
            end_in = input("Enter a different end date: ")

def ask_benchmarks():
    var_max = int( input('Whats your max variance: '))
    var_min = int( input('Whats your min variance: '))
    growth_min = int(input('What minimum growth in % do you want? '))
    benchmarks = [var_max, var_min, growth_min]
    return benchmarks

def look_up(file, start_date, end_date): 
    data = pd.read_csv(file, index_col='Date', parse_dates= True)
    data["Profit"] = (
        1 - ( data["Open"] / data["Close"] ) #calculates each days profit
    )
    x = data.loc[start_date:end_date]
    #selec_data = data.loc[start_date : end_date] #selects data from dates 
    #print(data.loc['2020-09-11' : '2020-09-14'])
    return x

def calc_var(data, benchmarks):

    n = data[["Profit"]].count()
    avg = data[["Profit"]].mean()  #Mittel/average
    val = data["Profit"].tolist() #creates list from profit
    el= 0
    for elem in val:                  #creates 
            el += (elem - avg)**2
    var = math.sqrt(1/n * el) #varianz
    var = round(var, 3) * 100 #to %
    print ('The variance was: ',str(var), "%")
    if benchmarks[0] <= var: 
        print ("It's higher than your maximum variance.")
    elif benchmarks[1] >= var: 
        print ("It's lower than your minimum variance.")
    else: 
        print("It's inside your variance preferences.")

def calc_gro(data, b):
    summe = data["Profit"].sum()
    summe = round(summe, 3)*100 #creates a %
    if summe <= b[2]: 
        print ("There was less growth than expected.") 
    elif summe == b[2]:
        print("Growth was as expected.")
    else: 
        print("There was more growth than expected.")
    print("The real growth was: "+str(summe)+"%")

def calc_vol(data):
    vol = data["Volume"].mean()
    vol = round(vol, 3)
    print("The average volume was: " + str(vol) )

if __name__ == '__main__':
    main()
