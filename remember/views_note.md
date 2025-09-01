# Views to be Remembered
Remember that API in Django relies in 3 things: `url`, `serializers`, `views`,

- `urls.py` file for the URL routes
- `serializers.py` file to transform the data into JSON
- `views.py` file to apply logic to each API endpoint

So whatever you see in the browsable API, how it is viewed, whether you can post or put whatever, it is the views that has something to do with it pecifically the parent class your view class inherits from.