import dataManipulation as fd
import dbQry as dQ
import textSummary as ts
import pandas as pd

# def _conditions1(row):    
#     if (row["actualVal"] -row["prevVal"]) > 0:
#         className='greenArrow'
#     else: className = 'redArrow'
#     return className

query = """
select 
		seller_parent_company as seller,
        seller_parent_company_long_name as sellerlong,
		ifnull(count(lot_nbr),0) as `Lots Assigned`
from
	`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
where
	assg_dt between DATE_SUB(current_date(),INTERVAL 7 DAY) and current_date()
group by 
	1,2
order by 3 desc
limit 10 
"""
query2= """
select
	d.metric_id,
	d.metric_disp_nm as metric_nm,
	ifnull(round(metric_forecast_value,0),0) as forecasted
from
	cprtpr-dataplatform-sp1.usmart.us_daily_cntry_anomalies mv inner join cprtpr-dataplatform-sp1.usmart.dim_anomaly_metrics d 
	on mv.metric_id=d.metric_id
where
	mv.metric_id in (1, 2, 3, 4, 5)
	and country_cd = 'USA'
	and model_name = 'ARIMA_PLUS'
	and (case when extract(DAYOFWEEK from current_date())=2
                   then metric_date=current_date()-3
            else metric_date=current_date()-1
    	end)
group by 
	all
order by 1

"""
query3 ="""
select 
		FORMAT_DATE('%d-%b',assg_dt) as monthYear,
		assg_dt,
		ifnull(count(lot_nbr),0) as lotsAssigned
from
	`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
where
	assg_dt between DATE_SUB(current_date(),INTERVAL 7 DAY) and current_date()-1
group by 
	all
order by 2

"""
currPeriod="""
select
	prevPeriod as prevPeriod,
	metricNm as metricNm,
	metric_id as metric_id,
	sum(metricVal) as actualVal
from
	(
	select
		assg_dt as prevPeriod,
		'Lots Assigned' as metricNm,
		1 as metric_id,
		ifnull(count(lot_nbr),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		 (case when extract(DAYOFWEEK from current_date())=2
                   then assg_dt=current_date()-3
            else assg_dt=current_date()-1
    	end)
	group by 
		all
UNION all
	select
		cfr_clear_dt as prevPeriod,
		'Lots Cleared' as metricNm,
		2 as metric_id,
		ifnull(sum(lots_cleared),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		 (case when extract(DAYOFWEEK from current_date())=2
                   then cfr_clear_dt=current_date()-3
            else cfr_clear_dt=current_date()-1
    	end)
	group by 
		all
UNION all
	select
		pkup_dt as prevPeriod,
		'Lots Picked Up' as metricNm,
		3 as metric_id,
		ifnull(sum(pick_up_same_day_perc),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		 (case when extract(DAYOFWEEK from current_date())=2
                   then pkup_dt=current_date()-3
            else pkup_dt=current_date()-1
    	end)
		and pkup_req_flag = 'Y'
	group by 
		all
UNION all
	select
		inv_dt as prevPeriod,
		'Lots Sold' as metricNm,
		4 as metric_id,
		ifnull(count(lot_nbr),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		(case when extract(DAYOFWEEK from current_date())=2
                   then inv_dt=current_date()-3
            else inv_dt=current_date()-1
    	end)
		and abnormal_close_type = ''
	group by 
		all
UNION all
	select
		inv_dt as prevPeriod,
		'Average Sale Price' as metricNm,
		5 as metric_id,
		ifnull(Round(safe_divide(sum(high_bid_amt), count(lot_nbr)), 0),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		(case when extract(DAYOFWEEK from current_date())=2
                   then inv_dt=current_date()-3
            else inv_dt=current_date()-1
    	end)
		and abnormal_close_type = ''
	group by 
		all
		)
	group by
		all
	order by 
		metric_id

"""

PrevPeriod = """
select
	prevPeriod as prevPeriod,
	metricNm as metricNm,
	metric_id as metric_id,
	sum(metricVal) as prevVal
from
	(
	select
		assg_dt as prevPeriod,
		'Lots Assigned' as metricNm,
		1 as metric_id,
		ifnull(count(lot_nbr),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
        (case when extract(DAYOFWEEK from current_date())=2
                   then assg_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-3,INTERVAL 12 Month),WEEK(MONDAY))
            else assg_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-1,INTERVAL 12 Month),WEEK(MONDAY))
    	end)
	group by 
		all
UNION all
	select
		cfr_clear_dt as prevPeriod,
		'Lots Cleared' as metricNm,
		2 as metric_id,
		ifnull(sum(lots_cleared),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		 (case when extract(DAYOFWEEK from current_date())=2
                   then cfr_clear_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-3,INTERVAL 12 Month),WEEK(MONDAY))
            else cfr_clear_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-1,INTERVAL 12 Month),WEEK(MONDAY))
    	end)
	group by 
		all
UNION all
	select
		pkup_dt as prevPeriod,
		'Lots Picked Up' as metricNm,
		3 as metric_id,
		ifnull(sum(pick_up_same_day_perc),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		 (case when extract(DAYOFWEEK from current_date())=2
                   then pkup_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-3,INTERVAL 12 Month),WEEK(MONDAY))
            else pkup_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-1,INTERVAL 12 Month),WEEK(MONDAY))
    	end)
		and pkup_req_flag = 'Y'
	group by 
		all
UNION all
	select
		inv_dt as prevPeriod,
		'Lots Sold' as metricNm,
		4 as metric_id,
		ifnull(count(lot_nbr),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		(case when extract(DAYOFWEEK from current_date())=2
                   then inv_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-3,INTERVAL 12 Month),WEEK(MONDAY))
            else inv_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-1,INTERVAL 12 Month),WEEK(MONDAY))
    	end)
		and abnormal_close_type = ''
	group by 
		all
UNION all
	select
		inv_dt as prevPeriod,
		'Average Sale Price' as metricNm,
		5 as metric_id,
		ifnull(Round(safe_divide(sum(high_bid_amt), count(lot_nbr)), 0),0) as metricVal
	from
		`cprtpr-dataplatform-sp1`.usmart.fact_lots_ops
	where
		(case when extract(DAYOFWEEK from current_date())=2
                   then inv_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-3,INTERVAL 12 Month),WEEK(MONDAY))
            else inv_dt = DATE_TRUNC(DATE_SUB(CURRENT_DATE()-1,INTERVAL 12 Month),WEEK(MONDAY))
    	end)
		and abnormal_close_type = ''
	group by 
		all
		)
	group by
		all
	order by 
		metric_id
"""

summary = """

SELECT
		sel.hrchy_levl2,
    ops.seller_parent_company,
    COUNT(DISTINCT CASE
      WHEN assg_dt = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) THEN lot_nbr
      ELSE NULL
    END) AS Assigned_cnt_yesterday,
    COUNT(DISTINCT CASE
      WHEN assg_dt = DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY), INTERVAL 364 DAY) THEN lot_nbr
      ELSE NULL
    END) AS Assigned_cnt_prior_year,
		sum(CASE
      WHEN pkup_dt = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) THEN pick_up_same_day_perc
      ELSE NULL
    END) AS Pickup_cnt_yesterday,
    sum(CASE
      WHEN pkup_dt = DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY), INTERVAL 364 DAY) THEN pick_up_same_day_perc
      ELSE NULL
    END) AS pickup_cnt_prior_year,
  FROM
    `cprtpr-dataplatform-sp1`.usmart.fact_lots_ops ops inner join	`cprtpr-dataplatform-sp1`.usmart.dim_seller sel
		on ops.seller_nbr=sel.seller_nbr
  GROUP BY all
	order by 3 desc 
	limit 50
"""
# Fetch data from BigQuery
df = fd.fetch_data_from_bigquery(query)
df2 = fd.fetch_data_from_bigquery(query2)
#df3 = fd.fetch_data_from_bigquery(query3)
df4 = fd.fetch_data_from_bigquery(summary)
dfprev = fd.fetch_data_from_bigquery(PrevPeriod)
dfcurr = fd.fetch_data_from_bigquery(currPeriod)

# Manipulating Actual vs Previous Period
dfTile= pd.merge(dfcurr, dfprev, on='metric_id')
dfTile['ActualDiff']=((dfTile['actualVal']-dfTile['prevVal'])/dfTile['prevVal'])*100
dfTile['className']=dfTile['ActualDiff'].apply(lambda x: 'greenArrow' if x > 0 else 'redArrow')

# Manipulating Actual vs Forecast
dfTile= pd.merge(dfTile, df2, on='metric_id')
dfTile['ForeDiff']=((dfTile['actualVal']-dfTile['forecasted'])/dfTile['forecasted'])*100
# dfTile['foreClassName']=dfTile['ForeDiff'].apply(lambda x: 'greenArrow' if x > 0 else 'redArrow')


# Data Exploration Analysis on processed Data
# executive_summary = f"""
# <ul class='summaryList'>
#     <li>Lots Assigned data for the past <strong>{len(df3)}</strong> days has been analyzed.</li>
#     <li>The highest Lots Assigned was <strong>{'{:,}'.format(int(df['Lots Assigned'].max()))}</strong> by <strong>{df.at[df['Lots Assigned'].idxmax(),'sellerlong']}</strong>.</li>
#     <li>The average daily Lots Assigned was <strong>{'{:,.2f}'.format(df3['lotsAssigned'].mean())}</strong> including weekends.</li>
#     <li>Observed a <strong> {'+' if df3['lotsAssigned'].iloc[-1] > df3['lotsAssigned'].iloc[0] else '-'}{abs(df3['lotsAssigned'].iloc[-1] - df3['lotsAssigned'].iloc[0]) / df3['lotsAssigned'].iloc[0] * 100:.1f}% </strong> change from start to end of the period.</li>
# </ul>
# """

executive_summary=ts.generate()