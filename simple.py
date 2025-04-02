text = ['1', '2', '3']
data = {'chat_id': 134}

for te in text:
    data['text'] = te
    print({'text': data['text']})  # Only printing the updated text

        
        