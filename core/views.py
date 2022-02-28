from django.shortcuts import render
# Create your views here.


def get_html_content(city):
    import requests
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def home(request):
    weather = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        # fetch the weather from Google.
        html_content = get_html_content(city)
        #importing beautifulSoup
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        weather = dict()
        weather['region'] = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        weather['dayhour'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')
    return render(request, 'core/home.html', {'weather': weather})