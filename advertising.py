# Advertising Simulator
# This program simulates the advertising of a product over a period of time.
# It will simulate the number of people who have seen the product advertising, brand experience, and product experience.

import numpy as np
import pandas as pd


class brand:
    def __init__(self, brand_name, brand_budget, brand_power):
        self.brand_name = brand_name
        self.advertising_budget = brand_budget
        self.brand_power = brand_power

    def __str__(self):
        return "Brand Name: " + self.brand_name + ", Brand Budget: " + str(self.advertising_budget) + ", Brand Power: " + str(self.brand_power)


class customer:
    def __init__(self):
        self.attitude_towards_brand = {}
        self.attitude_towards_advertising = {}
        self.advertising_exposure = {}
    
    def couch_time(self, brand_name, campaign_name):
        if brand_name not in self.attitude_towards_brand:
            self.attitude_towards_brand[brand_name] = 1
        else:
            if self.attitude_towards_brand[brand_name] <= 100:
                self.attitude_towards_brand[brand_name] += 1
        if campaign_name not in self.attitude_towards_advertising:
            self.attitude_towards_brand[brand_name] = 1
        else:
            if self.attitude_towards_brand[brand_name] <= 100:
                self.attitude_towards_brand[brand_name] += 1
        if campaign_name not in self.advertising_exposure:
            self.advertising_exposure[campaign_name] = 1
        else:
            self.advertising_exposure[campaign_name] += 1
    
    def __str__(self):
        return "Attitude towards brand: " + str(self.attitude_towards_brand) + ", Attitude towards advertising: " + str(self.attitude_towards_advertising) + ", Advertising Exposure: " + str(self.advertising_exposure)
                

class advertising:
    def __init__(self, brand_name, campaign_name, expense):
        self.brand_name = brand_name
        self.campaign_name = campaign_name
        self.advertising_expense = expense

    def __str__(self):
        return "Advertising Budget: " + str(self.advertising_budget) + ", Advertising expense: " + str(self.advertising_power)

    def advertise(self, customer, brand):
        customer.couch_time(self.brand_name, self.campaign_name)
        brand.advertising_budget -= self.advertising_expense


# Customer objects
customers = [customer() for i in range(100000)]

# Brand objects
brands = [brand("Coca-Cola", 1000000, 100), 
          brand("Pepsi", 1000000, 100), 
          brand("Ford", 1000000, 100), 
          brand("General Motors", 1000000, 100), 
          brand("Toyota", 1000000, 100), 
          brand("Honda", 1000000, 100), 
          brand("Nissan", 1000000, 100), 
          brand("Hyundai", 1000000, 100), 
          brand("Dr. Pepper", 1000000, 100), 
          brand("Sprite", 1000000, 100),
          brand("Starbucks", 1000000, 100)]

# Brand names
brand_name_lst = [brand.brand_name for brand in brands]
# Randomly Generated Campaign names
campaign_name_lst = [brand.brand_name + " Campaign " + str(i) for brand in brands for i in range(np.random.randint(10))]
# Advertising objects
ads = [advertising(np.random.choice(brand_name_lst), np.random.choice(campaign_name_lst), np.random.randint(5, 20)) for i in range(100)]


for n in range(100):
    np.random.seed(n)
    for i in range(len(customers)):
        for j in range(len(brand_name_lst)):
            for k in range(len(ads)):
                ads[k].advertise(customers[i], brands[j])
                

print(customers[1].advertising_exposure)
print(customers[1].attitude_towards_brand)
print(customers[1].attitude_towards_advertising)    

