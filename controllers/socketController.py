from app import socketio
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import MessageModel
from datetime import datetime

def init_socket(_socketio):
  global socketio
  socketio = _socketio


@socketio.on('join_room')
def handle_join_room(data):
  room = data['room']
  join_room(room)
  print(room + "\n\n\n\n")
  emit("joined_room", {"room": room, 'message': 'entrou na sala.'}, room=room)


@socketio.on('leave_room')
def handle_leave_room(data):
  room = data['room']
  leave_room(room)
  emit('left_room', {'room': room, 'message': 'saiu da sala.'}, room=room)


@socketio.on('start_chat')
def handle_start(data):
  user_id = data['user_id']
  friend_id = data['friend_id']
  
  room = f'{user_id}_{friend_id}'
  print(room + "\n\n\n\n\n")

  join_room(room)
  socketio.emit('chat_started', {'room': room}, room=user_id)
  socketio.emit('chat_started', {'room': room}, room=friend_id)


@socketio.on('message')
def handle_message(data):
  sender = data['sender']
  recipient = data['recipient']
  content = data['content']
  room = data['room']

  teste1 = room.split('_')
  teste1.reverse()
  teste3 = '_'.join(teste1)

  msg = {
    'sender': sender,
    'recipient': recipient,
    'content': content,
    'date': datetime.now().strftime('%Y-%m-%d'),
    'hour': datetime.now().strftime('%H:%M:%S')
  }

  socketio.emit("message_sended", msg, room=sender)
  socketio.emit("message_sended", msg, room=recipient)
  socketio.emit("notification", {"sender": sender}, room=recipient)
  message = MessageModel.Message(msg)

  message.create_message()

@socketio.on('typing')
def handle_typing(data):
  sender = data['sender']
  recipient = data['recipient']

  socketio.emit('user_typing', {"sender": sender, "recipient": recipient}, room=recipient)
