# 📈 CryptoCurrency ETL & Email Automation Project 🚀
---

## 📘 Project Overview

This is a complete **ETL (Extract-Transform-Load)** pipeline designed to run daily, written entirely in Python. It pulls **live crypto market data**, processes the data to extract meaningful insights, and sends an **HTML-formatted email** with the results — all through a **SendGrid email integration**.

The project answers the question:  
**"Which are the best and worst performing cryptocurrencies in the last 24 hours?"**

---
## 🚀 Features

- ✅ Fully automated ETL pipeline
- 📡 API integration with real-time data
- 📈 Generates insights: Top gainers and losers in 24H
- 💾 Saves complete report to CSV
- ✉️ Sends an email
- 📅 Ideal for daily job via cron/schedule

---

## 🛠️ Tech Stack

- **Python**: `pandas`, `requests`, `datetime`, `os`, `dotenv`
- **SendGrid** for email delivery (free tier)
- **HTML/CSS** for formatted email body
- **CoinMarketCap API** for cryptocurrency data
- **schedule / cron** (optional) for automation

---
## 🔄 ETL Workflow Explained

### 🟠 Extract

- We use the [CoinMarketCap API](https://coinmarketcap.com/api/) to extract live cryptocurrency data.
- The script sends an HTTP request using the `requests` library with proper headers including the **API key**.
- Response is parsed as a JSON object.

### 🔵 Transform

- The JSON is normalized using `pandas.json_normalize()` to create a structured DataFrame.
- We select specific relevant columns such as:
  - `name`
  - `symbol`
  - `cmc_rank`
  - `quote.USD.price`
  - `quote.USD.percent_change_24h`
  - `quote.USD.market_cap`
- Data is **sorted** based on 24-hour percentage change:
  - Top 10 gainers → `nlargest(10, 'percent_change_24h')`
  - Top 10 losers → `nsmallest(10, 'percent_change_24h')`
- Final DataFrame of all cryptocurrencies (200+) is exported to a `.csv` file.

### 🟢 Load

- A visually formatted **HTML email** is generated:
  - It includes a stylized table for top 10 gainers and losers.
  - Email also includes a brief message and footer.
- Email is sent using the **SendGrid API** with:
  - HTML content
  - Optional CSV file attached
- Email is delivered directly to the recipient’s inbox.

---

## 📧 Sample Email Output

📬 Below is a sample layout of the email (with table formatting):

> _(Attach this image in your repo)_

![Email Screenshot](assets/email_screenshot.png)

---

## 📁 Output Files

📁 Files generated after running the script:

- `crypto_report_<date>.csv` — full data of 200+ currencies
- HTML table summary in the email body

> _(Attach this image in your repo)_

![image](https://github.com/user-attachments/assets/37be5dd3-6bc7-4dc3-928f-b2fe1b59f83b)


---



## 📂 Folder Structure

