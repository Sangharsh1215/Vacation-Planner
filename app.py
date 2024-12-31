from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/results', methods=['GET'])
def results():
    try:
        # Load CSV files
        flights = pd.read_csv(r'C:\Users\Sangharsh\Desktop\git\flights.csv')
        hotels = pd.read_csv(r'C:\Users\Sangharsh\Desktop\git\hotels.csv')
        cabs = pd.read_csv(r'C:\Users\Sangharsh\Desktop\git\Cab.csv')
        activities = pd.read_csv(r'C:\Users\Sangharsh\Desktop\git\Activity.csv')

        # Convert dataframes to HTML tables
        flights_html = flights.to_html(classes='table', index=False)
        hotels_html = hotels.to_html(classes='table', index=False)
        cabs_html = cabs.to_html(classes='table', index=False)
        activities_html = activities.to_html(classes='table', index=False)

        # Pass HTML tables to the template
        return render_template(
            'results.html',
            flights_html=flights_html,
            hotels_html=hotels_html,
            cabs_html=cabs_html,
            activities_html=activities_html
        )
    except Exception as e:
        # Log error and display it
        print("Error occurred:", e)
        return f"<h1>An error occurred:</h1><p>{e}</p>"

if __name__ == '__main__':
    app.run(debug=True)
