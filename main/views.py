from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import pandas as pd

def index(request):

    url = "https://eu.kobotoolbox.org/api/v2/assets/aYM2ds6krFGYbznTSfZcDw/data/?format=json"

    payload = {}
    headers = {
    'Authorization': 'Basic Y2VsZXN0aW5fMDE6QEt1cmFtYmFuYTQ=',
    'Cookie': 'csrftoken=kk8LLpzA8dZVgxBoYCCK9VKwU9VEQP3U; django_language=en'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
     # Extract the list of submissions
    results = data.get("results", [])
    #convert to pandas dataframe
    df = pd.DataFrame(results)
    number_transactions = len(df)
    #convert to numeric 
    df['cost_of_production'] = pd.to_numeric(df['cost_of_production'],errors='coerce')
    #calculate the total costs
    total_cost = df['cost_of_production'].sum()
    # calculate the total revenue
    df['price'] = pd.to_numeric(df['price'],errors='coerce')
    #convert revenue to number
    total_revenue = df['price'].sum()
    #Profits 
    profits = total_revenue-total_cost
    # Provide totals revenue by location using group by 
    revenue_loc = df.groupby('location').agg(
        n_trans = ('_id','count'),
        gr_total_revenue = ('price','sum'),
        gr_total_cost = ('cost_of_production','sum')
    ).reset_index()
    #create total numbers of transaction by payment methods
    payment_methods = df.groupby('payment').agg(
        nbr_payments = ('_id','count')
    ).reset_index()
    #create number of transaction per day
    daily_transactions = df.groupby('date').agg(
        trans_day = ('_id','count')
    ).reset_index()
     # converts to list such that chartJs can work properly
    locations = revenue_loc['location'].tolist()
    revenues = revenue_loc['gr_total_revenue'].fillna(0).tolist()
    payment_amount = payment_methods['nbr_payments'].fillna(0).tolist()
    payment_method = payment_methods['payment'].tolist()
    transaction_date = daily_transactions['date'].tolist()
    transaction_number_day = daily_transactions['trans_day'].fillna(0).tolist()

    context = {
        "transactions":number_transactions,
        "cost":total_cost,
        "revenue":total_revenue,
        "profits":profits,
        "locations":locations,
        "revenues":revenues,
        "payment_amount":payment_amount,
        "payment_method": payment_method,
        "transaction_date":transaction_date,
        "transaction_number_day":transaction_number_day
    }

    # print("Locations:", locations)
    # print("Revenues:", revenues)
    # print("Payment Method:", payment_method)
    # print("Payment Amount:", payment_amount)
    #print("number of transaction date:",daily_transactions)
    return render (request, 'main/dashboard.html',context)

def transaction_view(request):
    url = "https://eu.kobotoolbox.org/api/v2/assets/aYM2ds6krFGYbznTSfZcDw/data/?format=json"

    payload = {}
    headers = {
    'Authorization': 'Basic Y2VsZXN0aW5fMDE6QEt1cmFtYmFuYTQ=',
    'Cookie': 'csrftoken=kk8LLpzA8dZVgxBoYCCK9VKwU9VEQP3U; django_language=en'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
     # Extract the list of submissions
    results = data.get("results", [])
    #convert to pandas dataframe
    df = pd.DataFrame(results)
    df['product'] = df['product'].str.replace('_', ' ', regex=False)
    list_columns = []
    for tx in results:
        list_columns.append({
        'Date': tx.get('date'),
        'Location': tx.get('location'),
        'Category': tx.get('category'),
        'Product':tx.get('product'),
        'Cost_of_Production':tx.get('cost_of_production'),
        'Price':tx.get('price'),
        'Payment_Methods':tx.get('payment')
    })
    print(list_columns)
    return render (request,'main/transaction.html',{'transactions':list_columns})

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')

def user(request):
    return render(request, 'main/users.html')

    
    
    
    
    
    
   




