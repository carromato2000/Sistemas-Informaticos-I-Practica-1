from quart import Quart, jsonify
import uuid

secret_uuid=uuid.UUID(hex='00010203-0405-0607-0809-0a0b0c0d0e0f')
app = Quart(__name__)



@app.route('/files/<UID>', methods=['GET'])

async def files(id):
    
    file=open("users.txt", "r")
    if not file:
        return jsonify({"error": "Could not open file"}), 500
        
    while True:
        line = file.readline()
        if not line:
            break
        if id in line:
           parts=line.split(",")
           return jsonify({"name": parts[0], "psswd":parts[1], "id": parts[2], "hash": parts[3]})
       
    file.close()
    ret={
            "error": "User not found"
    }
    return jsonify(ret)
    
    
if __name__ == '__main__':
    app.run(host='localhost', port=5051)
    
    
    


