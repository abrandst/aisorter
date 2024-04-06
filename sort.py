from labeler import Labeler
from mail import Mail
import json

mail=Mail()
labeler=Labeler()

mail.login()
mail_ids=mail.getFolderContent('inbox')
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
    except UnboundLocalError:
        print("Exception in move")

