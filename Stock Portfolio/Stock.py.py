"""
Stock Portfolio Tracker
------------------------
A simple console application that calculates the total value of a user's
stock portfolio using a hardcoded set of stock prices, and optionally saves
a summary report to a .txt or .csv file.

Key Concepts Used: dictionary, input/output, basic arithmetic, file handling
"""

import csv
import os
from datetime import datetime

# ----------------------------- Constants -----------------------------

STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "AMZN": 130.00,
    "MSFT": 310.00,
    "NFLX": 425.00,
    "META": 300.00,
}

DIVIDER = "-" * 52


# ----------------------------- Display Helpers -----------------------------

def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 52)
    print(title.center(52))
    print("=" * 52)


def print_available_stocks():
    """Display all available stock symbols and their current prices."""
    print_header("AVAILABLE STOCKS")
    print(f"{'Symbol':<10}{'Price (USD)':>15}")
    print(DIVIDER)
    for symbol, price in STOCK_PRICES.items():
        print(f"{symbol:<10}{price:>15,.2f}")
    print(DIVIDER)


def print_portfolio_table(portfolio):
    """Display the user's portfolio holdings in a formatted table."""
    print_header("YOUR PORTFOLIO")
    print(f"{'Symbol':<10}{'Quantity':>10}{'Price':>12}{'Subtotal':>18}")
    print(DIVIDER)

    total = 0.0
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        subtotal = price * quantity
        total += subtotal
        print(f"{symbol:<10}{quantity:>10}{price:>12,.2f}{subtotal:>18,.2f}")

    print(DIVIDER)
    print(f"{'TOTAL INVESTMENT VALUE':<32}{total:>20,.2f}")
    print(DIVIDER)
    return total


# ----------------------------- Input Helpers -----------------------------

def prompt_for_symbol():
    """
    Prompt the user for a stock symbol.
    Returns the validated, uppercase symbol, or None if the user wants to stop.
    """
    while True:
        raw = input("\nEnter stock symbol (or 'done' to finish): ").strip().upper()

        if raw == "DONE":
            return None

        if not raw:
            print("Invalid input: symbol cannot be empty.")
            continue

        if raw == "LIST":
            print_available_stocks()
            continue

        if raw not in STOCK_PRICES:
            print(f"'{raw}' is not in the available stock list. "
                  f"Type 'list' to see available symbols.")
            continue

        return raw


def prompt_for_quantity(symbol):
    """Prompt the user for a valid positive integer quantity for a given symbol."""
    while True:
        raw = input(f"Enter quantity of {symbol} shares: ").strip()

        try:
            quantity = int(raw)
        except ValueError:
            print("Invalid input: please enter a whole number.")
            continue

        if quantity <= 0:
            print("Invalid input: quantity must be greater than zero.")
            continue

        return quantity


def build_portfolio():
    """
    Interactively build a portfolio dictionary of {symbol: quantity}.
    If a symbol is entered more than once, quantities are combined.
    """
    portfolio = {}

    print_available_stocks()
    print("\nEnter your stock holdings below.")
    print("Type 'list' at any prompt to see available stocks again.")

    while True:
        symbol = prompt_for_symbol()
        if symbol is None:
            break

        quantity = prompt_for_quantity(symbol)
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"Added: {quantity} share(s) of {symbol}.")

    return portfolio


def prompt_save_choice():
    """Ask the user whether and how they want to save the report."""
    while True:
        choice = input(
            "\nWould you like to save this report? (txt / csv / no): "
        ).strip().lower()
        if choice in ("txt", "csv", "no"):
            return choice
        print("Invalid input: please enter 'txt', 'csv', or 'no'.")


# ----------------------------- File Handling -----------------------------

def save_as_txt(portfolio, total, filename="portfolio_report.txt"):
    """Save the portfolio summary to a plain text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("STOCK PORTFOLIO REPORT\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("=" * 52 + "\n")
        file.write(f"{'Symbol':<10}{'Quantity':>10}{'Price':>12}{'Subtotal':>18}\n")
        file.write("-" * 52 + "\n")

        for symbol, quantity in portfolio.items():
            price = STOCK_PRICES[symbol]
            subtotal = price * quantity
            file.write(f"{symbol:<10}{quantity:>10}{price:>12,.2f}{subtotal:>18,.2f}\n")

        file.write("-" * 52 + "\n")
        file.write(f"{'TOTAL INVESTMENT VALUE':<32}{total:>20,.2f}\n")

    return os.path.abspath(filename)


def save_as_csv(portfolio, total, filename="portfolio_report.csv"):
    """Save the portfolio summary to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Symbol", "Quantity", "Price (USD)", "Subtotal (USD)"])

        for symbol, quantity in portfolio.items():
            price = STOCK_PRICES[symbol]
            subtotal = price * quantity
            writer.writerow([symbol, quantity, f"{price:.2f}", f"{subtotal:.2f}"])

        writer.writerow([])
        writer.writerow(["", "", "TOTAL", f"{total:.2f}"])

    return os.path.abspath(filename)


# ----------------------------- Main Program -----------------------------

def main():
    print_header("STOCK PORTFOLIO TRACKER")

    portfolio = build_portfolio()

    if not portfolio:
        print("\nNo stocks were entered. Exiting program.")
        return

    total = print_portfolio_table(portfolio)

    save_choice = prompt_save_choice()
    if save_choice == "txt":
        path = save_as_txt(portfolio, total)
        print(f"\nReport saved to: {path}")
    elif save_choice == "csv":
        path = save_as_csv(portfolio, total)
        print(f"\nReport saved to: {path}")
    else:
        print("\nReport was not saved.")

    print("\nThank you for using the Stock Portfolio Tracker!")


if __name__ == "__main__":
    main()