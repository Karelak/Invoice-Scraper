import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
from tqdm import tqdm

def generate_random_invoice(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Generate random data
    invoice_number = random.randint(1000, 9999)
    booking_reference = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    booking_date = f"{random.randint(1, 28):02d}.{random.randint(1, 12):02d}.2024"
    first_names = ['JOHN', 'JANE', 'ALEX', 'EMILY', 'CHRIS', 'KATIE']  # Capitalized names
    last_names = ['DOE', 'SMITH', 'JOHNSON', 'BROWN', 'WILLIAMS', 'JONES']  # Capitalized names
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    passenger_name = random.choice(['Mr.', 'Ms.']) + ' ' + first_name + ' ' + last_name
    ticket_number = f"657-{random.randint(1000000000, 9999999999)}"
    flight_date = f"{random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])} {random.randint(1, 28):02d}/{random.randint(1, 12):02d}"
    dep_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
    arr_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
    dep_city = random.choice(['Riga', 'Tallinn', 'Vilnius'])
    arr_city = random.choice(['Berlin', 'Paris', 'London'])
    flight_num = f"BT{random.randint(100, 999)}"
    flight_class = random.choice(['Economy', 'Business'])
    fare = f"{random.uniform(50, 500):.2f}"
    taxes = f"{random.uniform(10, 100):.2f}"  # Fixed format specifier
    fuel_surcharge = f"{random.uniform(5, 50):.2f}"  # Fixed format specifier
    ticketing_service = f"{random.uniform(1, 10):.2f}"  # Fixed format specifier
    total = f"{float(fare) + float(taxes) + float(fuel_surcharge) + float(ticketing_service):.2f}"

    # Write data to PDF
    c.drawString(100, height - 50, f"Invoice number: {invoice_number}")
    c.drawString(100, height - 70, f"Booking reference: {booking_reference}")
    c.drawString(100, height - 90, f"Booking date: {booking_date}")
    c.drawString(100, height - 110, f"Passenger name: {passenger_name}")
    c.drawString(100, height - 130, f"{flight_date} {dep_time} {dep_city} ({dep_city[:3].upper()}) {arr_time} {arr_city} ({arr_city[:3].upper()}) {flight_num} {flight_class}")
    c.drawString(100, height - 150, f"Fare EUR {fare}")
    c.drawString(100, height - 170, f"Taxes EUR {taxes}")
    c.drawString(100, height - 190, f"Fuel surcharge * EUR {fuel_surcharge}")
    c.drawString(100, height - 210, f"Ticketing service ** EUR {ticketing_service}")
    c.drawString(100, height - 230, f"Total EUR {total}")

    c.save()

def generate_pdfs(folder, count):
    os.makedirs(folder, exist_ok=True)
    existing_files = len(os.listdir(folder))
    for i in tqdm(range(existing_files, existing_files + count), desc="Generating PDFs"):
        filename = os.path.join(folder, f"invoice_{i+1}.pdf")
        generate_random_invoice(filename)

if __name__ == "__main__":
    count = int(input("Enter the number of PDF invoices to generate: "))
    generate_pdfs("pdfs", count)  # Generate the specified number of sample PDF files in the pdfs folder
