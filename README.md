# Address transformation
With this short and simple Python script you can easily transform unstructured and inconsistent address data to the format you like. It uses the free Google Maps Geocoding API. You just need to get a API key [here](https://developers.google.com/maps/documentation/geocoding/start#get-a-key).

More information about the Google Maps Geocoding API can be found [here](https://developers.google.com/maps/documentation/geocoding/intro), including an example response of the API and a list of possible address attributes the API delivers.

## Requirements
* Pyhton 3 is needed to execute the script
* make sure that all dependencies (from imports) are installed and correctly installed

## How it works
Clone the repository
```
git clone git@github.com:bastians/address_transformation.git
```
and switch to the folder
```
cd address_transformation
```
In that folder, prepare the `input.csv` file with the unstructured, inconsistent or incomplete addresses you want to transform. The `input.csv` has two columns: 
In the first column, you can add ids for the addresses you want to trasnform. The ids are a reference and will be also added to the output file. If you don't have ids, you can leave the column empty but don't remove it and also keep the first delimiter `;`.

In the second column you have to put the addresses you want to transform. Make sure, that the address does not contain a semicolon (`;`) as this is the delimiter for the columns in the CSV file.

Example with filled id column:
```
id;address
1;1600 Amphiteatre Pkwy Mountan View 94047
2;White House Pennsylvania 1600 Washinton
```

Example with empty id column:
```
id;address
;1600 Amphiteatre Pkwy Mountan View 94047
;White House Pennsylvania 1600 Washinton
```

Add your [Google Maps Geocoding API key](https://developers.google.com/maps/documentation/geocoding/start#get-a-key) to the file `address_transformation.py` and save it.

Execute the script with
```
python3 address_transformation.py
```

An output file with a timestamp is created that contains the transformed and structured address data.

Enjoy!

Thanks to [Thilo Huellmann](https://github.com/thilohuellmann) who initially created that script.