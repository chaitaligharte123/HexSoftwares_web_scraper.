import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox

os.makedirs("output", exist_ok=True)

def scrape_website(url):
    data = []
    try:
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Error", f"Cannot reach website: {url}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            availability = book.find("p", class_="instock availability").text.strip()
            rating = book.p["class"][1]  # Example: rating
            data.append({
                "Title": title,
                "Price": price,
                "Availability": availability,
                "Rating": rating
            })

        return data
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def start_scraping():
    urls = url_entry.get("1.0", tk.END).strip().split("\n")
    all_data = []

    for url in urls:
        website_data = scrape_website(url)
        if website_data:
            all_data.extend(website_data)
            messagebox.showinfo("Info", f"Scraped {len(website_data)} items from {url}")

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("output/all_data.csv", index=False)
        df.to_excel("output/all_data.xlsx", index=False)
        messagebox.showinfo("Success", f"Scraping completed!\nCSV and Excel saved in output folder")

# GUI
root = tk.Tk()
root.title("Advanced Web Scraper")
root.geometry("600x400")

tk.Label(root, text="Enter URLs (one per line):").pack(pady=5)
url_entry = tk.Text(root, width=70, height=10)
url_entry.pack()

tk.Button(root, text="Start Scraping", command=start_scraping).pack(pady=10)
tk.Button(root, text="Clear", command=lambda: url_entry.delete("1.0", tk.END)).pack()

root.mainloop()
