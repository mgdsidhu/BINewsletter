# import pandas as pd
import dataManipulation as fd
import charts as cc
import mailer as sml
import dbQry as dQ


# Create chart
chart = cc.create_chart(dQ.df, 'seller', 'Lots Assigned', 'Last 7 Days Trend of Lots Assigned by Sellers')

print("Simulated email content:")
print(f"Subject: {sml.subject}")
print(f"Recipients: {', '.join(sml.recipient_email)}")

if __name__ == '__main__':
    sml.send_executive_summary_newsletter(sml.sender_email, fd.sender_password, sml.recipient_email, sml.subject, dQ.executive_summary, dQ.df,dQ.dfTile, chart)