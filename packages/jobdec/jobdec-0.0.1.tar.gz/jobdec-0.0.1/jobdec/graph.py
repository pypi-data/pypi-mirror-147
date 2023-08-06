import networkx as nx


class Job:
    def __init__(self, name, depends_on=None, produces=None, min_ram: int = 1):
        self.name = name
        self.depends_on = depends_on or []
        self.produces = produces or []
        self.min_ram = min_ram


class SimpleJob:
    def __init__(self, name, depends_on=None, min_ram: int = 1):
        self.name = name
        self.depends_on = depends_on or []
        self.min_ram = min_ram


def get_graph(jobs, edges):
    g = nx.DiGraph()
    for job in jobs:
        g.add_node(job.name)

    for e in edges:
        g.add_edge(*e)

    return g


def simple_jobs_to_networkx_graph(jobs: list):
    edges = [(dep, job.name) for job in jobs for dep in job.depends_on]

    g = get_graph(jobs, edges)
    return g


def jobs_to_networkx_graph(jobs: list):
    produced_by = {output: job.name for job in jobs for output in job.produces}

    edges = [(produced_by[dep], job.name) for job in jobs for dep in job.depends_on]

    g = get_graph(jobs, edges)
    return g


def get_node_positions(g) -> dict:
    return nx.drawing.nx_agraph.graphviz_layout(g, prog="dot", args="-Grankdir=LR")
