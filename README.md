# up42-imagery-data - Charlotte Gephart

Hello! Welcome to my code challenge response. Thank you for your consideration, and I welcome any feedback you have!


## Setup:

To set up the code, download the repository, then use the command line to navigate to the downloaded folder. Install the required packages with 

```pip3 install -r requirements.txt```

## Running The Code

Once the required packages have been installed, navigate to your localhost/mean-value in your web browser (for me this was ```http://127.0.0.1:8000/mean-value```). You can then run the code from the command line by running:

```python3 -m uvicorn process_sat_data:app --reload```

Reload the browser page if necessary, and you should see the mean value output.

## Testing

Unit tests are located in ```tests.py```. Run them from the command line with ```python3 tests.py```.
