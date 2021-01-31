#!/usr/bin/env python

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import secrets
import argparse
import json
import sys


update_ad_gql = gql('''
mutation updateAd($id: String!, $width: Int, $height: Int, $color: String, $texts: [String!]) {
  updateAdById(input: {id: $id, adPatch: {width: $width, height: $height, color: $color}}) {
    ad {
      id
    }
  }
  insertAdTexts(input: {adId: $id, texts: $texts}) {
    clientMutationId
  }
}
''')

new_ad_gql = gql('''
mutation newAd($id: String!, $width: Int, $height: Int, $color: String, $texts: [String!]) {
  createAd(input: {ad: {id: $id, width: $width, height: $height, color: $color}}) {
    ad {
      id
    }
  }
  insertAdTexts(input: {adId: $id, texts: $texts}) {
    clientMutationId
  }
}
''')

class MakeAd:
    def __init__(self, url):
        # Select your transport with a defined url endpoint
        self.transport = AIOHTTPTransport(url=url)
        
        # Create a GraphQL client using the defined transport
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
        
        self.new_gql = new_ad_gql
        self.update_gql = update_ad_gql
        
    def update_ad(self, variables):
        self.client.execute(self.update_gql, variable_values=variables)
    
    def new_ad(self, variables):
        print(f'Creating new ad {variables["id"]}: {variables}')
        self.client.execute(self.new_gql, variable_values=variables)
    
    def create_or_update_packed(self, variables):
        if variables.get("id") is None:
            variables["id"] = secrets.token_hex(16)
            self.new_ad(variables)
        else:
            self.update_ad(variables)
    
    def create_or_update(self, ad_id=None, width=None, height=None, color=None, texts=None):
        variables = {}
        if ad_id is not None:
            variables["id"] = ad_id
        if width is not None:
            variables["width"] = width
        if height is not None:
            variables["height"] = height
        if color is not None:
            variables["color"] = color
        if texts is not None:
            variables["texts"] = texts
        
        if len(variables) == 0:
            print("No data specified")
            return
        
        self.create_or_update_packed(variables)
    
    def process_file(self, in_file):
        for line in in_file.readlines():
            if len(line) <= 1:
                continue
            if line.startswith('//'):
                continue
            line = json.loads(line)
            self.create_or_update_packed(line)
            


def main():
    try:
        maker = MakeAd("http://localhost:5000/graphql")
    except:
        print('Can\'t connect to GraphQL API')
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Load ad (or multiple ads from a file) into a database')
    parser.add_argument('--file', dest='input_file', action='store', type=open)
    
    parser.add_argument('--id', dest='ad_id', action='store')
    parser.add_argument('--width', dest='width', action='store', type=int)
    parser.add_argument('--height', dest='height', action='store', type=int)
    parser.add_argument('--color', dest='color', action='store')
    parser.add_argument('--texts', dest='texts', action='store', nargs='*')
    args = parser.parse_args()
    
    if(args.input_file):
        maker.process_file(args.input_file)
    else:
        maker.create_or_update(args.ad_id, args.width, args.height, args.color, args.texts)


if __name__ == '__main__':
    main()



    
