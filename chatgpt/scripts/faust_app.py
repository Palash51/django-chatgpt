import faust
import requests
from bs4 import BeautifulSoup

app = faust.App('myapp', broker='kafka://localhost:9092')

class Website(faust.Record):
    website_url: str
    data: str

website_topic = app.topic('website_data', value_type=Website)

def extract_data_from_site(web_url):
    # perform data extraction for website here
    
    # Make a GET request to the website
    response = requests.get(web_url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the products on the page
    products = soup.find_all("div", class_="col-sm-4 col-lg-4 col-md-4")

    # Extract information from each product
    for product in products:
        # Get the product name
        print(product)
        name = "test product"
        
        # Get the product price
        price = 10000
        
        # Get the product description
        description = "test description"
        
        # Print the product information
        return {
            'website_url': web_url,
            'Name': name,
            'Price': price,
            'Description': description
        }
        


@app.agent(website_topic)
async def process_website_data(websites):
    async for website in websites:
        # perform data extraction for website here
        extracted_data = extract_data_from_site(website.website_url)
        print(f"Extracted data for website: {extracted_data}")
