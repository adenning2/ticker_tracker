''' -------------------
   | ticker_tracker.py |
   |   Adam  Denning   |
    -------------------
    This program is designed to get a given stock's current price, and output indicators to an arduino.
    https://www.youtube.com/c/ProjectCentral/
'''
import finnhub #Stock Price API
import serial #To send to Arduino
import time #For Timers

#(Notes for future distribution): Enter your personal Finnhub API key here. You can get a free API key at https://finnhub.io/ by creating account.
fhub = finnhub.Client(api_key="KEYHERE")
#(Notes for future distribution): Enter the serial port assigned to your Arduino here.
ser = serial.Serial('COM3', 9600)

#Global Variables
#Price Keys
fcurrent = "c"
fchange = "d"
fpchange = "dp"
#Write Codes
clear = "/"
green = "{"
red = "}"
row1 = "["
row2 = "]"

def write(content):

    ser.write(content.encode())
    
def get_target():

    target_ticker = input("Welcome to the Ticker Tracker program.\nPlease enter your desired stock ticker symbol to begin (SPY): ").upper()

    return target_ticker
    
def determine_indicators():

    #set indicator arrays
    available_indicators = [1, 2, 3, 4, 5]
    target_indicators = []
    choice = 0
    
    while choice != 5:

        print("Please select your desired indicators: (Note, certain indicators may require additional Arduino setup.")

        for indicator in available_indicators:

            if indicator == 1:
                print("1. Current Stock Price (###: XX.XX)")

            elif indicator == 2:
                print("2. Change Since Open (+X.XX)")

            elif indicator == 3:
                print("3. Percent Change Since Open (-X.XX%)")

            elif indicator == 4:
                print("4. Day Change Indicator Light (Green light or Red Light)")

            elif indicator == 5:
                print("5. Finish Program Setup")

        choice = int(input("Choice (1-5): "))

        if choice in available_indicators and choice != 5:

            available_indicators.remove(choice)
            target_indicators.append(choice)

        elif choice != 5:
            print("Not a valid selection.")
    
    #return chosen indicators
    return target_indicators

def get_price(target):

    ticker_price = fhub.quote(target)

    return ticker_price

def send_price(name, p, ind):

    #indicator light
    if 4 in ind:
        #green or red
        if float(p[fchange]) >= 0:
            write(green)
        else:
            write(red)

    #display price
    if 1 in ind:

        write(clear)
        time.sleep(.1) #allows clear time to execute without interfering with writes
        write(row1)
        write(f"{name}: {p[fcurrent]}")
    
    write(row2)

    #change num
    if 2 in ind:
        write(f"{p[fchange]} ")
    
    #change per
    if 3 in ind:
        write(f"{p[fpchange]:.2f}% ")

def main():
    
    #program setup
    ticker = get_target()
    indicators = determine_indicators()

    #loop
    while 1==1:

        #gets ticker info
        price = get_price(ticker)

        #outputs to arduino
        send_price(ticker, price, indicators)

        #refresh buffer
        time.sleep(15)

#run program
if __name__ == "__main__":
    main()