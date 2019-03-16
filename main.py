from flask import Flask, render_template
from .employee_db import history, absent, active, out,\
    absent_count, active_count, out_count,\
    date_now, time_now1


# server run
app = Flask(__name__)


@app.route("/")
@app.route("/employee")
def home():
    return render_template("employee.html", history=history,
                           absent=absent, active=active, out=out,
                           absent_count=absent_count, active_count=active_count,
                           out_count=out_count, date_now=date_now, time_now1=time_now1
                           )


if __name__ == '__main__':
    app.run(debug=True)


