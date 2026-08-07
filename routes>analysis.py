from flask import Blueprint, render_template

analysis = Blueprint(
    "analysis",
    __name__
)


@analysis.route("/analysis")
def analysis_page():

    return render_template(
        "analysis.html"
    )


@analysis.route("/analysis-results")
def analysis_results_page():

    return render_template(
        "analysis_results.html"
    )
