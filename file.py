from quart import Quart, jsonify



app = Quart(__name__)
file=open("users.txt", "w")


@app.route('/files/{name}', methods=['GET'])

async def files(name):
    
    file=open("users.txt", "r")
    if not file:
        return jsonify({"error": "Could not open file"}), 500
        
    while True:
        line = file.readline()
        if not line:
            break
        if name in line:
           parts=line.split(",")
           return jsonify({"name": parts[0], "id": parts[1], "hash": parts[2]})
       
    file.close()
    ret={
            "error": "User not found"
    }
    return jsonify(ret)
    
    
if __name__ == '__main__':
    app.run(host='localhost', port=5051)
    
    
    


