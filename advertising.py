# Advertising Simulator
# This program simulates the advertising of a product over a period of time.
# It will simulate the number of people who have seen the product advertising, brand experience, and product experience.

import numpy as np
import pandas as pd 
import math
import seaborn as sns
import matplotlib.pyplot as plt


class customer:
    def __init__(self):
        # Awareness
        self.advertising_exposure = {}
        # Interest
        # Attitude towards advertising
        self.attitude_towards_advertising = {}
        # Desire
        self.attitude_towards_brand = {}
        # Action: Purchase decision
        self.brand_experience = {}
        # Budget
        self.budget = np.random.randint(1000, 5000)
        # Purchase decision
        self.likelihood_of_purchase = {}
        
    def couch_time(self, brand_name, campaign_name, effectiveness, brand_power):
        # Advertising Exposure
        if campaign_name not in self.advertising_exposure:
            self.advertising_exposure[campaign_name] = 1
        else:
            self.advertising_exposure[campaign_name] += 1
        
        # Attitude towards advertising
        if campaign_name not in self.attitude_towards_advertising:
            self.attitude_towards_advertising[campaign_name] = 1
        else:
            if self.attitude_towards_advertising[campaign_name] <= 100:
                self.attitude_towards_advertising[campaign_name] += np.log(effectiveness * self.advertising_exposure[campaign_name]+ 1)
        
        # Attitude towards brand
        if brand_name not in self.attitude_towards_brand:
            self.attitude_towards_brand[brand_name] = 1
        else:
            if self.attitude_towards_brand[brand_name] <= 100:
                self.attitude_towards_brand[brand_name] += np.log(1 + brand_power * self.attitude_towards_advertising[campaign_name] + self.brand_experience[brand_name])
                for other_brand in self.attitude_towards_brand.keys():
                    if other_brand != brand_name:
                        self.attitude_towards_brand[other_brand] -= np.random.normal(0, 0.5) * np.log(1 + brand_power * self.attitude_towards_advertising[campaign_name] + self.brand_experience[brand_name])
                        self.attitude_towards_brand[other_brand] = max(0, self.attitude_towards_brand[other_brand])


    def purchase(self, brand_name, item_price, brand_sales):
        # Random seed assignment
        np.random.seed(0)
        # Purchase decision
        # Purchase decision is binary variable, 1 for purchase and 0 for no purchase
        # If there is a previous brand experience, the probability of purchase will be higher than brand without experience
        if brand_name not in self.brand_experience:
            self.brand_experience[brand_name] = 0

        # Get the likelihood of purchase which will be used for binomial distribution.
        # Sigmoid function to get the probability of purchase to bound in range between 0 and 1
        if self.brand_experience[brand_name] == 0:
            # Without this condition, if the customers are exposed to same brand advertising several times at the beginning, the likelihood of purchase will be 1 and this will lead to np.log to zero.
            # In other words, the likelihood of purchase will be 0.5 for first few times.
            # This is not correct considering the nature of the advertising exposures in our daily life.
            # We are exposed to two brands' advertisings repeadetly.
            if self.attitude_towards_brand[brand_name] == sum(self.attitude_towards_brand.values()):
                # Due to the reason, put the likelihood of purchase to random variable generation.
                # Considering the nature of randomness in consumer behavior, this is more realistic.
                likelihood_of_purchase = np.random.uniform(0, 0.5)
            else:
                likelihood_of_purchase = np.log((self.attitude_towards_brand[brand_name]) / sum(self.attitude_towards_brand.values()))
        else:
            likelihood_of_purchase = np.log((self.attitude_towards_brand[brand_name]) / sum(self.attitude_towards_brand.values())) * np.log(self.brand_experience[brand_name])

        #likelihood_of_purchase = np.log((self.attitude_towards_brand[brand_name])  / sum(self.attitude_towards_brand.values())) 
        likelihood_of_purchase = sigmoid(likelihood_of_purchase)
        
        
        # if brand_name not in self.likelihood_of_purchase:
        if brand_name not in self.likelihood_of_purchase:
            self.likelihood_of_purchase[brand_name] = []
        # append the likelihood of purchase to the list
        self.likelihood_of_purchase[brand_name].append(likelihood_of_purchase)
        

        # Purchase decision
        status = np.random.binomial(1, likelihood_of_purchase)
        if status == 1 and self.budget > item_price:
            self.brand_experience[brand_name] += 1
            brand_sales += item_price
            return brand_sales
        else:
            # print("Not enough money to purchase the item.")
            self.budget += np.random.randint(100, 500)
            return brand_sales
                   
    def __str__(self):
        return "Attitude towards brand: " + str(self.attitude_towards_brand) + ", Attitude towards advertising: " + str(self.attitude_towards_advertising) + ", Advertising Exposure: " + str(self.advertising_exposure)


class brand:
    def __init__(self, brand_name, brand_budget, brand_power, item_price):
        self.brand_name = brand_name
        self.advertising_spending = 0
        self.advertising_budget = brand_budget
        self.brand_power = brand_power
        self.campaign = {}
        self.item_price = item_price
        self.brand_sales = 0
        campaign_name_lst = [self.brand_name + " Campaign " + str(i) for i in range(np.random.randint(3, 10))]
        for ad_campaign in campaign_name_lst:
            self.campaign[ad_campaign] = {}
            self.campaign[ad_campaign]["expense"] = np.random.normal(3,1)
            self.campaign[ad_campaign]["exposure"] = 0
            self.campaign[ad_campaign]["advertising_effectiveness"] = np.random.normal(1,0.25)
            # self.campaign[ad_campaign]["total_expense"] += self.campaign[ad_campaign]["expense"]


    def advertise(self, customer):
        ad_campaign = np.random.choice([element for element in self.campaign.keys()])
        if self.advertising_budget > self.campaign[ad_campaign]["expense"]:
            self.advertising_budget -= self.campaign[ad_campaign]["expense"]
            self.advertising_spending += self.campaign[ad_campaign]["expense"]
            self.campaign[ad_campaign]["exposure"] += 1
            customer.couch_time(self.brand_name, ad_campaign, self.campaign[ad_campaign]["advertising_effectiveness"], self.brand_power)
            self.brand_sales = customer.purchase(self.brand_name, self.item_price, self.brand_sales)
        else:
            print("No budget left for advertising")
            self.brand_sales = customer.purchase(self.brand_name, self.item_price, self.brand_sales/100)


def sigmoid(x):
    return (1 / (1 + math.exp(-x)))


def simulate(customers, brands, number_of_simulations):
    ads_effects = []
    # Expose advertisings
    for n in range(number_of_simulations):
        np.random.seed(n)
        i = np.random.choice(range(len(customers)))
        j = np.random.choice(range(len(brands)))
        brands[j].advertise(customers[i])
        ads_effects.append([i, 
                            j, 
                            customers[i].likelihood_of_purchase])

    # Create a dataframe
    df = pd.DataFrame(ads_effects, columns = ["Customer", 
                                            "Brand", 
                                            "Likelihood of Purchase"] )

    tmp = df[['Customer', 'Brand', 'Likelihood of Purchase']]
    temp = pd.concat([tmp[["Customer", "Brand"]], tmp["Likelihood of Purchase"].apply(pd.Series)], axis = 1)
    temp = temp.drop_duplicates(["Customer", "Brand"], keep = "last").melt(id_vars = ["Customer", "Brand"], value_name = "Likelihood of Purchase")
    temp = temp.explode("Likelihood of Purchase", ignore_index = False).reset_index().rename(columns = {"index": "id"})
    # temp = temp.explode("Likelihood of Purchase", ignore_index = True)
    temp["customer_brand"] = temp["Customer"].astype(str) + "-" + temp["Brand"].astype(str)
    return temp



# transform the simulation outcome to a dataframe for visualization.
def visualize(dataframe):
    dataframe["index"] = dataframe.groupby(["id", "variable"]).cumcount()
    return dataframe


def customer_mind(dataframe):
    final = dataframe.drop_duplicates(["Customer", "Brand", "variable"], keep = "last").sort_values(by = ["Customer", "Brand", "Likelihood of Purchase"], ascending = [True, True, False]).reset_index(drop = True)
    return_df = pd.DataFrame()
    for i in final["id"].unique():
        tmp = final[final["id"] == i]
        max_value = tmp["Likelihood of Purchase"].max()
        if len(tmp) > 0:
            tmp["NumberOfFavorites"] = len(tmp[tmp["Likelihood of Purchase"] >= max_value - 0.01])
            return_df = pd.concat([return_df, tmp])
    return return_df


# transform the simulation outcome to a dataframe for visualization.
def visualize(dataframe):
    '''
    unique_id = dataframe["id"].unique()
    brand_lst = dataframe["variable"].unique()
    dataframe = dataframe[dataframe["Brand"] == 0]
    return_df = pd.DataFrame()
    for id in unique_id:
        for brandname in brand_lst:
            tmp1 = dataframe[(dataframe["id"] == id) & (dataframe["variable"] == brandname)].reset_index(drop = True).reset_index(drop = False)
            #tmp1 = dataframe[(dataframe["id"] == id)].reset_index(drop = True).reset_index(drop = False)
            return_df = pd.concat([return_df, tmp1])
    return return_df
    '''
    dataframe["index"] = dataframe.groupby(["id", "variable"]).cumcount()
    return dataframe

def customer_mind(dataframe):
    final = dataframe.drop_duplicates(["Customer", "Brand", "variable"], keep = "last").sort_values(by = ["Customer", "Brand", "Likelihood of Purchase"], ascending = [True, True, False]).reset_index(drop = True)
    return_df = pd.DataFrame()
    for i in final["id"].unique():
        tmp = final[final["id"] == i]
        max_value = tmp["Likelihood of Purchase"].max()
        if len(tmp) > 0:
            tmp["NumberOfFavorites"] = len(tmp[tmp["Likelihood of Purchase"] >= max_value - 0.01])
            return_df = pd.concat([return_df, tmp])
    return return_df
