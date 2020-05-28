# install libraries using pip3 install facebookads, facebook_business, datetime, os, pandas

# importing libraries
from facebookads.api import FacebookAdsApi
from facebookads.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount


# Gets campaigns data for n days before today
def get_campaignDFn(n):

    # Set the info to get connected to the API. Do NOT share this info
    my_app_id = 'APP_ID'
    my_app_secret = 'APP-SECRET'
    my_access_token = 'ACCESS-TOKEN'

    # Start the connection to the facebook API
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

    # Get yesterday's date for the filename, and the csv data
    yesterdaybad = datetime.datetime.now() - datetime.timedelta(days=(1+n))
    yesterdayslash = yesterdaybad.strftime('%Y/%m/%d')
    yesterdayhyphen = yesterdaybad.strftime('%Y-%m-%d')
    
    # params = {'time_range':{"since":"2019-08-25","until":"2019-08-25"},'level':'adset'} This is an example
    params['time_range']['since'] = yesterdayhyphen
    params['time_range']['until'] = yesterdayhyphen

    # Define the destination filename
    filename = 'data'+str(n)+'.csv'
    filelocation = filename

    # Open or create new file 
    try:
        csvfile = open(filelocation , 'w+', newline='')
    except:
        print ("Cannot open file.")


    # To keep track of rows added to file
    rows = 0

    try:
        # Create file writer
        filewriter = csv.writer(csvfile, delimiter=',')
    except Exception as err:
        print(err)

    # Create an addaccount object from the adaccount id to make it possible to get insights
    tempaccount = AdAccount("ad_account_ID")

    # Grab insight info for all ads in the adaccount
    ads = tempaccount.get_insights(params=params,
                                   fields=[AdsInsights.Field.account_id,
                       AdsInsights.Field.account_name,
                                           AdsInsights.Field.ad_id,
                                           AdsInsights.Field.ad_name,
                                           AdsInsights.Field.adset_id,
                                           AdsInsights.Field.adset_name,
                                           AdsInsights.Field.campaign_id,
                                           AdsInsights.Field.campaign_name,
                                           AdsInsights.Field.cost_per_outbound_click,
                                           AdsInsights.Field.outbound_clicks,
                                           AdsInsights.Field.spend,
                                           AdsInsights.Field.impressions
                                          ]  # add any other required fields
    );

    # Iterate through all accounts in the business account
    filewriter.writerow(["date", "adsetid", "adsetname","impressions", "clicks", "CPC",  "spend"])
    for ad in ads:
#         print(ad)
        # Set default values in case the insight info is empty
        date = yesterdayslash
        adsetid = ""
        adsetname = ""
        impressions = ""
        costperoutboundclick = ""
        outboundclicks = ""
        spend = ""

        # Set values from insight data
        if ('adset_id' in ad) :
            adsetid = ad[AdsInsights.Field.adset_id]
        if ('adset_name' in ad) :
            adsetname = ad[AdsInsights.Field.adset_name]
        if 'impressions' in ad:
            impressions = ad[AdsInsights.Field.impressions]
        if ('cost_per_outbound_click' in ad) : # This is stored strangely, takes a few steps to break through the layers
            costperoutboundclicklist = ad[AdsInsights.Field.cost_per_outbound_click]
            costperoutboundclickdict = costperoutboundclicklist[0]
            costperoutboundclick = costperoutboundclickdict.get('value')
        if ('outbound_clicks' in ad) : # This is stored strangely, takes a few steps to break through the layers
            outboundclickslist = ad[AdsInsights.Field.outbound_clicks]
            outboundclicksdict = outboundclickslist[0]
            outboundclicks = outboundclicksdict.get('value')
        if ('spend' in ad) :
            spend = ad[AdsInsights.Field.spend]

        # Write all ad info to the file, and increment the number of rows that will display
        filewriter.writerow([date, adsetid, adsetname, impressions, outboundclicks, costperoutboundclick, spend])
        rows += 1


    csvfile.close()

    # Print report
    print (str(rows) + " rows added to the file " + filename)