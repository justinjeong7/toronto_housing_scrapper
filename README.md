# Toronto condo sales price scrapper
This is a quick side project to scrape sales prices for Toronto condo market.

Due to the fact that I am not sure how legal this scrapping is and I don't want the host to close down on loopholes, if you want to find out the host source, contact me directly.


## Usage:

### Install:
Coming soon

### Configuration:
In order to use this project, you will need to provide a configuration file.   This configuration file will require:

- url
- login_url
- search_url
- cred_data containing: `email`, `password`
- listing_map:

```
sold: 'Sld'
terminated: 'Ter'
suspended: 'Sus'
leased: 'Lsd'
```

### Objects:
There is really only one object you need to really use: `objects.scrapper.Scrapper`

#### `Scrapper.load_cred(filename)`:

`filename` is the yaml config file that contains the configuration mentioned above



#### `Scrapper.login()`:

login to the host source



#### `Scrapper.get_buildings`:

Get buildings that are available with historical data.  You can access buildings through `.buildings`


#### `Scrapper.get_history(building, type = 'sold')`

`building` is the dictionary variable that you will scan through.  `type` is to highlight what transaction records you want to filter on.
