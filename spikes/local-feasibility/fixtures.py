import hashlib,json
from core import durable,wav_bytes

def install_fixture(store,job,fence,attempt='a',kind='audio'):
 store.prepare(job,fence,attempt)
 j=store.read('SELECT * FROM jobs WHERE id=?',(job,))[0];scene=store.read('SELECT * FROM scenes WHERE id=?',(j['scene'],))[0]
 data=wav_bytes() if kind=='audio' else b'EXPORT-FIXTURE:old successful export'
 key=attempt+'.'+('wav' if kind=='audio' else 'bin')
 durable(store.media/key,data)
 durable(store.root/'spool'/f'{attempt}.json',json.dumps({'key':key,'hash':hashlib.sha256(data).hexdigest(),'words':scene['words'],'voice':scene['voice'],'source':'shared-source','start':0,'end':4000}).encode())
 return attempt
