#!/usr/bin/env python

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import secrets
import argparse
import json
import sys

update_user_gql = gql('''
mutation updateUser($uid: String!, $year: Int, $income: BigInt, $lat: Float, $lon: Float, $intr: [String!]) {
  updateUserById(
    input: {userPatch: {bornYear: $year, income: $income, lat: $lat, lon: $lon}, id: $uid}
  ) {
    clientMutationId
  }
  insertInterests(input: {uid: $uid, intr: $intr}) {
    clientMutationId
  }
}''')

new_user_gql = gql('''
mutation newUser($uid: String!, $year: Int, $income: BigInt, $lat: Float, $lon: Float, $intr: [String!]) {
  createUser(
    input: {user: {id: $uid, bornYear: $year, income: $income, lat: $lat, lon: $lon}}
  ) {
    clientMutationId
  }
  insertInterests(input: {uid: $uid, intr: $intr}) {
    clientMutationId
  }
}''')

class MakeUser:
    def __init__(self, url):
        # Select your transport with a defined url endpoint
        self.transport = AIOHTTPTransport(url=url)
        
        # Create a GraphQL client using the defined transport
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
        
        self.new_gql = new_user_gql
        self.update_gql = update_user_gql
        
    def update_user(self, variables):
        self.client.execute(self.update_gql, variable_values=variables)
    
    def new_user(self, variables):
        print(f'Creating new user {variables["uid"]}: {variables}')
        self.client.execute(self.new_gql, variable_values=variables)
    
    def create_or_update_packed(self, variables):
        if variables.get("uid") is None:
            variables["uid"] = secrets.token_hex(16)
            self.new_user(variables)
        else:
            self.update_user(variables)
    
    def create_or_update(self, uid=None, born=None, income=None, lat=None, lon=None, intr=None):
        variables = {}
        if uid is not None:
            variables["uid"] = uid
        if born is not None:
            variables["year"] = born
        if income is not None:
            variables["income"] = income
        if lat is not None:
            variables["lat"] = lat
        if lon is not None:
            variables["lon"] = lon
        if intr is not None:
            variables["intr"] = intr
        
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
        maker = MakeUser("http://localhost:5000/graphql")
    except:
        print('Can\'t connect to GraphQL API')
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Load user (or multiple users from a file) into a database')
    parser.add_argument('--file', dest='input_file', action='store', type=open)
    
    parser.add_argument('--uid', dest='uid', action='store')
    parser.add_argument('--year', dest='year', action='store', type=int)
    parser.add_argument('--income', dest='income', action='store')
    parser.add_argument('--lat', dest='lat', action='store', type=float)
    parser.add_argument('--lon', dest='lon', action='store', type=float)
    parser.add_argument('--intr', dest='intr', action='store', nargs='*')
    args = parser.parse_args()
    
    if(args.input_file):
        maker.process_file(args.input_file)
    else:
        maker.create_or_update(args.uid, args.year, args.income, args.lat, args.lon, args.intr)


if __name__ == '__main__':
    main()



    
