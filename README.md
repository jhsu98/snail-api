# snail-api

A simple Flask app to simulate a snail climbing out of a well. API is written to POST a simluation or GET existing results, which are stored in a CSV file after each simulation. To POST to the API, four values are required:
1. Height of the Well
2. Original Climbing Distance (during each day)
3. Sliding Distance (during each night)
4. Fatigue Factor (percentage climbing distance atrophies each day)

The API will return the original values along with the result, which is a success/failure on the deciding day.

## Running the App
To run the app, download to your local computer and ensure both Python and Flask are installed.

Navigate to the directory and begin the local server with the command:
```python
python app.py
```

Then, in your browser, navigate to `localhost:5000` to view the entry form and existing results.