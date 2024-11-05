import requests
import sys

def fetch_report(month: str, department: str):
    url = f"http://localhost:5000/birthdays?month={month}&department={department}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"Report for {department} department for {month.capitalize()} fetched.")
        print(f"Total: {data['total']}")
        print("Employees:")
        
        for employee in data['employees']:
            date = employee['birthday']
            name = employee['name']
            print(f"- {date}, {name}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching report: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fetch_report.py <month> <department>")
    else:
        month = sys.argv[1]
        department = sys.argv[2]
        fetch_report(month, department)