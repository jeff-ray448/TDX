TDX - Trasport Data Exchange
[TDX]https://tdx.transportdata.tw/

This project utilizes an API to gather JSON data from CCTV cameras, including their locations and real-time video feeds. The JSON data is processed and displayed on a Leaflet map on the website. It covers CCTV cameras situated along highways, freeways, and roads.

## Installation

1. git clone https://github.com/jeff-ray448/TDX
2. cd  TDX
3. pip install -r requirements.txt
4. Configure `app_id` and `app_key`:
    Add your `app_id` and `app_key` in the `app.py` file.

## Usage

1. python3 app.py
2. Open a web browser and navigate to `http://localhost:5000` to view the map display.


## Features

- select CCTV from different cities
- Real-time retrieval of CCTV camera locations and video stream data.
- Display of CCTV camera locations on a website using Leaflet maps.
- Support for searching CCTV data by city and road.

## Contributing

If you find any issues or have any suggestions for improvement, feel free to open an issue or submit a pull request.

## License

[MIT License](LICENSE)
