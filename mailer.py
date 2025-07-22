import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import base64
import htmlEmbed as ht
import utils as ut
import os

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

def encode_image(image_path):
    """Encode image to Base64"""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def send_executive_summary_newsletter(sender_email, sender_password, recipient_email, subject, executive_summary, df,dfTile, chart):

    # msg = MIMEMultipart()
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_email)
    msg['Subject'] = subject

    # Convert DataFrame to HTML table
    df_html = df.to_html(index=False , classes='data-table', border=0)
    df_html2 = dfTile.to_html(index=False , classes='data-table', border=0)

    image_path = 'copartlogo.png'
    encoded_image = encode_image(image_path)


    dashboard_tile_html = ht.create_dashboard_tile(dfTile, "Executive Metrics")
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
                    padding: 10px;
                    background-color: #f4f4f4;
                    border-radius:10px;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #4a90e2;
                    background:linear-gradient(to right, #1C1E21, #0935A5);
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
                    background-color: #fff9ec;
                    border-left: 4px solid #FFB838;
                    padding: 15px;
                    margin-bottom: 5px;
                    border-radius: 4px;
                }}
                .summary h2 {{
                    margin-top: 0;
                    color: #FFB838;
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
                .tileCon{{
                    border-radius:7px; 
                    border:1px solid #cacaca; 
                    margin:10px 0;
                }}
                .metricNameVal{{
                    font-size:14px; 
                    font-weight:bold;
                }}
                .foreVal{{
                    font-size:18px; 
                    right:10px; 
                    position:relative;
                }}
                .actualVal{{
                    font-size:18px; 
                }}
                .diffVal{{
                    margin: 0 20px;
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
                .tileHeading{{
                    margin: 0; 
                    color: #333333; 
                    font-size: 20px;
                    padding: 20px;
                }}
                .summaryList li{{
                    text-decoration: none;
                    list-style: none;
                    padding: 5px;
                    border-bottom: 1px solid #d8d8d8;

                }}
                .summaryList{{
                    padding-left: 5px;
                }}
                .greyLbl{{
                    color: #767676;
                }}
                .greyArrow{{
                        border: 1px dashed #a9aaa9;
                        border-radius: 10px;
                        padding: 4px;
                        background: #efefef;
                        font-size: 11px;
                        color: #767676;
                }}
                .greenArrow {{
                    border: 1px solid #52ab52;
                    border-radius: 10px;
                    padding: 4px;
                    background: #f1fff1;
                    font-size: 11px;
                    color: #52ab52;
                }}
                .redArrow {{
                    font-size: 11px;
                    color: #d13535;
                    border: 1px solid #d13535;
                    border-radius: 10px;
                    padding: 4px;
                    background: #fff2f2;
                }}
                .footer {{
                    background-color: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 7px 0;
                    font-size: 0.8em;
                    border-bottom-left-radius: 8px;
                    border-bottom-right-radius: 8px;
                }}
                .logoWrapper{{
                    width:150px;
                    height:50px;
                }}
                .headingTitle{{
                    color:#ffffff;
                    margin: 0px 0 8px 0 !important;
                }}
                .TileWrapper{{
                    padding: 20px 60px;
                }}
                .tileLblLast{{
                    font-size:12px;
                }}
                .spacer20{{
                    margin:0 20px;
                }}
                .prevPerLbl{{
                    margin-left: 30px;
                }}
                .varLbl{{
                    margin: 0 30px;
                }}    
                .foreLbl{{
                    margin-left: 10px;
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
                    .foreVal,.actualVal{{
                        font-size:12px; 
                    }}
                    .diffVal{{
                        margin: 0 5px;
                        font-size:11px; 
                    }}
                    .TileWrapper{{
                        padding: 20px 20px;
                     }}
                     .tileLblLast{{
                        font-size:11px;
                    }}
                    .spacer20{{
                        margin:0 5px;
                    }}
                    .prevPerLbl{{
                        margin-left: 2px;
                    }}
                    .varLbl{{
                        margin: 0 10px;
                    }} 
                    .foreLbl{{
                        margin-left: 2px;
                    }}
                    .tileHeading{{
                        font-size: 14px;
                        padding: 0 5px;
                    }}
                    .headingTitle{{
                        font-size:14px
                    }}
                    .logoWrapper{{
                        width:115px;
                        height:50px;
                    }}
                }}
            </style>
        </head>
            <body>
            <div class="container">
               <div class="header">
                <table style="border: none; width:100%;">
                    <tr>
                        <td>
                            <div> <img src="data:image/png;base64,{encoded_image}"  alt="Logo" class="logoWrapper" ></div>
                        </td>
                        <td colspan='2' style='text-align: center;'>
                            <h2 class='headingTitle'>Weekly Business Buzzworthy</h2>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="content">
              <div class="summary">
                <h2>{ut.weekendDate()} Week's Highlights</h2>
                <p>{executive_summary}</p>
            </div>
            
                <span>&nbsp;</span>
                <div>
                    {dashboard_tile_html}
                </div>

                <h2>Data Insights</h2>
                <div class="chart-container">
                    <img src="data:image/png;base64,{chart_base64}" alt="Data Chart">
                </div>

                <div style='font-size:11px; color:#a1a1a1; margin-top:10px;'>
                    Disclaimer: You have received this mail because you are registered user on MiHub. This is a system generated email, please don't reply to this message.If you do not want to receive this mailer, Please contact us.
                </div>

            </div>
            <div class="footer">
                <p>Thank you for your attention to this important update.<br/>
                    For any questions, please contact the analytics team.</p>
                <p> Regards,<br/>
                    Data & AI Team</p>
            </div>
          </body>
        </html>
        """

    msg.attach(MIMEText(email_body, 'html'))

    try:
        with smtplib.SMTP_SSL(os.getenv('SMTP_CLIENT'), os.getenv('SMTP_PORT')) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email newsletter sent successfully to {recipient_email}!")
    except Exception as e:
        print(f"An error occurred while sending to {recipient_email}: {e}")


sender_email = os.getenv('FROM_EMAIL')
#recipient_email =["ankit.aggarwal@copart.com","hardik.bhavsar@copart.com"]
recipient_email =["ankit.aggarwal@copart.com"]
subject = f"Copart Weekly Business Buzzworthy for {ut.weekendDate()}"
