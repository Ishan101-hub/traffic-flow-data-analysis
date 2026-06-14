#Author: Ishan Ernaga Adithya Udawatte
#Date: 12/06/2024
#Student ID: 20232686/ 2120028

import csv
import datetime
from datetime import datetime, date

# Task A: Input Validation
def validate_date_input():
    
    #Taking date from user
    while True:
        try:
            day=int(input("Please enter the day of the survey in the format DD: "))
            if day<1 or day>31:
                print("Out of range - values must be in the range 1 and 31.")
                print()
                continue
        except ValueError:
            print(f"Integer required!!!")
            print()
            continue
        except Exception as e:
            print(f"An error occured: {e}")
            print()
            continue
        else:
            print("You have successfully entered the day")
            print()
            break

    #Taking month from user
    while True:
        try:
            month=int(input("Please enter the month of the survey in the format MM: "))
            if 1>month or month>12:
                print("Out of range - values must be in the range 1 to 12.")
                print()
                continue
        except ValueError:
            print(f"Integer required!!!")
            print()
            continue
        except Exception as e:
            print(f"An error occured: {e}")
            print()
            continue
        else:
            print("You have successfully entered the month")
            print()
            break

    #Taking year from user
    while True:
        try:
            year=int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000>year or year>2024:
                print("Out of range - values must range from 2000 and 2024")
                print()
                continue
            date(year, month, day)
        except ValueError as v:
            if('invalid literal for int() with base 10:' in str(v)):
                print(f"Integer required!!!")
                print()
            if('day is out of range for month' in str(v)):
                print('The day is out of range for the month!!, Please renter year.')
                print()
            continue
        except Exception as e:
            print(f"An error occured: {e}")
            print()
            continue
        else:
            print("You have successfully entered the year")
            print()
            break
                    
    return day, month, year

#A: converting user input in to a file name
def process_file_name(day, month, year):
    if day <10:
        day=f"0{day}"
    if month <10:
        month=f"0{month}"
    file_name = f"traffic_data{day}{month}{year}.csv"
    return file_name
#A: asking user if another file needs to be loaded
def validate_continue_input():
   
    while True:
        load_dataset=input("Do you want to load a another dataset?(Y/N): ")

        match load_dataset.upper().strip(): #removing the additional space and getting  user input as uppecase
            case 'Y' | 'YES':
                return 'Y'
            case 'N' | 'NO':
                print("Exiting program...")
                print("Good bye!!")
                return 'N'
            case _:
                print("Invalid input. Please enter Y or N.")
                continue


# Task B: Processed Outcomes
def process_csv_data(file_name):
    
    #initializing the variables as global variables
    global outcomes, total_vehicle_count, total_truck_count, electric_vehicle_count, two_wheeled_vehicle_count
    global north_buss_count_leaving_elm, vehicle_count_going_straight, truck_percentage
    global total_bicycle_count, bicycle_count_per_hour, over_speed_vehicle_count
    global total_vehicle_count_through_elm, total_vehicle_count_through_han
    global scooter_count, scooter_percentage, peak_hour_vehicle_count, peak_hour, peak_hour2, total_rain_count


    # Reseting variables before processing each file
    outcomes = []
    total_vehicle_count = 0
    total_truck_count = 0
    electric_vehicle_count = 0
    two_wheeled_vehicle_count = 0
    north_buss_count_leaving_elm = 0
    vehicle_count_going_straight = 0
    truck_percentage = 0
    total_bicycle_count = 0
    bicycle_count_per_hour = 0
    over_speed_vehicle_count = 0
    total_vehicle_count_through_elm = 0
    total_vehicle_count_through_han = 0
    scooter_count = 0
    scooter_percentage = 0
    hour_counts = [0] * 24
    peak_hour_vehicle_count = 0
    peak_hour = 0
    peak_hour2 = 0
    rain_counts= []
    rain_set={}
    total_rain_count = 0

    try:
        # Reading the CSV file in the local device
        with open(f"{file_name}", "r") as file:
            csv_content = csv.DictReader(file)
            for row in csv_content:
                total_vehicle_count += 1 #outcome 2
                vehicle_type = row.get("VehicleType", "").lower()
                vehicle_mode = row.get("elctricHybrid", "").lower()
                junction_name = row.get("JunctionName", "").lower()
                travel_direction_out = row.get("travel_Direction_out", "").lower()
                travel_direction_in = row.get("travel_Direction_in", "").lower()
                speed_limit = int(row.get("JunctionSpeedLimit", 0))
                speed = int(row.get("VehicleSpeed", 0))
                time_str = row.get("timeOfDay")  # Get the "timeOfDay" column
                weather = row.get("Weather_Conditions", "").lower()
                
                #outcome 3
                if vehicle_type == "truck":
                    total_truck_count += 1
                #outcome 4    
                if vehicle_mode == 'true':
                    electric_vehicle_count += 1
                #outcome 5
                if vehicle_type in ['bicycle', 'motorcycle', 'scooter']:
                    two_wheeled_vehicle_count += 1
                #outcome 6
                if junction_name == 'elm avenue/rabbit road' and travel_direction_out == 'n' and vehicle_type == 'buss':
                    north_buss_count_leaving_elm += 1
                #outcome 7
                if travel_direction_in == travel_direction_out:
                    vehicle_count_going_straight += 1
                #outcome 9 
                if vehicle_type == "bicycle":
                    total_bicycle_count += 1
                #outcome 10
                if speed_limit < speed:
                    over_speed_vehicle_count += 1
                #outcome 11
                if junction_name == 'elm avenue/rabbit road':
                    total_vehicle_count_through_elm += 1
                #outcome13
                    if vehicle_type == 'scooter':
                        scooter_count += 1
                #outcome 12
                if junction_name == 'hanley highway/westway':
                    total_vehicle_count_through_han += 1
                    #outcome 14
                    if time_str:# Check if the record is for the specified junction
                        time_obj = datetime.strptime(time_str, "%H:%M:%S") #getting time of day in time format
                        hour = time_obj.hour #splitting hour from formatted time
                        hour_counts[hour] += 1 #counting hours and appending to a list
                    
                #outcome 16
                if weather== 'heavy rain' or weather=='light rain':
                    if time_str:
                        time_obj = datetime.strptime(time_str, "%H:%M:%S")
                        hour = time_obj.hour
                        rain_counts.append(hour)
                        rain_set=set(rain_counts)
                        
                        


            # Final calculations
            
            #outcome 8
            truck_percentage = (total_truck_count / total_vehicle_count) * 100 if total_vehicle_count else 0
            #outcome 9
            bicycle_count_per_hour = (total_bicycle_count / 24) if total_bicycle_count else 0
            #outcome 13
            scooter_percentage = (scooter_count / total_vehicle_count_through_elm) * 100 if total_vehicle_count_through_elm else 0
            #outcome 14
            peak_hour_vehicle_count = max(hour_counts)
            #outcome 15
            peak_hour = hour_counts.index(peak_hour_vehicle_count)
            peak_hour2 = hour_counts.index(peak_hour_vehicle_count)+1

            #outcome 16
            total_rain_count=len(rain_set)

            #getting the output to a list
            outcomes = [
                file_name,
                total_vehicle_count,
                total_truck_count,
                electric_vehicle_count,
                two_wheeled_vehicle_count,
                north_buss_count_leaving_elm,
                vehicle_count_going_straight,
                truck_percentage,
                bicycle_count_per_hour,
                over_speed_vehicle_count,
                total_vehicle_count_through_elm,
                total_vehicle_count_through_han,
                scooter_percentage,
                peak_hour_vehicle_count,
                peak_hour,
                peak_hour2,
                total_rain_count
            ]
            

    except FileNotFoundError:
        print(f"File '{file_name}' not found!!!. Please re-enter the date.")
        print()
        day, month, year = validate_date_input()
        print()
        file_name = process_file_name(day, month, year)
        return process_csv_data(file_name)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    return outcomes
#B: Displaying the data
def display_outcomes(outcomes):
    
    if not outcomes or len(outcomes) < 16:  # Check if outcomes is None or not long enough
        print("No valid data available to display.")
        return

    output_text=f"""
            Here is the requested traffic data.
            
            *********************************
            The selected data file: {(outcomes[0])}
            *********************************
            
            The total number of vehicles for this date: {outcomes[1]}
            The total number of trucks for this date: {outcomes[2]}
            The total number of electric vehicles for this date: {outcomes[3]}
            The total number of “two wheeled” vehicles for this date: {outcomes[4]}
            The total number of busses leaving Elm Avenue/Rabbit Road heading north: {outcomes[5]}
            The total number of vehicles passing through both junctions without turning left or right: {outcomes[6]}
            The percentage of total vehicles recorded that are Trucks for this date: {round(outcomes[7])}%
            The average number Bicycles per hour for this date: {round(outcomes[8])}
            The total number of vehicles recorded as over the speed limit for this date: {outcomes[9]}
            The total number of vehicles recorded through Elm Avenue/Rabbit Road junction: {outcomes[10]}
            The total number of vehicles recorded through Hanley Highway/Westway junction: {outcomes[11]}
            {int(outcomes[12])}% of vehicles recorded through Elm Avenue/Rabbit Road that are Scooters.
            The highest number of vehicles in an hour on Hanley Highway/Westway: {outcomes[13]}
            The most vehicles through Hanley Highway/Westway were recorded between: {outcomes[14]}:00 between {outcomes[15]}:00
            The number of hours of rain for this date: {outcomes[16]}

            *********************************
            
            """
    print(output_text)
    return output_text


# Task C: Save Results to Text File
def save_results_to_file(output_text):
    with open("results.txt", "a")as file:
        file.write(output_text)
        return
    
#Main program flow
def main():
    print("""
    *******     Traffic Flow Data Analysis      *******
    """)

    while True:
        day, month, year=validate_date_input()
        print('------------------------------------------------------------------------------------------------------------------------')
        file_name=process_file_name(day, month, year)
        outcomes=process_csv_data(file_name)
        output_text=display_outcomes(outcomes)
        print('------------------------------------------------------------------------------------------------------------------------')
        save_results_to_file(output_text)
        load_dataset = validate_continue_input()
        print()
        
        

        if load_dataset =='N':
            break
if __name__ == "__main__":
    main()
# if you have been contracted to do this assignment please do not remove this line
