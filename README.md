# up42-imagery-data - Charlotte Gephart

Hello! Welcome to my code challenge response. Thank you for your consideration, and I welcome any feedback you have!


## Setup:

To set up the code, download the repository, then use the command line to navigate to the downloaded folder. Install the required packages with 

```pip3 install -r requirements.txt```

## Running The Code

Once the required packages have been installed, you can then run the code from the command line. Start by running in one tab:

```python3 -m uvicorn process_sat_data:app --reload```

In another tab run:

```
curl -X 'PUT' \
  'http://127.0.0.1:8000/mean-value' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "geometry_json": "satellite_geometry.json",
  "cloud_cover_limit": 40
}'
```
You can change the parameters as desired, with ```geometry_json``` being the json file with the geometry you wish to search, and ```cloud_cover_limit``` as the int limit, [0,100].

You can also run this in the FastAPI Swagger UI (```http://127.0.0.1:8000/docs```), by clicking the ```PUT /mean-value``` tab, "Try it out", editing params if desired, then "Execute". 

## Testing

Unit tests are located in ```tests.py```. Run them from the command line with ```python3 tests.py```.
