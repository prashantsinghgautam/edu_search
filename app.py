from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def google_search(query, api_key, cx, suffix):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query + ' ' + suffix,
        'key': api_key,
        'cx': cx,
    }

    response = requests.get(base_url, params=params)
    search_results = response.json()

    if 'items' in search_results:
        top_result = search_results['items'][0]['link'] if search_results['items'] else None
        return top_result
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        google_api_key = "AIzaSyC6g1M5hxepqkVHi2frqdnQDLSA3LFRWwE"
        search_engine_cx = "92a425bcc5b9e4313"
        suffixes = ['byjus', 'khan academy', 'toppr', 'vedantu']

        result_set = set()

        for suffix in suffixes:
            full_query = search_query + ' ' + suffix
            top_result = google_search(full_query, google_api_key, search_engine_cx, suffix)

            if top_result:
                result_set.add(top_result)

        if result_set:
            return render_template('results.html', results=result_set)
        else:
            return render_template('no_results.html')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
