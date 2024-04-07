from labeler import Labeler
from mail import Mail
import json
from dotenv import load_dotenv
import os

load_dotenv()
mail=Mail()
labeler=Labeler()

folder_name=os.environ.get('MAIL_FOLDER')

mail.login()
mail_ids=mail.getFolderContent(folder_name)
for s in mail_ids:
    try:
        text=mail.get_text(s)    
        label=labeler.label(text)
        print(json.dumps(label, indent=2))
            
    
    
        match(label['category']):
            case 'ad':        
                mail.move(s,'ad')
            case 'notification':
                mail.move(s,'notification')
            case 'bill':
                mail.move(s,'bill')
            case 'verification':
                mail.move(s,'nearlytrash')
    except FileExistsError as e:
        raise e
    except json.decoder.JSONDecodeError as e:
        print("Original message")
        print(text)
        print("----------------------------------------------------")
        print(label)

