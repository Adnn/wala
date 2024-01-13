from flask import Flask, render_template

from pathlib import Path
import subprocess, os

app = Flask(__name__)

configFolder = "./config/"
commandTimeoutSeconds = 5


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/machines/")
def machines():
    machines = {}
    for entry in os.listdir(configFolder):
        machineFolder = os.path.join(configFolder, entry)
        machines[entry] = {"actions": [], "statuses": []}
        for name in (Path(f).stem for f in os.listdir(machineFolder) if os.path.isfile(os.path.join(machineFolder, f))):
            if name.startswith("status_"):
                machines[entry]["statuses"].append(name[7:])
            else:
                machines[entry]["actions"].append(name)

    return render_template("machines.html", machines=machines)


@app.route("/execute/<machine>/<script>")
def execute(machine, script):
    scriptPath = os.path.join(configFolder, machine, script + ".sh")
    if os.path.isfile(scriptPath):
        try:
            result = subprocess.run([scriptPath,],
                                    timeout = commandTimeoutSeconds)
            app.logger.info(f"Execution of '{machine}/{script}' returned code {result.returncode}.")
            if result.returncode == 0:
                return ("", 204)
            else:
                return (f"Execution failed with return code {result.returncode}", 500)
        except Exception as error:
            return(f"Could not execute, error: {error}.", 500)
        except:
            return(f"Could not execute, unknown type was raised.", 500)
    else:
        return "Bad request.", 400
