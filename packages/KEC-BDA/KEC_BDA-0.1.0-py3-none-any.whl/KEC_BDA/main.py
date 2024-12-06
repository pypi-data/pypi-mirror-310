from . import exp2A, exp2B, exp3, exp4, exp5, exp6, exp7, exp8

experiments = {
    "2A": {"run": exp2A.run, "name": "Exp:2a(Action)"},
    "2B": {"run": exp2B.run, "name": "Exp:2b(TRANSFORMATION)"},
    "3": {"run": exp3.run, "name": "Experiment 3"},
    "4": {"run": exp4.run, "name": "Experiment 4"},
    "5": {"run": exp5.run, "name": "Exp:5 Find the minimum temperature in a city using PySpark"},
    "6": {"run": exp6.run, "name": "Exp:6 Perform DDL and DML operations in PySpark SQL."},
    "7": {"run": exp7.run, "name": "Exp:7 Implement Spark SQL Functions to manipulate strings, dates using PySpark SQL."},
    "8": {"run": exp8.run, "name": "Exp:8 Apply Windowing Functions and aggregate function using PySpark SQL."}
}

def list_experiments():
    """List all available experiments."""
    print("Available Experiments:")
    for key, value in experiments.items():
        print(f"{key}. {value['name']}")



def run_experiment(exp_key):
    """Run an experiment by key."""
    if exp_key in experiments:
        experiments[exp_key]['run']()
    else:
        print("Invalid experiment key.")
