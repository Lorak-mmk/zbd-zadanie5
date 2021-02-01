#!/usr/bin/env python

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import secrets
import argparse
import json
import sys

query_gql = gql('''
query data_fetch($time_begin: Datetime!, $time_end: Datetime!, $user_id: String, $user_year: Int, $user_income: BigInt, $user_lat: Float, $user_lon: Float, $user_interest: String, $ad_id: String, $ad_height: Int, $ad_width: Int, $ad_color: String, $ad_text: String) {
  allViews(
    filter: {
   adByAdId:{
      adsTextsByAdId:{
         some:{
            name:{
               equalTo:$ad_text
            }
         }
      },
      color:{
         equalTo:$ad_color
      },
      height:{
         equalTo:$ad_height
      },
      id:{
         equalTo:$ad_id
      },
      width:{
         equalTo:$ad_width
      }
   },
   userByUserId:{
      bornYear:{
         equalTo:$user_year
      },
      id:{
         equalTo:$user_id
      },
      income:{
         equalTo:$user_income
      },
      lat:{
         equalTo:$user_lat
      },
      lon:{
         equalTo:$user_lon
      },
      interestsByUserId:{
         some:{
            name:{
               equalTo:$user_interest
            }
         }
      }
   },
   time:{
      greaterThanOrEqualTo:$time_begin,
      lessThanOrEqualTo:$time_end
   }
}
  ) {
    totalCount
  }
}
''')

class QueryData:
    def __init__(self, url):
        # Select your transport with a defined url endpoint
        self.transport = AIOHTTPTransport(url=url)
        
        # Create a GraphQL client using the defined transport
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
        
        self.query_gql = query_gql
    
    def query(self, params):
        if params.get('time_begin') is None or params.get('time_end') is None:
            print("You must specify time range")
            return
        return self.client.execute(self.query_gql, variable_values=params)
            


def main():
    try:
        query_api = QueryData("http://localhost:5000/graphql")
    except:
        print('Can\'t connect to GraphQL API')
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Query database for amount of views. You must specify time frame. Other arguments are optional')
        # $time_begin: Datetime, $time_end: Datetime
    # $user_id: String, $user_year: Int, $user_income: BigInt, $user_lat: Float, $user_lon: Float, $user_interest: String, 
    # $ad_id: String, $ad_height: Int, $ad_width: Int, $ad_color: String, $ad_text: String
    parser.add_argument('--time_begin', dest='time_begin', action='store')
    parser.add_argument('--time_end', dest='time_end', action='store')
    
    parser.add_argument('--user_id', dest='user_id', action='store')
    parser.add_argument('--user_year', dest='user_year', action='store', type=int)
    parser.add_argument('--user_income', dest='user_income', action='store')
    parser.add_argument('--user_lat', dest='user_lat', action='store', type=float)
    parser.add_argument('--user_lon', dest='user_lon', action='store', type=float)
    parser.add_argument('--user_interest', dest='user_interest', action='store')
    
    parser.add_argument('--ad_id', dest='ad_id', action='store')
    parser.add_argument('--ad_height', dest='ad_height', action='store', type=int)
    parser.add_argument('--ad_width', dest='ad_width', action='store', type=int)
    parser.add_argument('--ad_color', dest='ad_color', action='store')
    parser.add_argument('--ad_text', dest='ad_text', action='store')
    args = parser.parse_args()
    
    params = dict(vars(args))
    params = dict((k,v) for k,v in params.items() if v is not None)
    result = query_api.query(params)
    print(result['allViews']['totalCount'])


if __name__ == '__main__':
    main()



    
