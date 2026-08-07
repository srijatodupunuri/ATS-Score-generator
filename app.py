import os

from flask import Flask

from config.config import Config
from routes.about import about
from routes.analysis import analysis
from routes.ats import ats
from routes.dashboard import dashboard
from routes.home import home
from routes.jd import jd
from routes.reports import reports
from routes.resume import resume
from routes.upload import upload

app = Flask(__name__)


app.config.from_object(Config)

os.makedirs(app.config["JOB_DESCRIPTION_FOLDER"], exist_ok=True)

os.makedirs(app.config["RESUME_FOLDER"], exist_ok=True)


app.register_blueprint(upload)
app.register_blueprint(jd)
app.register_blueprint(resume)
app.register_blueprint(ats)
app.register_blueprint(home)

app.register_blueprint(dashboard)

app.register_blueprint(analysis)

app.register_blueprint(reports)

app.register_blueprint(about)



if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True
    )
