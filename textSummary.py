import os
from google.cloud import bigquery
import google.generativeai as genai
import pandas as pd
import dbQry as dQ
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

def generate():
# Set up your Google Cloud credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GCP_JSON_PATH')
    genai.configure(api_key=os.getenv('BQ_API_KEY'))  
    client = bigquery.Client()

    query = dQ.summary

    query_job = client.query(query)
    results = query_job.result()
    df = pd.DataFrame(results)  # More efficient than the list comprehension

    # Create an HTML table
    # html_table = df.to_html(index=False , classes='data-table', border=0)
    ## This report analyzes the top 5 customers by total orders based on the following data:
    html_table = df.to_string(index=False )

    prompt = f"""
    {html_table}
    Please provide a concise summary to highlight it:
    1.  Key Insights Identify any prominent trends or patterns in business unit and seller order activity.
    2.  Top Performers Briefly describe the top 3 sellers based on order volume.
     ignore these sellers update 'STF', 'GEI','ALL','USA'
    """

    # Based on the following data from our top 5 seller by lots assigned orders:

    # {data_str}

    # Please generate a brief summary report highlighting key insights and recommendations. 
    # Include the following:
    # 1. An overview of the top performers
    # 2. Any notable patterns or trends
    # 3. Suggestions for customer engagement strategies


    model = genai.GenerativeModel('gemini-pro')

    generation_config = {
        "max_output_tokens": 250,
        "temperature": 1,
        "top_p": 0.95
    }

    # safety_settings = {
    #     generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    #     generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    #     generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    #     generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    # }

    response = model.generate_content(prompt,
        generation_config=generation_config
        # ,safety_settings=
        # stream=True
        ) 

    # HTML formatting 
    response_text_modified = response.text.replace("*", "")
    response_text = response_text_modified.replace("Top Performers", "<b>Top Performers </b>").replace("Key Insights", "<b>Key Insights </b>")
  
    nl = '\n'
    html = f"""
    <ul class='summaryList'>
        {''.join(f"<li>{line.strip()}</li>{nl}" for line in response_text.splitlines()).strip()}
    </ul>
    """

    # print(html.replace("<li></li>", ""))  
    return html.replace("<li></li>", "")

# generate()