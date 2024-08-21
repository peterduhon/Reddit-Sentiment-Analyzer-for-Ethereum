import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import praw
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.models import LdaMulticore
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Use the 'Agg' backend for Matplotlib to avoid GUI issues on macOS
matplotlib.use('Agg')

# Download necessary NLTK data
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Define the Flask application
app = Flask(__name__)
CORS(app)

# Reddit API credentials
reddit = praw.Reddit(
    client_id="ZncY_7rRtFdvuo5HknSqow",
    client_secret="U_VvAIQW4r8y7Vr5LuRsvq7tmu-Jtg",
    user_agent="CommentAnalyzerAPI by /u/Front-Holiday-1591"
)

sia = SentimentIntensityAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_comments():
    try:
        data = request.json
        if not data or 'subreddit' not in data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        subreddit_name = data.get('subreddit')
        num_comments = data.get('num_comments', 100)  # default to 100 comments if not specified

        subreddit = reddit.subreddit(subreddit_name)
        comments = list(subreddit.comments(limit=num_comments))

        results = []
        all_text = []
        for comment in comments:
            if not comment.body.startswith("Your submission was removed"):
                sentiment = sia.polarity_scores(comment.body)
                results.append({
                    'text': comment.body,
                    'sentiment': sentiment
                })
                all_text.append(comment.body)

        # Combine all comments into a single text for summarization
        all_text = ' '.join(all_text)

        # Generate summary
        parser = PlaintextParser.from_string(all_text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count=3)  # Summarize to 3 sentences
        summary = " ".join([str(sentence) for sentence in summary])

        # Generate visualization
        compound_scores = [result['sentiment']['compound'] for result in results]
        plt.figure(figsize=(12, 10))
        sns.set(style="whitegrid")

        # Create color map
        colors = LinearSegmentedColormap.from_list("sentiment", ["red", "yellow", "green"])

        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(12, 10))
        bars = ax.barh(range(len(compound_scores)), compound_scores, color=colors(np.array(compound_scores) * 0.5 + 0.5))
        
        # Add labels to bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                    f'{width:.2f}', ha='left', va='center')

        # Customize chart
        ax.set_xlabel('Compound Sentiment Score')
        ax.set_ylabel('Comments')
        ax.set_title(f'Sentiment Analysis for r/{subreddit_name}')
        fig.suptitle(f'Analysis Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}', fontsize=10)
        
        # Add truncated comment text to y-axis
        truncated_comments = [comment[:50] + '...' if len(comment) > 50 else comment for comment in [r['text'] for r in results]]
        ax.set_yticks(range(len(compound_scores)))
        ax.set_yticklabels(truncated_comments)

        # Add color legend
        sm = plt.cm.ScalarMappable(cmap=colors, norm=plt.Normalize(vmin=-1, vmax=1))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label('Sentiment', rotation=270, labelpad=15)

        # Add summary to the plot
        fig.text(0.5, 0.01, f"Summary: {summary[:200]}...", wrap=True, horizontalalignment='center', fontsize=8)

        plt.tight_layout()

        # Save the plot to a file
        plot_path = 'sentiment_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        return send_file(plot_path, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
