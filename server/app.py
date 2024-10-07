from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = [message.to_dict() for message in Message.query.all()]

    return make_response(messages, 200)

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == "GET":
        return make_response(message.to_dict(), 200)
    
    elif request.method == "PATCH":
        body = request.json.get('body')
        
        if body:
            message.body = body
            db.session.commit()
        return make_response(message.to_dict(), 200)
    
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        return({"message": "Message deleted successfully."}, 200)
        
if __name__ == '__main__':
    app.run(port=5555)
