from flask import abort, Flask, make_response, render_template

from pathlib import Path
import subprocess, os

app = Flask(__name__)

configFolder = "./config/"
commandTimeoutSeconds = 5


@app.route("/")
def hello_world():
    app.logger.debug(f"Visited root page.")
    return "<p>Hello, World!</p>"


@app.route("/machines/")
def machines():
    if not Path(configFolder).is_dir():
        app.logger.error(f"No folder at expected configuration path \
                           '{Path(configFolder).resolve()}'.")
        abort(500,  "Configuration folder is not present.")

    machines = {}
    for entry in os.listdir(configFolder):
        machineFolder = os.path.join(configFolder, entry)
        if not Path(machineFolder).is_dir():
            app.logger.warning(f"Configuration folder contains a file '{entry}', it will be ignored.")
            continue
        machines[entry] = {"actions": [], "statuses": []}
        for name in (Path(f).stem for f in os.listdir(machineFolder) if os.path.isfile(os.path.join(machineFolder, f))):
            if name.startswith("status_"):
                machines[entry]["statuses"].append(name[7:])
            else:
                machines[entry]["actions"].append(name)

    return render_template("machines.html", machines=machines)


def abort_plaintext(status_code, text):
    # Return a plaintext message instead of HTML
    #see: https://stackoverflow.com/a/69829766/1027706
    response = make_response(text)
    response.status_code = status_code
    abort(response)


def runscript(machine, script):
    scriptPath = Path(os.path.join(configFolder, machine, script + ".sh"))
    # First make sure the script is under the config folder, trying to prevent escaping
    if scriptPath.resolve().is_relative_to(Path(configFolder).resolve()) \
       and os.path.isfile(scriptPath):
        try:
            result = subprocess.run([scriptPath,],
                                  timeout = commandTimeoutSeconds,
                                  capture_output = True,
                                  text = True)
            if result.stderr:
                app.logger.error(f"Execution of {scriptPath} wrote to stderr:\n{result.stderr}")
            return result;
        except Exception as error:
            abort_plaintext(500, f"Could not execute, error: {error}")
        except:
            abort_plaintext(500, f"Could not execute, unknown type was raised.")
    else:
        abort_plaintext(400, "Bad request.")


# TODO: ensure that script cannot contain path separators and '.'
@app.route("/execute/<machine>/<script>")
def execute(machine, script):
        result = runscript(machine, script)
        app.logger.info(f"Execution of '{machine}/{script}' returned code {result.returncode}.")
        if result.returncode == 0:
            return ("", 204)
        else:
            stderr_diag = ""
            if result.stderr:
                stderr_diag = f"\nScript wrote to stderr: {result.stderr}"
            return (f"Execution failed with return code {result.returncode}.{stderr_diag}", 500)


@app.route("/status/<machine>/<script>")
def queryStatus(machine, script):
        result = runscript(machine, script)
        app.logger.info(f"Query status of '{machine}/{script}' returned code {result.returncode}.")
        if result.returncode == 0:
            return ("", 204)
        else:
            body = {"return_code": result.returncode}
            if result.stderr:
                body["stderr"] = result.stderr
            return (body, 200)
