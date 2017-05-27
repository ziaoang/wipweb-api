print 'Please input "wipweb" to confirm you know what you are doing'
confirm = raw_input()

if confirm == 'wipweb':
    from db import db
    db.drop_all()


