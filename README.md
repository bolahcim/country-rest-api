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

For this Country ISO REST API I chose a bit different approach.
I did not wanted to create big database with adding values for country names in all different languages.
Therefore, I implemented it with translator module that detects and translate any given text.
Current solution is not production ready and it must be tested more deeply
as translation from some languages might differ from country name stored in DB.
DB is created of country codes described in ISO 3166 international standard

## Tests
You can test that everything is build by sending GET request on http://localhost:5000/
and you should receive 
```
Hello, I am available to receive requests
```
Function of REST API can be tested by sending POST requests on
http://localhost:5000/match_country
with body
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
