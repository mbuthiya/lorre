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
        

        for harvests in harvest:
            for dateListDate in dateListConvert:
                if harvests.expected_harvest_date == dateListDate.date():
                    data[dateListDate.date().strftime('%d/%b/%Y')
                         ] = harvests.estimated_yield
                else:
                    data[dateListDate.date().strftime('%d/%b/%Y')
                         ] = None
        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
