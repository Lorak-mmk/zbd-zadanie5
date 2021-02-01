#!/usr/bin/env python

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import secrets
import argparse
import json
import sys

add_single_view_gql = gql('''
mutation addSingleView($user_id: String!, $ad_id: String!, $time: Datetime!) {
  createView(input: {view: {adId: $ad_id, userId: $user_id, time: $time}}) {
    view {
      id
    }
  }
}
''')

class MakeViews:
    def __init__(self, url):
        # Select your transport with a defined url endpoint
        self.transport = AIOHTTPTransport(url=url)
        
        # Create a GraphQL client using the defined transport
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
        
        self.add_single = add_single_view_gql
    
    def add_single_view_packed(self, variables):
        print(f'Creating new view: {variables}')
        self.client.execute(self.add_single, variable_values=variables)
    
    def add_single_view(self, user_id=None, ad_id=None, time=None):
        variables = {}
        if user_id is not None:
            variables["user_id"] = user_id
        if ad_id is not None:
            variables["ad_id"] = ad_id
        if time is not None:
            variables["time"] = time
        
        if len(variables) != 3:
            print("Not enough data")
            return
        
        self.add_single_view_packed(variables)
        
    
    def process_file(self, in_file):
        for line in in_file.readlines():
            if len(line) <= 1:
                continue
            if line.startswith('//'):
                continue
            line = json.loads(line)
            self.add_single_view_packed(line)
            


def main():
    try:
        maker = MakeViews("http://localhost:5000/graphql")
    except:
        print('Can\'t connect to GraphQL API')
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Load view (or multiple ads from a file) into a database')
    parser.add_argument('--file', dest='input_file', action='store', type=open)
    
    parser.add_argument('--user_id', dest='user_id', action='store', required=True)
    parser.add_argument('--ad_id', dest='ad_id', action='store', required=True)
    parser.add_argument('--time', dest='time', action='store', required=True)
    args = parser.parse_args()
    
    if(args.input_file):
        maker.process_file(args.input_file)
    else:
        maker.add_single_view(args.user_id, args.ad_id, args.time)


if __name__ == '__main__':
    main()



    
