#Polamraju Sai nithin 
from flask import Flask, request, jsonify
from textblob import TextBlob
import requests

app = Flask(__name__)

@app.route('/comments/<subfeddit>', methods=['GET'])

#Function to get the comments and save them in ans
def get_comments(subfeddit):
    limit = 25
    #desubfeddit_id = request.args.get('subfeddit_id')
    subfeddit_id = 1
    #api_url = f'http://localhost:8080/api/v1/comments/?subfeddit_id={subfeddit_id}&limit={limit}'
    api_url = f'http://localhost:8080/api/v1/comments/?subfeddit_id=1&limit=25'
    
    #above url to access the data from api and then use the data to say positive or nagative
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        comments_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"})

    query_time_range = request.args.get('time_range')
    sort_by_polarity = request.args.get('sort_by_polarity', type=bool, default=False)

    filtered_comments = filter_comments(subfeddit, query_time_range, comments_data)
    sorted_comments = sort_comments(filtered_comments, sort_by_polarity)
    limited_comments = sorted_comments


    result = []

    #store the data which we get from the JSON file and taking only the comments part for the next step
    comments = limited_comments.get('comments', [])
    
    for comment in comments:
            polarity_score, classification = analyze_sentiment(comment['text'])
            result.append({
                #"username": comment['username'],
                "comment_id": comment['id'],
                "text": comment['text'],
                "polarity_score": polarity_score,
                "classification": classification
            })
    return jsonify(result)

#filter funtion if we want to filter the comments for futher use 
def filter_comments(subfeddit, time_range, comments_data):
    
    filtered_comments = comments_data  

    return filtered_comments

#sort funtion if we want to filter the comments for futher use
def sort_comments(comments, by_polarity=False):
    
    sorted_comments = comments

    return sorted_comments

# this function is to analyze the data we stored and classify them using the polarity score.
def analyze_sentiment(text):
    analysis = TextBlob(text)

    if analysis.sentiment.polarity > 0:
        return analysis.sentiment.polarity, "positive"
    elif analysis.sentiment.polarity < 0:
        return analysis.sentiment.polarity, "negative"
    else:
        return analysis.sentiment.polarity, "neutral"

if __name__ == '__main__':
    app.run(debug=True, port=8082)
