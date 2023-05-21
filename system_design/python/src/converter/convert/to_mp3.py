import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    #empty file
    tf = tempfile.NamedTemporaryFile()
    #video contents
    out = fs_videos.get(ObjectId(message["videos_fid"]))
    #read the out file
    tf.write(out.read())
    #create audio from temp file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    #write the audio to file
    tf_path = tempfile.gettempdir + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    #save the file to mongo
    f = open(tf_path, 'r')
    data = f.read()
    fid = fs_mp3s.put(data) #Storing our mp3 data into our gridFs
    f.close()
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)
    try:
        channel.basic_publish(
            exchange = "",
            routing_key = os.environ.get("MP3_QUEUE"),
            body = json.dumps(message), #because queue gets only json objects
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "Failed to publish message"