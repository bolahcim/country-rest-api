# Country REST API


### Prerequisities
Installed pip and docker-compose

### Instalation

Download the repository open terminal within the path of it.
Then run:
```
$ sudo docker-compose build
```
After succesfull build run:
```
$ sudo docker-compose up
```

## Description

Country REST API compares list of received countries with received ISO and returns countries that belong to the ISO in any given language.
Solution is created based on translator modul and on country_converter.
Countries and ISO inputs and outputs shold represent ISO 3166 international standard

## Tests
You can test that everything is build by sending GET request on http://localhost:5000/
and you should receive 
```
Hello, I am available to receive requests
```
Function of REST API can be tested by sending POST requests on
http://localhost:5000/match_country
Example: of body of POST request
```
{
	"iso": "svk",
	"countries": [
		"iran",
		"Slowakei",
		"Vatikan",
		"Slovaška",
		"Slovakia",
		"Belgrade",
		"España",
		"Nizozemsko"
	]
}
```
Response:
```
{
    "Status Code": 200,
    "count": 3,
    "countries": [
        "slowakei",
        "slovaška",
        "slovakia"
    ],
    "iso": "svk"
}
```