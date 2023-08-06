import datetime
import time

import networkx as nx
from flask import Flask, Markup, jsonify, request

from jobdec.file_utils import full_path
from jobdec.graph import simple_jobs_to_networkx_graph
from jobdec.scheduled_job import JobStatuses


def create_app(scheduler):
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder=full_path(__file__) / "static",
    )
    app.scheduler = scheduler

    def health():
        pass

    def version():
        pass

    @app.route("/jobs")
    def jobs():
        # Returns jsonified details of all scheduler's jobs (jobs)
        return jsonify([t.to_json() for t in app.scheduler.jobs])

    @app.route("/jobs/<job_name>")
    def job(job_name):
        try:
            job = app.scheduler.get_job(job_name)
        except KeyError:
            resp = {"status": "failed", "detail": f"No job found named {job_name}"}
            return jsonify(resp)

        return jsonify(job.to_json())

    @app.route("/run_leaf_nodes")
    def run_leaf_nodes():
        # NOTE: This means "run all jobs with no upstream
        #       dependencies". It might be clearer to call
        #       this "run all root nodes"? Not sure.
        app.scheduler.run_all_leaf_nodes()
        return jsonify({"status": "success"})

    @app.route("/graph")
    def graph():
        # NOTE: This means "run all jobs with no upstream
        #       dependencies". It might be clearer to call
        #       this "run all root nodes"? Not sure.
        jobs = app.scheduler.job_lookup
        text = parse_jobs_to_svg(jobs)
        return Markup(text)

    @app.route("/kill/<job_name>")
    def kill(job_name):
        # NOTE: This means "run all jobs with no upstream
        #       dependencies". It might be clearer to call
        #       this "run all root nodes"? Not sure.
        try:
            job = app.scheduler.get_job(job_name)
        except KeyError:
            resp = {"status": "failed", "detail": f"No job found named {job_name}"}
            return jsonify(resp)

        action = app.scheduler.force_kill(job)

        # We wait to give the action a chance to
        # be processed. Yes, this is hacky, but
        # I think it's a lot more helpful to report
        # the result of the action here than to
        # simply report "success". Since we interact
        # with the Scheduler only by creating actions
        # I don't know of a clean way to specify
        # "only return the resulting action's status
        # when it has been processed".
        time.sleep(0.1)
        return jsonify({"status": action.status})

    def get_edges():
        pass

    def next_job():
        pass

    def running():
        # Returns jsonified details of all jobs (jobs) currently running
        pass

    def failed():
        # Returns jsonified details of all jobs (jobs) in failed state
        pass

    def status():
        pass

    def logs():
        pass

    def history():
        pass

    def force_kill():
        pass

    def force_run():
        pass

    def force_run_dependencies():
        pass

    def get_hosts():
        pass

    def update_hosts():
        pass

    return app


colours = {
    JobStatuses.pending: "#bbbbbb",
    JobStatuses.pending_searching_for_host: "#bbbbbb",
    JobStatuses.pending_no_host_found: "#bbbbbb",
    JobStatuses.pending_about_to_run: "#bbbbbb",
    JobStatuses.pending_waiting_to_retry: "#bbbbbb",
    JobStatuses.running: "#a0b3dd",
    JobStatuses.succeeded: "#03cc01",
    JobStatuses.failed_waiting_to_rerun: "#ff3233",
    JobStatuses.failed: "#ff3233",
    JobStatuses.killed: "#ff3233",
}


def parse_jobs_to_svg(jobs: dict):
    """
    Takes in a dictionary of {job_name: Task}
    and returns SVG text for displaying the given
    jobs on a web page.
    """
    g = simple_jobs_to_networkx_graph(list(jobs.values()))
    now = datetime.datetime.now()

    # Get a dictionary from job name to (x, y) position
    # positions = nx.nx_pydot.pydot_layout(g, prog='dot')
    # positions = nx.drawing.nx_agraph.graphviz_layout(g, prog='dot', args='-Grankdir=LR')
    # positions = nx.drawing.nx_agraph.graphviz_layout(g, prog='dot')
    positions = nx.drawing.nx_agraph.graphviz_layout(
        g, prog="dot", args="-Grankdir=BT -Granksep=1.5"
    )

    # Format here is start x, start y, width, height
    text = """
    <head>
      <link rel="stylesheet" type="text/css" href="/static/style.css">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    </head>
    """
    text += "<body>"

    # TODO: Adjust viewbox to size of graph
    text += """<svg viewBox="0 0 1600 900">"""

    for job_name, job in jobs.items():
        x, y = positions[job_name]

        final_name = job_name.split(".")[-1]
        short_name = final_name[0:16] + "..." if len(final_name) > 16 else final_name
        if (
            job.next_run
            and job.status == JobStatuses.pending
            and job.next_run - now < datetime.timedelta(days=1)
        ):
            next_run_str = job.next_run.time().isoformat()
            if next_run_str[-3:] == ":00":
                next_run_str = next_run_str[:-3]
            next_run_text = f"""
          <text class="info" font-family="Inter" font-size="11" fill="#555">
            <tspan x="102" y="63.8636">{next_run_str}</tspan>
          </text>
            """
        else:
            next_run_text = ""

        svg_class = " " + job.status.name

        # The rectangle starts at 10, 10, so if you line this up with
        # arrows remember to add 10 to the svg's x and y
        job_text = f"""
        <svg x={x} y={y} class="job{svg_class}" width="260" height="86" viewBox="0 0 260 86" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="10" y="10" width="239" height="65" rx="9" fill="white"/>
          <text class="title" fill="black" font-family="Inter" font-size="12" font-weight="bold">
            <tspan x="22" y="30.8636">
              <a href="jobs/{job_name}" target="_blank">{short_name}</a>
            </tspan>
          </text>
          <text class="info" fill="black" font-family="Inter" font-size="12">
            <tspan x="22" y="63.8636">{job.status.name}</tspan>
          </text>
          {next_run_text}
          <rect x="10" y="10" width="239" height="65" rx="9" stroke="#F0F0F0"/>
          <line class="line" x1="10" y1="42" x2="250" y2="42" stroke="#F0F0F0"/>
          <circle class="status" cx="211.5" cy="42.5" r="16" fill="white" stroke="#F0F0F0"/>
          <circle class="progress-circle" cx="211.5" cy="42.5" r="11.5" stroke="#06B6FF" stroke-width="3"/>
          <circle class="succeeded" cx="211.5" cy="42.5" r="7.5" fill="#FF9900"/>
          <circle class="failed" cx="211.5" cy="42.5" r="7.5" fill="#FF0000"/>
          <circle class="socket" cx="30" cy="10" r="4" fill="white" stroke="#F0F0F0"/>
          <circle class="socket" cx="30" cy="75" r="4" fill="white" stroke="#F0F0F0"/>
        </svg>
        """

        text += job_text

    text += """
      <!-- arrowhead marker definition -->
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
            markerWidth="6" markerHeight="6"
            orient="auto-start-reverse">
      <!-- fill matches stroke color-->
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#666666" />
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#666666" />
        </marker>
      </defs>
    """

    for e in g.edges:
        from_job_name, to_job_name = e
        from_x, from_y = positions[from_job_name]
        to_x, to_y = positions[to_job_name]
        arrow_text = f"""
          <polyline points="{from_x + 30},{from_y + 75} {to_x + 30},{to_y + 10}" fill="none" stroke="black" marker-end="url(#arrow)" />
        """
        text += arrow_text

    text += """</svg>"""
    text += "</body>"

    return text
