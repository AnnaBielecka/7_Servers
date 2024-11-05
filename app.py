
from flask import Flask, request, jsonify

import pandas as pd

import csv
import sys
from collections import defaultdict
from datetime import datetime


app = Flask(__name__)


# Функція для фільтрації співробітників за місяцем та відділом

def filter_employees(month, department, date_field):
    # Завантажуємо дані з database.csv
    employees = []
    with open("database.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            employees.append(row)
    
    # Перевіряємо збіги з фільтрами
    filtered_employees = []
    for emp in employees:
        emp_date = datetime.strptime(emp[date_field], "%Y-%m-%d")  # Перетворюємо рядок дати у формат дати
        emp_month = emp_date.strftime("%B")  # Отримуємо місяць у форматі тексту ("April", "May" тощо)
        
        if emp["Department"] == department and emp_month.lower() == month.lower():
            filtered_employees.append({
                "name": emp["Name"],
                "date": emp_date.strftime("%b %d")  # Формат дати для виведення, наприклад "Apr 18"
            })
    
    return filtered_employees


# Ендпоінт для отримання днів народження
@app.route('/birthdays', methods=['GET'])
def get_birthdays():
    month = request.args.get('month')
    department = request.args.get('department')
    
    employees = filter_employees(month, department, 'Birth date')
    
    # Формуємо відповідь JSON
    return jsonify({
        "total": len(employees),
        "employees": employees
    })


# Ендпоінт для отримання річниць
@app.route('/anniversaries', methods=['GET'])
def get_anniversaries():
    month = request.args.get('month')
    department = request.args.get('department')
    
    employees = filter_employees(month, department, 'Hire date')
    
    # Формуємо відповідь JSON
    return jsonify({
        "total": len(employees),
        "employees": employees
    })


# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)