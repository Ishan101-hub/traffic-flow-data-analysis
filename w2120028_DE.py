#Author:I. E. A. Udawatte
#Date:23/12/2024
#Student ID:20232686 / 2120028(UOW)

# Task D: Histogram Display
import tkinter as tk
import csv
from datetime import datetime, date
from w2120028_ABC import process_csv_data, display_outcomes, save_results_to_file

# Constants
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600

class HistogramApp:
    def __init__(self, traffic_data, survey_date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.main = tk.Tk()
        self.traffic_data = traffic_data
        self.survey_date = survey_date  # Store the date for display in the heading

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.main.geometry('1000x600')
        self.main.title("Histogram")
        self.canvas = tk.Canvas(self.main, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="lavender")
        self.canvas.pack()

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Heading of the Histogram with the date
        heading_text = f"Histogram of Vehicle Frequency per Hour ({self.survey_date})"
        self.canvas.create_text((CANVAS_WIDTH / 2, 25), text=heading_text, font=("Arial", 12, "bold"))

        # Creating color legend(s)
        rectangle_box_y = 50
        legend_items_list = [
            ("mediumpurple", "Elm Avenue/Rabbit Road Junction"),
            ("skyblue", "Hanley Highway/Westway Junction")
        ]

        for color, text in legend_items_list:
            # Color legend box
            self.canvas.create_rectangle((50, rectangle_box_y, 60, rectangle_box_y + 10), fill=color)
            # Color legend text
            self.canvas.create_text((70, rectangle_box_y + 5), text=text, anchor="w", font=("Arial", 10), fill="black")
            rectangle_box_y += 20
        
        # X-axis label
        self.canvas.create_text((CANVAS_WIDTH / 2, 530), text="Hours 00:00 to 24:00", font=("Arial", 10), fill="midnightblue")

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        margin = 50
        bar_width = 10
        bar_spacing = 0.8  # Space between bars of each category
        category_spacing = (CANVAS_WIDTH - 3 * margin) / 24  # One category for each hour
        max_height = CANVAS_HEIGHT - 6 * margin

        # Get the maximum value to scale bars proportionally
        max_value = max(
            max(map(int, junction.values())) for junction in self.traffic_data.values()
        )
        if max_value == 0:
            print("Warning: No traffic data available.")
            max_value = 1

        # Draw bars
        for i, hour in enumerate(range(24)):
            label = f"{hour:02}"
            elm_value = self.traffic_data["Elm Avenue/Rabbit Road"].get(label, 0)
            hanley_value = self.traffic_data["Hanley Highway/Westway"].get(label, 0)

            x_start = margin + i * category_spacing
            bar1_x1 = x_start
            bar1_x2 = bar1_x1 + bar_width
            bar2_x1 = bar1_x2 + bar_spacing
            bar2_x2 = bar2_x1 + bar_width

            bar1_height = (elm_value / max_value) * max_height
            bar2_height = (hanley_value / max_value) * max_height
            y_base = CANVAS_HEIGHT - margin - 60

            # Draw the first bar
            self.canvas.create_rectangle(bar1_x1, y_base - bar1_height, bar1_x2, y_base, fill="mediumpurple", width=0)
            self.canvas.create_text(bar1_x1 + bar_width / 2, y_base - bar1_height - 10, text=str(elm_value), fill="blueviolet", font=("Arial", 7))

            # Draw the second bar
            self.canvas.create_rectangle(bar2_x1, y_base - bar2_height, bar2_x2, y_base, fill="skyblue", width=0)
            self.canvas.create_text(bar2_x1 + bar_width / 2, y_base - bar2_height - 10, text=str(hanley_value), fill="dodgerblue", font=("Arial", 7))

            # Add label for the hour
            self.canvas.create_text((bar1_x1 + bar2_x2) / 2, y_base + 15, text=label, fill="midnightblue", font=("Arial", 10, "bold"))

        # Draw x-axis
        self.canvas.create_line(margin, y_base, CANVAS_WIDTH - margin, y_base, width=1)

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.add_legend()
        self.draw_histogram()
        self.main.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.hour_counts = [0] * 24
        self.hour_counts2 = [0] * 24

    def load_csv_file(self, file_name):
        """
        Loads a CSV file and processes its data.
        """
        # Reset counts each time data is processed
        self.hour_counts = [0] * 24
        self.hour_counts2 = [0] * 24

        try:
            with open(file_name, "r") as file:
                csv_content = csv.DictReader(file)
                for row in csv_content:
                    junction_name = row.get("JunctionName", "").lower()
                    time_str = row.get("timeOfDay")
                    if time_str:
                        time_obj = datetime.strptime(time_str, "%H:%M:%S")
                        hour = time_obj.hour
                        if junction_name == "elm avenue/rabbit road":
                            self.hour_counts[hour] += 1
                        elif junction_name == "hanley highway/westway":
                            self.hour_counts2[hour] += 1
            return True
        except FileNotFoundError:
            return False
    
    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        # Validate day
        while True:
            try:
                self.day = int(input("Please enter the day of the survey in the format DD: "))
                if self.day < 1 or self.day > 31:
                    print("Out of range - values must be in the range 1 and 31.")
                    continue
                break
            except ValueError:
                print(f"Integer required!!!")
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

        # Validate month
        while True:
            try:
                self.month = int(input("Please enter the month of the survey in the format MM: "))
                if self.month < 1 or self.month > 12:
                    print("Out of range - values must be in the range 1 to 12.")
                    continue
                break
            except ValueError:
                print(f"Integer required!!!")
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

        # Validate year
        while True:
            try:
                self.year = int(input("Please enter the year of the survey in the format YYYY: "))
                if self.year < 2000 or self.year > 2024:
                    print("Out of range - values must range from 2000 and 2024")
                    continue
                date(self.year, self.month, self.day)  # Validate if the date is valid
                break
            except ValueError as v:
                if 'invalid literal for int()' in str(v):
                    print(f"Integer required!!!")
                if 'day is out of range for month' in str(v):
                    print('The day is out of range for the month!!, Please re-enter the date.')
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
        
        return self.day, self.month, self.year

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.hour_counts = [0] * 24
        self.hour_counts2 = [0] * 24
        self.current_data = None
        with open("results.txt","w") as file:
            file.write("")
        print("Previous data cleared.")

    def process_file_name(self, day, month, year):
        """Generates the filename based on the provided day, month, and year.""" 
        file_name=f"traffic_data{day:02}{month:02}{year}.csv"
        return file_name

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        print("Traffic Flow Data Analysis")

        while True:
            # Get user input for file date using imported function
            day, month, year = self.handle_user_interaction()
            file_name = self.process_file_name(day, month, year)
            survey_date = f"{day:02}/{month:02}/{year}"  # Format the date for display

            if self.load_csv_file(file_name):
                outcomes = process_csv_data(file_name)
                output_text = display_outcomes(outcomes)
                save_results_to_file(output_text)
                traffic_data = {
                    "Elm Avenue/Rabbit Road": {f"{hour:02}": self.hour_counts[hour] for hour in range(24)},
                    "Hanley Highway/Westway": {f"{hour:02}": self.hour_counts2[hour] for hour in range(24)},
                }
                app = HistogramApp(traffic_data, survey_date)
                app.run()
            else:
                print(f"File '{file_name}' not found!!!. Please re-enter the date.")
                continue

            # Ask if the user wants to load another file
            while True:
                response = input("Do you want to load another dataset? (Y/N): ").strip().upper()
                if response in {"Y", "YES"}:
                    self.clear_previous_data()
                    break
                elif response in {"N", "NO"}:
                    print("Exiting program. Goodbye!")
                    return
                else:
                    print("Invalid input. Please enter Y or N.")

if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
