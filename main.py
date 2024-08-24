from Config import *
from ExcelContent import create_excel
#from WhatsappContent import whatsapp_notification
from EmailContent import email_generator
from MaxcountEmail import NullEmail
from SqlContent import establish_connection,update_query
import test as t
ongo=True
apptry=0
try:
    while ongo:
        rows_query1 = establish_connection(query1)
        num_rows_query1 = len(rows_query1)
        print(f"Threshold master: {num_rows_query1}")
        logging.info(f"Threshold master: {num_rows_query1}")

        rows_query2 = establish_connection( query2)
        num_rows_query2 = len(rows_query2)
        print(f"Threshold FEED: {num_rows_query2}")
        logging.info(f"Threshold FEED: {num_rows_query2}")

        rows_query3 = establish_connection( query3)
        num_rows_query3 = len(rows_query3)
        print(f"Total null: {num_rows_query3}")
        logging.info(f"Total null: {num_rows_query3}")
        overflowQUERY= establish_connection( query5)
        num_overflowQUERY = len(overflowQUERY)
        print(f"Total lead overflow: {num_overflowQUERY}")
        logging.info(f"Total null: {num_overflowQUERY}")

        if num_rows_query1 <= num_rows_query2 and num_rows_query3 >= 0 :
            
            if any(row[5] == 9999 for row in rows_query3):
                print("update query start")
                logging.warning("update query start")
                update_query()
                NullEmail(num_rows_query1,num_rows_query2,num_rows_query3)
            else:
                
                print("maxcount is up to date")
                logging.warning("maxcount is up to date")
            rows_query3 = establish_connection( query3)   
            if any(row[5] != 9999 for row in rows_query3):
                excel_name=create_excel(rows_query1, rows_query2,overflowQUERY)
                email_generator(excel_name)
                #whatsapp_notification(num_rows_query1, num_rows_query2, num_rows_query3)
            ongo=False
        else:
            print('Not equal')
            logging.error("thresholdMaster and thresholdfeed count is not equal")
            t.run()
            apptry+=1
            if  apptry==2:
                ongo=False

except pyodbc.Error as e:
    logging.error("A pyodbc error occurred: %s", str(e))
    print("A pyodbc error occurred:", str(e))
except Exception as e:
    logging.error("An error occurred: %s", str(e))


