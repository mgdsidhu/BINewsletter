
import pandas as pd

def create_dashboard_tile(df, title):
    html_template = """
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="font-family: Arial, sans-serif;  margin: 0 auto; background-color: #f4f4f4;">
        <tr>
            <td style="padding: 20px;">
                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="border-bottom: 1px solid #e0e0e0;">
                            <h2 class="tileHeading">{title}</h2>
                            
                        </td>
                        <td style="padding: 20px; border-bottom: 1px solid #e0e0e0; text-align:right;">
                            <h5 style="margin: 0; color: #333333;">Period=yesterday</h5>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2" class="TileWrapper">
                            {content}
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2" style="padding: 10px; text-align:center; border-top: 1px solid #e0e0e0;">
                            <span style='color:#979797; font-size:13px;'>Please login to MiHub to see further details.</span> <br/>
                            <span style='color:#979797; font-size:13px;'>%Var : Difference of Actual vs Forecast.</span>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    """

    content = ""
    content += "<table cellpadding='0' cellspacing='0' border='0' width='100%' bgcolor='#ffffff' style='margin-bottom: 15px;'>"
    for index, row in df.iterrows():
        content += f"<tr> <td><div class='tileCon'>"
        content += f"<div style='text-align:center;'><span class='metricNameVal'>{row['metricNm_x']}</span></div>"
        content += f"<div style='text-align:center;'>  <span class='foreVal'>{'{:,}'.format(int(row['prevVal']))}</span> <span class='diffVal {row['className']}'>{"{:.1f}".format(row['ActualDiff'])}%</span><span class='actualVal'>{'{:,}'.format(int(row['actualVal']))}</span><span class='diffVal greyArrow'>{"{:.1f}".format(row['ForeDiff'])}%</span> <span class='foreVal greyLbl'>{'{:,}'.format(int(row['forecasted']))}</span></div>"
        content += f"<div style='text-align:left;'><span class='tileLblLast prevPerLbl'>Prev Period</span><span class='tileLblLast spacer20' >%Growth</span><span class='tileLblLast'>Actual</span><span class='greyLbl tileLblLast varLbl'>%Var</span><span class='greyLbl tileLblLast foreLbl' >Forecast</span></div>"
        content += f"</div></td></tr>"
    content += "</table>"
    
    return html_template.format(title=title, content=content)

