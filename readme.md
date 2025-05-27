

# Food Places Enrichment

A Python script to automatically enrich a CSV list of food and restaurant places with details fetched from the Google Maps API.

## Features

- Reads an input CSV containing place names, locations, and visited status.
- Uses the Google Maps Places API to fetch:
  - Formatted address
  - Phone number
  - Average rating
  - Price level
  - Website URL
  - Primary category (Google Places type)
  - Neighborhood or locality
  - Direct Google Maps place link
- Outputs an enriched CSV with all original columns plus enrichment fields.

## Prerequisites

- Python 3.8 or newer
- A Google Maps API key with Places API enabled

## Installation

1. Clone this repository or download the files:
   ```bash
   git clone <your-repo-url>
   cd food-python
   ```
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install required Python packages:
   ```bash
   pip install --upgrade pip
   pip install pandas googlemaps
   ```

## Configuration

1. Export your Google Maps API key as an environment variable:
   ```bash
   export GOOGLE_MAPS_API_KEY="YOUR_API_KEY"
   ```

## Usage

```bash
python enrich_places.py input.csv output.csv
```

- `input.csv` should be a CSV with at least the columns:
  - `Name` (place name)
  - `Location` (city or area for disambiguation)
  - `Visited` (True/False or blank)
- The script will create `output.csv` containing all original columns plus:
  - `Address`
  - `Phone`
  - `Rating`
  - `Price`
  - `Website`
  - `Category`
  - `Neighborhood`
  - `Google Maps Link`

## Example

```bash
python enrich_places.py food_places_input_full.csv food_places_enriched.csv
```

## License

This project is released under the MIT License.