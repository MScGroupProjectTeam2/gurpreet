import requests   
import postcodes_io_api
def get_location_detail(pc):    
    api  = postcodes_io_api.Api(debug_http=True)
    data = api.get_postcode(pc)
    return data

