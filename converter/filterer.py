import re
import csv
import os

def clean_passenger_name(full_name):
    # Remove Mr./Ms. prefix and clean up spaces
    name = re.sub(r'^(Mr\.|Ms\.)\s+', '', full_name.strip())
    # Split into first and last name
    parts = name.split()
    if len(parts) >= 2:
        return {'first_name': parts[0], 'last_name': ' '.join(parts[1:])}
    return {'first_name': name, 'last_name': ''}

def convert_date_format(weekday_date):
    """Convert 'Tue 01/07' to '01-07-2024'"""
    day, month = weekday_date.split()[1].split('/')
    return f"{day}-{month}-2024"  # Assuming all flights are in 2024

def parse_invoice_text(text):
    # Clean up any extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    data = {
        'invoice_number': re.search(r'Invoice number: (\d+)', text),
        'booking_reference': re.search(r'Booking reference: ([A-Z0-9]+)', text),
        'booking_date': re.search(r'Booking date: (\d{2}\.\d{2}\.\d{4})', text),
        
        # Extract passenger info including their ticket numbers
        'passengers': re.findall(r'((?:Mr\.|Ms\.)\s+[A-Z\s]+)\s+657-(\d+)', text),
        
        # Improved flight info matching
        'flight_info': re.findall(
            r'((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{2}/\d{2})\s+'
            r'(\d{2}:\d{2})\s+([^(]+)\(([^)]+)\)'
            r'\s*(\d{2}:\d{2})\s+([^(]+)\(([^)]+)\)'
            r'\s*(BT\d+)\s+([^,]+)', 
            text
        ),
        
        # Improved price matching
        'fare': re.search(r'Fare EUR\s*([\d.]+)', text),
        'taxes': re.search(r'Taxes EUR\s*([\d.]+)', text),
        'fuel_surcharge': re.search(r'Fuel surcharge \* EUR\s*([\d.]+)', text),
        'ticketing_service': re.search(r'Ticketing service \*\* EUR\s*([\d.]+)', text),
        'total': re.search(r'Total EUR\s*([\d.]+)', text)
    }

    # Create a list to hold all rows of data
    all_rows = []
    
    # Basic data that's same for all rows
    base_data = {
        'invoice_number': data['invoice_number'].group(1) if data['invoice_number'] else '',
        'booking_reference': data['booking_reference'].group(1) if data['booking_reference'] else '',
        'booking_date': data['booking_date'].group(1) if data['booking_date'] else '',
    }
    
    # Process passenger names
    if data['passengers']:
        passenger = clean_passenger_name(data['passengers'][0][0])  # Take first passenger's name
        base_data.update({
            'first_name': passenger['first_name'],
            'last_name': passenger['last_name']
        })
    else:
        base_data.update({'first_name': '', 'last_name': ''})

    # Process each flight as a separate row
    for i, flight in enumerate(data['flight_info']):
        row_data = base_data.copy()
        
        (date, dep_time, dep_city, dep_airport, 
         arr_time, arr_city, arr_airport, 
         flight_num, flight_class) = flight
        
        # Clean city names
        dep_city = dep_city.strip()
        arr_city = arr_city.strip()
        
        row_data.update({
            'date': convert_date_format(date),
            'departure_time': dep_time,
            'arrival_time': arr_time,
            'route': f"{dep_city}-{arr_city}",
        })
        
        # Add pricing only to the last flight
        if i == len(data['flight_info']) - 1:
            row_data.update({
                'fare': data['fare'].group(1) if data['fare'] else '0.00',
                'taxes': data['taxes'].group(1) if data['taxes'] else '0.00',
                'fuel_surcharge': data['fuel_surcharge'].group(1) if data['fuel_surcharge'] else '0.00',
                'ticketing_service': data['ticketing_service'].group(1) if data['ticketing_service'] else '0.00',
                'total': data['total'].group(1) if data['total'] else '0.00'
            })
        else:
            row_data.update({
                'fare': '',
                'taxes': '',
                'fuel_surcharge': '',
                'ticketing_service': '',
                'total': ''
            })
        
        all_rows.append(row_data)
    
    return all_rows

def save_to_csv(parsed_data_rows, csv_path):
    fieldnames = [
        'Invoice Number', 'Booking Reference', 'Booking Date',
        'First Name', 'Last Name', 'Date', 'Departure Time', 'Arrival Time', 
        'Route', 'Fare', 'Taxes', 'Fuel Surcharge', 'Ticketing Service', 'Total'
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in parsed_data_rows:
            writer.writerow({
                'Invoice Number': row['invoice_number'],
                'Booking Reference': row['booking_reference'],
                'Booking Date': row['booking_date'],
                'First Name': row['first_name'],
                'Last Name': row['last_name'],
                'Date': row['date'],
                'Departure Time': row['departure_time'],
                'Arrival Time': row['arrival_time'],
                'Route': row['route'],
                'Fare': row['fare'],
                'Taxes': row['taxes'],
                'Fuel Surcharge': row['fuel_surcharge'],
                'Ticketing Service': row['ticketing_service'],
                'Total': row['total']
            })
