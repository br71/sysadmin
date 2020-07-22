# Export data from SQL result set to pandas data frame and directly (from memory)to excel (response from flask)
# This works for Python 3. # Import related only to this function


import pandas as pd
import io
from flask import make_response


@app.route('/export_pandas_excel')
def export_pandas_excel():
    # Function is defined somewhere else
    data = result_set_from_db_query
   
    # Convert result set to pandas data frame and add columns
    df = pd.DataFrame((tuple(t) for t in data), columns=('Date ', 'name', 'username', 'description', 'email'))

    # Creating output and writer (pandas excel writer)
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
   
    # Export data frame to excel
    df.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    writer.save()
    writer.close()
   
    # Flask create response 
    r = make_response(out.getvalue())
    
    # Defining correct headers
    r.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
    r.headers["Content-type"] = "application/x-xls"
    
    # Finnaly return response. When user access to this URL it will get browser window with download or open file option.
    return r
