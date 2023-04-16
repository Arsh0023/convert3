import pika, json

def upload(f, fs, channel, access):
    #Tip: Always right in try and clause statements and in error catching sytanxes as that will help to solve a lot of problems and will this result in cleaner code.

    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange = "", #def exchange queues can be accessed by using name as their key
            routing_key = "video", #name of the queue
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE #makes sure when the pod is reset the messagesa are all there and no information is lost
            )
        )
    except:
        fs.delete(fid)
        return "internal server error", 500
