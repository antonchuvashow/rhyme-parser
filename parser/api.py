from flask import Flask, jsonify, request

from scraper import get_rhymes

app = Flask(__name__)


@app.route('/crawl', methods=['POST'])
def crawl():
    try:
        word = request.json.get('word')

        if not word:
            return jsonify({'error': 'Please provide a word'}), 400

        return jsonify({'message': get_rhymes(word)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2209)
