from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:M%40riaSQL%2189@localhost/url_shortener'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'clicks': self.clicks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_code=code).first():
            return code

@app.route('/')
def index():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template('index.html', urls=urls)

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    original_url = data.get('url', '').strip()

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    # Check if already shortened
    existing = URL.query.filter_by(original_url=original_url).first()
    if existing:
        return jsonify({'short_code': existing.short_code}), 200

    short_code = generate_code()
    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'short_code': short_code}), 201

@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@app.route('/delete/<int:url_id>', methods=['DELETE'])
def delete_url(url_id):
    url = URL.query.get_or_404(url_id)
    db.session.delete(url)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)