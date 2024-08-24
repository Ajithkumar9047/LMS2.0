import pyodbc
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import tempfile
import logging
current_date = datetime.now().strftime('%d/%m/%Y')
bucket_value = datetime.now().strftime('%Y%m%d')
yesterday_date =(datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')


excelName=f"TVS_LMS_MissingDealerUpdate{current_date}"

logging.basicConfig(
    filename='lmsapp.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
)

query1 = f"SELECT * FROM ThresholdMaster WHERE CONVERT(date, created_on) = CONVERT(date, '{current_date}', 103)"
query2 = f"SELECT * FROM TVSDealerThresholdFeeds feeds JOIN ThresholdMaster master ON feeds.DealerId = master.dealer_id AND feeds.branchId = master.branch_id WHERE bucket = '{bucket_value}' AND CONVERT(date, master.created_on) = CONVERT(date, '{current_date}', 103)"
query3 = f"SELECT * FROM TVSDealerThresholdFeeds feeds JOIN ThresholdMaster master ON feeds.DealerId = master.dealer_id AND feeds.branchId = master.branch_id WHERE bucket = '{bucket_value}' AND CONVERT(date, master.created_on) = CONVERT(date, '{current_date}', 103) AND feeds.thresholdGetdate IS NULL"
query4 = f"UPDATE A SET a.maxcount = RA.threshold from  TVSDealerThresholdFeeds A INNER JOIN ThresholdMaster RA ON A.DealerId = RA.dealer_id and a.branchId = RA.branch_id where bucket = '{bucket_value}' and CONVERT(date,RA.created_on)=CONVERT(date, '{current_date}', 103) and  a.thresholdGetdate IS NULL"
query5= f'''
select * from (select  'website' as source ,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tb_tvs_common_api_leads  where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select 'BikeDekho campaign'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tb_tvs_common_BikeDekho_api_leads where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select ' tvs credit'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tb_tvscredit_common_api_leads   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select'campaign leads'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tvs_all_campaign_leads   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select 'failed booking'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tb_tvs_common_drop_leads   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select '91Wheels'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tvs_91Wheels_leads   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select ' website popup leads'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tb_tvs_websitepopupleads_prod   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select ' BikeDekho Cps'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tb_tvs_common_BikeDekho_cps   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select 'BikeWale'as source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  
from tb_tvs_common_BikeWale_prod   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1 
UNION ALL
select 'facebook'as source,customer_name as name,mobilenumber as mobile,partsid as part_id,emailid as email,campaign_name as model_name,'' as city,TRY_CAST(modelid AS BIGINT) AS model_id,area as pincode,dealer_id,Dealer_Name,Dealer_Mobile,Dealer_Emailid,dealer_area_2 as AREA,Dealer_PinCode  
from tb_tvs_zapier_dms_api_leads   where convert(date,create_date) between convert(date,'{yesterday_date}',103) and convert(date,'{current_date}',103)
and DealerOverFlow=1) as T group by dealer_id, source,name,mobile,part_id,email,model_name,city,model_id,pincode,DEALER_ID,Dealer_Name,Dealer_Mobile,Dealer_Emailid,AREA,Dealer_PinCode  



'''