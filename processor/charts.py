import pygal
from datetime import datetime,timedelta
import pandas as pd 

from .models import Farm,Season


class ThisWeekHarvest():

    def __init__(self, **kwargs):
        self.chart = pygal.Bar(**kwargs)
        self.chart.title = 'Mango Raw materials in Kgs'
        

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''

        this_week = datetime.isocalendar(datetime.today())[1]
        harvest= [harvest_season for harvest_season in Season.objects.all() if datetime.isocalendar(harvest_season.expected_harvest_date)[1]== this_week]
        
        start = datetime.today() - timedelta(days=datetime.today().weekday())
        end = start + timedelta(days=6)

        dateList =pd.date_range(start,end)
        dateListConvert = list(map(pd.Timestamp.to_pydatetime,dateList))

        data = {}
        
        
        for day in dateListConvert:
           data[day.date()] = 0

        for harvests in harvest:
            if harvests.expected_harvest_date in data:
                data[harvests.expected_harvest_date] = harvests.estimated_yield
        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            day = ""
            
            if key.weekday() == 0:
                day = "Monday"
            elif key.weekday()==1:
                day = "Tuesday"
            elif key.weekday() == 2:
                day = "Wednesday"
            elif key.weekday() == 3:
                day = "Thurday"
            elif key.weekday() == 4:
                day = "Friday"
            elif key.weekday() == 5:
                day ="Saturday"
            else:
                day="Sunday"

            self.chart.add(day, value)
        
        # Return the rendered SVG
        return self.chart.render(is_unicode=True)

class Trend():

    def __init__(self, **kwargs):
       self.line_chart = pygal.Bar(**kwargs)
       self.line_chart.title= "Harvesting trend for the past 2 years in Kgs"
       self.line_chart.x_labels=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    
    def get_data(self):
        
        this_year = [harvest for harvest in Season.objects.all() if harvest.expected_harvest_date.year==datetime.today().year]
        last_year = [harvest for harvest in Season.objects.all() if harvest.expected_harvest_date.year==datetime.today().year -1]

        this_year_month_sum ={}
        last_year_month_sum = {}

        this_year_linelist = []
        last_year_linelist = []


        for harvest in this_year:
            this_year_month_sum.setdefault(harvest.expected_harvest_date.month,0)
            this_year_month_sum[harvest.expected_harvest_date.month] += harvest.estimated_yield
        

        
        for harvest in last_year:
            last_year_month_sum.setdefault(harvest.expected_harvest_date.month,0)
            last_year_month_sum[harvest.expected_harvest_date.month] += harvest.estimated_yield

        
        for i in range(1,13):

            if i in this_year_month_sum:
                this_year_linelist.append(this_year_month_sum[i])
                continue
            this_year_linelist.append(None)

        for i in range(1,13):

            if i in last_year_month_sum:
                last_year_linelist.append(last_year_month_sum[i])
                continue
            last_year_linelist.append(None)
       
        return this_year_linelist,last_year_linelist

    def generate(self):

        
        this_year,last_year = self.get_data()
        
        
        self.line_chart.add(str(datetime.today().year),this_year)

        self.line_chart.add(str(datetime.today().year -1), last_year)

        return self.line_chart.render()


class FarmTrend():

    def __init__(self, **kwargs):
       self.line_chart = pygal.Line(**kwargs)
       self.line_chart.title = "Harvesting trend"
       

    def get_data(self,farm):

        years = range(farm.date_added.year, datetime.today().year + 1)
        self.line_chart.x_labels = map(str, years)

        all_harvests = Season.objects.filter(farm=farm)
        
        total_year_yield = {}

        for harvest in all_harvests:
            total_year_yield.setdefault(harvest.expected_harvest_date.year,0)
            total_year_yield[harvest.expected_harvest_date.year] += harvest.estimated_yield    

        data = []

        for year in years:
            if year in total_year_yield:
                data.append(total_year_yield[year])
            else:
                data.append(None)

        return data

    def generate(self,farm):

        data = self.get_data(farm)

        self.line_chart.add("Yield",data)


        return self.line_chart.render()
      

