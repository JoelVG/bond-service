## Bonds API
Small app to manage bonds

## Installation

PIP
[requirements.txt](https://github.com/JoelVG/bond-service/blob/develop/service/requirements.txt)
```pip install -r requirements.txt```

DOCKER
```
docker-compose build
docker-compose up  
```
ENDPOINTS
```
POST /api/bonds/                Create a new Bond object
GET	/api/bonds/                 List bonds that don't have a buyer attached
GET	/api/bonds/{id}	            Returns a specific bond details by id
PUT	/api/bonds/{id}/buy	        Buy a bond attached to the current user as a buyer
GET	/api/bonds?currency=USD	    List bonds that available to purchase. (currency in usd)
```
> Note: `seller, name, quantity, price` are required for post method