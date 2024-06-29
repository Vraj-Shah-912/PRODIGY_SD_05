import csv
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ScraperForm
import requests
from bs4 import BeautifulSoup

def scrape_product(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Selectors adjusted for "Books to Scrape"
    name = soup.select_one('div.product_main h1').text.strip()
    price = soup.select_one('p.price_color').text.strip()
    rating = soup.select_one('p.star-rating')['class'][1] if soup.select_one('p.star-rating') else 'No rating'

    return {
        'name': name,
        'price': price,
        'rating': rating,
    }

def index(request):
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            product_data = scrape_product(url)

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="products.csv"'

            writer = csv.writer(response)
            writer.writerow(['Name', 'Price', 'Rating'])
            writer.writerow([product_data['name'], product_data['price'], product_data['rating']])

            return response
    else:
        form = ScraperForm()

    return render(request, 'scraper/index.html', {'form': form})
