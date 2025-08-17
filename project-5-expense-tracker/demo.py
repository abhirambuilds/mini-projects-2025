#!/usr/bin/env python3
"""
Demo script for Expense Tracker
This script demonstrates the application's features by adding sample transactions
reflecting a typical lifestyle for 1 year.
"""

import csv
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Create sample transaction data for demonstration"""
    
    # Sample transactions with realistic data
    demo_transactions = []
    
    # Generate 1 year of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    current_date = start_date
    monthly_salary = 50000
    
    while current_date <= end_date:
        # Add monthly salary on the 1st of each month
        if current_date.day == 1:
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": "Monthly Salary",
                "amount": monthly_salary,
                "category": "Salary Income",
                "type": "Income"
            })
            
            # Add some side income (random)
            if current_date.month % 3 == 0:  # Every 3rd month
                side_income = 5000 + (current_date.month * 1000)  # Varies by month
                demo_transactions.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "description": "Freelance Project",
                    "amount": side_income,
                    "category": "Side Income",
                    "type": "Income"
                })
        
        # Add regular monthly expenses
        if current_date.day == 1:  # Rent on 1st
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": "House Rent",
                "amount": 15000,
                "category": "Rent",
                "type": "Expense"
            })
        
        if current_date.day == 5:  # Electricity bill
            electricity_amount = 2000 + (current_date.month * 100)  # Varies by month
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": "Electricity Bill",
                "amount": electricity_amount,
                "category": "Electricity",
                "type": "Expense"
            })
        
        if current_date.day == 10:  # School fees
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": "School Fees",
                "amount": 8000,
                "category": "School Fees",
                "type": "Expense"
            })
        
        if current_date.day == 15:  # Groceries
            grocery_amount = 3000 + (current_date.month * 200)  # Varies by month
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": "Monthly Groceries",
                "amount": grocery_amount,
                "category": "Groceries",
                "type": "Expense"
            })
        
        # Add some random daily expenses
        if current_date.day % 3 == 0:  # Every 3rd day
            expense_types = [
                ("Travel", 200, 800),
                ("Entertainment", 500, 2000),
                ("Shopping", 1000, 5000),
                ("Healthcare", 300, 1500),
                ("Miscellaneous", 100, 500)
            ]
            
            expense_type, min_amount, max_amount = random.choice(expense_types)
            amount = random.randint(min_amount, max_amount)
            
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": f"Daily {expense_type}",
                "amount": amount,
                "category": expense_type,
                "type": "Expense"
            })
        
        # Add transport expenses
        if current_date.day % 2 == 0:  # Every 2nd day
            transport_amount = random.randint(100, 500)
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": "Daily Transport",
                "amount": transport_amount,
                "category": "Transport",
                "type": "Expense"
            })
        
        # Add some savings
        if current_date.day == 25:  # Savings on 25th
            savings_amount = random.randint(2000, 5000)
            demo_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "description": "Monthly Savings",
                "amount": savings_amount,
                "category": "Savings",
                "type": "Expense"
            })
        
        current_date += timedelta(days=1)
    
    return demo_transactions

def save_demo_data(filename="transactions.csv"):
    """Save demo data to CSV file"""
    
    demo_transactions = create_demo_data()
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["date", "description", "amount", "category", "type"])
            writer.writeheader()
            writer.writerows(demo_transactions)
        
        print(f"✅ Demo data saved to {filename}")
        print(f"📊 Total transactions: {len(demo_transactions)}")
        
        # Calculate summary
        total_income = sum(t["amount"] for t in demo_transactions if t["type"] == "Income")
        total_expenses = sum(t["amount"] for t in demo_transactions if t["type"] == "Expense")
        balance = total_income - total_expenses
        
        print(f"💰 Total Income: ₹{total_income:,.2f}")
        print(f"💸 Total Expenses: ₹{total_expenses:,.2f}")
        print(f"💵 Balance: ₹{balance:,.2f}")
        
        # Category breakdown for expenses
        print("\n📈 Expense Breakdown by Category:")
        category_totals = {}
        for transaction in demo_transactions:
            if transaction["type"] == "Expense":
                category = transaction["category"]
                amount = transaction["amount"]
                category_totals[category] = category_totals.get(category, 0) + amount
        
        for category, total in sorted(category_totals.items()):
            percentage = (total / total_expenses) * 100
            print(f"  {category}: ₹{total:,.2f} ({percentage:.1f}%)")
        
        # Monthly breakdown
        print("\n📅 Monthly Breakdown:")
        monthly_data = {}
        for transaction in demo_transactions:
            date_obj = datetime.strptime(transaction["date"], "%Y-%m-%d")
            month_key = f"{date_obj.year}-{date_obj.month:02d}"
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {"income": 0, "expenses": 0}
            
            if transaction["type"] == "Income":
                monthly_data[month_key]["income"] += transaction["amount"]
            else:
                monthly_data[month_key]["expenses"] += transaction["amount"]
        
        for month in sorted(monthly_data.keys()):
            month_name = datetime.strptime(month, "%Y-%m").strftime("%B %Y")
            income = monthly_data[month]["income"]
            expenses = monthly_data[month]["expenses"]
            balance = income - expenses
            print(f"  {month_name}: Income ₹{income:,.2f}, Expenses ₹{expenses:,.2f}, Balance ₹{balance:,.2f}")
            
    except Exception as e:
        print(f"❌ Error saving demo data: {str(e)}")

def main():
    """Main function to run the demo"""
    print("🎯 Expense Tracker - Demo Data Generator")
    print("=" * 60)
    print("Generating 1 year of realistic sample data...")
    print("Includes monthly salary (₹50,000), rent, bills, groceries, and daily expenses.")
    print("=" * 60)
    
    # Create and save demo data
    save_demo_data()
    
    print("\n🚀 To run the Expense Tracker application:")
    print("   python main.py")
    print("\n📖 For more information, see README.md")
    print("\n💡 Features included:")
    print("   • Rupee (₹) currency")
    print("   • Monthly salary income")
    print("   • Realistic expense categories")
    print("   • 1 year of sample data")
    print("   • Pie chart and bar chart visualizations")

if __name__ == "__main__":
    main()
