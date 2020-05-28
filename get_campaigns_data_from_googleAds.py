# install libraries using pip3 install googleads, datetime, os, pandas

# importing libraries
import sys
from googleads import adwords
import datetime
import os
import pandas as pd


# Gets campaigns data for n days before today
def get_campaignDFn(n):
    date = (datetime.datetime.now() + datetime.timedelta(-(n+1))).strftime('%Y%m%d')
    
    # Initialize client object.
    adwords_client = adwords.AdWordsClient.LoadFromStorage(r'''/path/to/googleads.yaml''')
    adwords_client.SetClientCustomerId('10-digit-customer-id')

    
    def main(client):
        output_file = 'day'+str(n)+'.csv'
#         print('file made')
    # Initialize appropriate service.
        report_downloader = client.GetReportDownloader(version='v201809')
#         print('report downloader')
        reportCSV = str()
#         print('csv')

    # Create report query.
        report_query = (adwords.ReportQueryBuilder()
                      .Select('CampaignName','Impressions', 'Clicks',
                              'Cost') # add any other required columns
                      .From('CAMPAIGN_PERFORMANCE_REPORT')
                      .During(date+','+date)
                      .Build())
#         print('query')
        orig_stdout = sys.stdout
        with open(output_file, 'w'):
            sys.stdout = open(output_file, 'w')
            reportCSV = report_downloader.DownloadReportWithAwql(
                report_query, 'CSV', sys.stdout, skip_report_header=False,
                skip_column_header=False, skip_report_summary=False,
                include_zero_impressions=False)
            sys.stdout.close()
            sys.stdout=orig_stdout
            return(reportCSV)
#         print('write')

    # Fetching Data and Pre-processing
    report = main(adwords_client)