from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# Database file path
DATABASE = '/data/fraud_detection.db'

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    per_page = 10

    conn = sqlite3.connect(DATABASE)

    if search_query:
        # Check if the search query is a full timestamp or just a date
        if len(search_query) > 10:  # Assuming full timestamp is longer than 10 characters
            base_query = "SELECT * FROM potential_fraud WHERE Time LIKE ?"
            count_query = "SELECT COUNT(*) as count FROM potential_fraud WHERE Time LIKE ?"
            search_param = search_query + '%'  # To match timestamp starting with the query
        else:
            base_query = "SELECT * FROM potential_fraud WHERE DATE(Time) = ?"
            count_query = "SELECT COUNT(*) as count FROM potential_fraud WHERE DATE(Time) = ?"
            search_param = search_query

        params = [search_param]
    else:
        base_query = "SELECT * FROM potential_fraud"
        count_query = "SELECT COUNT(*) as count FROM potential_fraud"
        params = []

    total_count = pd.read_sql_query(count_query, conn, params=params).iloc[0]['count']
    total_pages = (total_count + per_page - 1) // per_page

    query = base_query + " LIMIT ? OFFSET ?"
    params.extend([per_page, (page - 1) * per_page])
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    return render_template('index.html', 
                           tables=[df.to_html(classes='table table-bordered table-hover data-table table-striped',
                                              header=True, index=False)],
                           page=page, 
                           total_pages=total_pages, 
                           total_count=total_count,
                           search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
