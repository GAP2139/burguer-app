db = db.getSiblingDB('burguer_app_db')

db.createUser({
    user: 'appuser',
    pwd: 'apppass',
    roles: [{ role: 'readWrite', db: 'burguer_app_db'}]
});