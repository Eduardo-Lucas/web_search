from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import SearchForm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search(request):
    results = None
    not_found = False
    page_obj = 0
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            results, not_found = perform_search(name)

            if results:
                paginator = Paginator(results, 5)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

    else:
        form = SearchForm()
    return render(request, 'searchapp/search.html', {'form': form, 'results': results, 'page_obj': page_obj, 'not_found': not_found})

def perform_search(name):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get('https://www.in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados')

    search_box = driver.find_element(By.NAME, 'search-bar')  # Atualize para o seletor correto
    search_box.send_keys(name)
    search_box.submit()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.resultado'))  # Atualize para o seletor correto
        )
        elements = driver.find_elements(By.CSS_SELECTOR, '.resultado')  # Atualize para o seletor correto
        if elements:
            results = [element.text for element in elements]
            not_found = False
        else:
            results = None
            not_found = True
    except Exception as e:
        results = None
        not_found = True
        print(f"An error occurred: {e}")

    driver.quit()
    return results, not_found
