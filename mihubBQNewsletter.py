
import os
from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
import base64

# Set up BigQuery client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/anaggarwal/Downloads/Python/cprtprsvc-dataapps-rptapp-bq.json'
client = bigquery.Client()

def fetch_data_from_bigquery(query):
    query_job = client.query(query)
    return query_job.result().to_dataframe()

def create_chart(data, x_column, y_column, title):
    plt.figure(figsize=(6,6))
    sns.set_style("whitegrid")
    sns.barplot(x=x_column, y=y_column, data=data, hue=x_column, palette="Blues_d")
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_column.capitalize(), fontsize=12)
    plt.ylabel(y_column.capitalize(), fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save to BytesIO object
    from io import BytesIO
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    return img_buffer

def send_executive_summary_newsletter(sender_email, sender_password, recipient_email, subject, executive_summary, df, chart):

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_email)
    msg['Subject'] = subject

    # Convert DataFrame to HTML table
    df_html = df.to_html(index=False , classes='data-table', border=0)

    # Encode chart image
    chart_base64 = base64.b64encode(chart.getvalue()).decode()

    email_body= f"""
        <html>
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
                body {{
                    font-family: 'Roboto', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #4a90e2;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 20px;
                }}
                h1, h2 {{
                    color: #2c3e50;
                    margin-top: 0;
                }}
                .summary {{
                    background-color: #e8f4fd;
                    border-left: 4px solid #4a90e2;
                    padding: 15px;
                    margin-bottom: 20px;
                    border-radius: 4px;
                }}
                .summary h2 {{
                    margin-top: 0;
                    color: #4a90e2;
                }}
                .chart-container {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .chart-container img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 4px;
                }}
                .data-table {{
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0;
                }}
                .data-table th, .data-table td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #e0e0e0;
                }}
                .data-table th {{
                    background-color: #4a90e2;
                    color: white;
                    font-weight: bold;
                }}
                .data-table tr:last-child td {{
                    border-bottom: none;
                }}
                .footer {{
                    background-color: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 10px;
                    font-size: 0.8em;
                    border-bottom-left-radius: 8px;
                    border-bottom-right-radius: 8px;
                }}
                @media only screen and (max-width: 600px) {{
                    body {{
                        padding: 10px;
                    }}
                    .header {{
                        padding: 15px;
                    }}
                    .content {{
                        padding: 15px;
                    }}
                }}
            </style>
        </head>
            <body>
            <div class="container">
               <div class="header">
                <h1>Executive Summary Newsletter</h1>
            </div>
            <div class="content">
              <div class="summary">
                <h2>{weekNumber} Week's Highlights</h2>
                <p>{executive_summary}</p>
            </div>
            <h2>Data Insights</h2>
            <div class="chart-container">
                <img src="data:image/png;base64,{chart_base64}" alt="Data Chart">
            </div>
            <h2>Detail Data</h2>
                {df_html}
                <div class="footer">
                    <p>Thank you for your attention to this important update.</p>
                    <p>For any questions, please contact the analytics team.</p>
                    <br/>
                    <br/>

                    <p> Regards,</p>
                    <p> Data & AI Team</p>
                </div>
            </div>
          </body>
        </html>
        """

    msg.attach(MIMEText(email_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email newsletter sent successfully to {recipient_email}!")
    except Exception as e:
        print(f"An error occurred while sending to {recipient_email}: {e}")

    
sender_email = <<EMAIL ID>>
sender_password = # Use an app password for Gmail
recipient_email =[<<EMAIL ID>>,<<EMAIL ID>>]

subject = "Weekly Executive Summary with Data Insights"

# Fetch data from BigQuery
query = """
select date as MonthYear,LotsSold from (	
select 
		 FORMAT_DATE('%d-%b',inv_dt) as date,
		 inv_dt,
		ifnull(count(lot_nbr),0) as LotsSold
from
	`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops_uat
where
	inv_dt between '2024-07-05' and '2024-07-15'
	and abnormal_close_type = ''
group by 
	1,2
order by inv_dt )
"""
df = fetch_data_from_bigquery(query)

# Create chart
chart = create_chart(df, 'MonthYear', 'LotsSold', 'Lots Sold Over Time')

weekstarting= datetime.now()
weekending =weekstarting + timedelta(6)
weekstart = weekstarting.strftime("%B %d, %Y")
weekend=weekending.strftime("%B %d, %Y")

weekstartLbl = weekstarting.strftime("%B %d")
weekendLbl=weekending.strftime("%B %d")
weekNumber = str(weekstartLbl) +' - '+ str(weekendLbl)

executive_summary = f"""
<ul>
    <li>This week's {weekNumber} update:</li>
    <li>Lots Sold data for the past <strong>{len(df)}</strong> days has been analyzed.</li>
    <li>The highest Lots Sold was <strong>{df['LotsSold'].max()}</strong>.</li>
    <li>The average daily Lots Sold was <strong>{df['LotsSold'].mean():.2f}</strong>.</li>
    <li>Observed a <strong> {'+' if df['LotsSold'].iloc[-1] > df['LotsSold'].iloc[0] else '-'}{abs(df['LotsSold'].iloc[-1] - df['LotsSold'].iloc[0]) / df['LotsSold'].iloc[0] * 100:.1f}% </strong> change from start to end of the period.</li>
    <li>Please refer to the chart and table below for more details.</li>
</ul>
"""

send_executive_summary_newsletter(sender_email, sender_password, recipient_email, subject, executive_summary, df, chart)

print("Simulated email content:")
print(f"Subject: {subject}")
print(f"Recipients: {', '.join(recipient_email)}")
