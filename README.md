# Reddit Sentiment Analyzer for Ethereum

## Description
This project is a Reddit sentiment analyzer specifically designed for the Ethereum subreddit. It fetches comments, performs sentiment analysis, and generates a visual representation of the sentiment distribution. The tool provides insights into the community's sentiment towards various topics related to Ethereum.

## Features
- Fetches recent comments from r/ethereum using the Reddit API
- Performs sentiment analysis on each comment using NLTK
- Generates a color-coded visualization of sentiment scores with Matplotlib
- Provides a summary of the overall sentiment
- Includes a color legend for easy interpretation of sentiment intensity
- Filters out common administrative messages for cleaner analysis
- Handles up to 100 comments per analysis for a comprehensive view

## Installation
1. Clone this repository:
git clone https://github.com/yourusername/Reddit-Sentiment-Analyzer-for-Ethereum.git
cd Reddit-Sentiment-Analyzer-for-Ethereum
Copy2. Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
Copy3. Install required packages:
pip install flask flask-cors praw nltk gensim sumy matplotlib seaborn numpy
Copy4. Set up your Reddit API credentials:
- Create a Reddit account and navigate to https://www.reddit.com/prefs/apps
- Create a new app, select "script" as the type
- Note down your client_id, client_secret, and user_agent
- Update the `reddit = praw.Reddit(...)` section in `app.py` with your credentials

## Usage
1. Run the Flask application:
python app.py
Copy2. Use curl or a similar tool to send a POST request:
curl -X POST http://127.0.0.1:5001/analyze -H "Content-Type: application/json" -d '{"subreddit":"ethereum", "num_comments": 30}' --output ethereum_analysis.png
Copy3. The analysis will be saved as an image file (ethereum_analysis.png)

## Interpreting the Results
- The x-axis represents the compound sentiment score (-1 to 1)
- The y-axis shows truncated comments
- Colors range from red (negative) to yellow (neutral) to green (positive)
- The color bar on the right provides a legend for sentiment intensity
- The summary at the bottom gives an overview of the analyzed comments

## Upcoming Features and Enhancements
1. Improved summarization techniques for more insightful overviews
2. Trend analysis to track sentiment changes over time
3. Interactive web interface for easier use and real-time analysis
4. Enhanced topic modeling to identify key discussion themes
5. Customizable time ranges for fetching comments (e.g., past day, week, month)
6. Support for analyzing multiple cryptocurrencies' subreddits
7. Export options for data in various formats (CSV, JSON)
8. Integration with other data sources for more comprehensive analysis
9. Implementing SQL database storage for historical analysis
10. Advanced NLP features (e.g., entity recognition)
11. An interactive dashboard for data exploration
12. Developing a feature to compare sentiment across different subreddits
13. Adding a predictive component for sentiment forecasting

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer
This tool is for educational and research purposes only. Always do your own research and consult with financial advisors before making investment decisions.
