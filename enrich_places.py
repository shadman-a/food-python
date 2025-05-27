#!/usr/bin/env python3
"""
Auto-enrich food places CSV using Google Maps API.

Usage:
    pip install pandas googlemaps
    export GOOGLE_MAPS_API_KEY="YOUR_API_KEY"
    python enrich_places.py input.csv output.csv
"""

import os
import sys
import time
import pandas as pd
import googlemaps

def enrich_places(input_csv, output_csv, api_key_env='GOOGLE_MAPS_API_KEY'):
    # Load API key
    api_key = os.getenv(api_key_env)
    if not api_key:
        sys.exit(f"Error: Environment variable {api_key_env} not set.")
    gmaps = googlemaps.Client(key=api_key)

    # Read input CSV
    df = pd.read_csv(input_csv)

    # Ensure enrichment columns exist
    for col in ['Visited','Address','Phone','Rating','Price','Website','Category','Neighborhood','Google Maps Link']:
        if col not in df.columns:
            df[col] = ''

    # Iterate and enrich each row
    for idx, row in df.iterrows():
        query = f"{row['Name']} {row.get('Location','')}"
        try:
            # Perform a text search
            res = gmaps.places(query=query, language='en')
            results = res.get('results', [])
            if not results:
                print(f"[{idx}] No result for: {query}")
                continue

            place = results[0]
            pid = place['place_id']

            # Fetch detailed info
            details = gmaps.place(
                place_id=pid,
                fields=[
                    'formatted_address',
                    'formatted_phone_number',
                    'rating',
                    'price_level',
                    'website',
                    'types',
                    'address_components'
                ],
                language='en'
            ).get('result', {})

            # Write details back into DataFrame
            df.at[idx, 'Address'] = details.get('formatted_address','')
            df.at[idx, 'Phone']   = details.get('formatted_phone_number','')
            df.at[idx, 'Rating']  = details.get('rating','')
            price_lvl = details.get('price_level')
            df.at[idx, 'Price']   = '$' * price_lvl if price_lvl is not None else ''
            df.at[idx, 'Website'] = details.get('website','')

            # Category: first Google type
            types = details.get('types',[])
            df.at[idx, 'Category'] = types[0] if types else ''

            # Neighborhood: prefer neighborhood, fallback to locality
            nb = ''
            for comp in details.get('address_components',[]):
                if 'neighborhood' in comp['types']:
                    nb = comp['long_name']
                    break
                if 'locality' in comp['types']:
                    nb = comp['long_name']
            df.at[idx, 'Neighborhood'] = nb

            # Google Maps link by place_id
            df.at[idx, 'Google Maps Link'] = f"https://www.google.com/maps/place/?q=place_id:{pid}"

        except Exception as e:
            print(f"[{idx}] Error for {query}: {e}")

        # small delay to avoid rate limits
        time.sleep(0.1)

    # Save enriched output
    df.to_csv(output_csv, index=False)
    print(f"✅ Enriched data saved to: {output_csv}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python enrich_places.py input.csv output.csv")
    else:
        enrich_places(sys.argv[1], sys.argv[2])