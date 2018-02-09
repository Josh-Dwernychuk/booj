# booj
XML data extraction from endpoint, parsing of XML data, and writing of data to csv file


# Running the project
To run the project, run:
```
pip install -r requirements.txt
python booj.py
```

# Testing
All tests are currently passing.
Tests can be run with:
```
pytest test.py
```
The -s argument can be used with pytest to account for a debugger like so:
```
pytest -s test.py
```

# CSV Files
The created CSV file can be found at 'output_data/listings.csv'.

The CSV file created for testing purposes can be found at 'test_output_data/test_listings.csv'.
