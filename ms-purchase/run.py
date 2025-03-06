from app import create_app, db


app = create_app()
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5002)


@app.cli.command("create-db")
def create_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada")