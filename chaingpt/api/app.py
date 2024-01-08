# Standard lib

# 3rd party
from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api, reqparse

# local
from chaingpt.api.session import new_session, get_workspace
from chaingpt.api.system import SystemEnvironment


app = Flask(__name__)
api = Api(app)


class Session(Resource):
    def post(self):
        url = request.args.get("url")
        if url is None:
            return {"error", "Missing required parameter `url`"}, 400

        try:
            session_id = new_session(url)
            return jsonify({"session_id": session_id})
        except ValueError as e:
            return {"error", str(e)}, 400


class FileQA(Resource):
    def get(self):
        params = {}
        for param in ["session_id", "question", "file_path"]:
            value = request.args.get(param)
            if value is None:
                return {"error", f"Missing required parameter `{param}`"}, 400
            params[param] = value
        
        try:
            workspace = get_workspace(params["session_id"])
            response = workspace.fileqa(params["question"], params["file_path"])
            return jsonify({
                "output": response.output,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens
                })
        except (ValueError, FileNotFoundError) as e:
            return {"error": str(e)}, 400


class FileSearch(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("session_id", type=str, action="append")
        self.parser.add_argument("path", type=str, action="append")

    def get(self):
        params = {}
        for param in ["session_id", "path"]:
            value = request.args.get(param)
            if value is None:
                return {"error", f"Missing required parameter `{param}`"}, 400
            params[param] = value

        try:
            workspace = get_workspace(params["session_id"])
            dirs, files = workspace.search(params["path"])
            return jsonify({
                "directories": dirs,
                "files": files})
        except ValueError as e:
            return {"error": str(e)}, 400


class RunScript(Resource):
    def post(self):
        params = {}
        for param in ["script", "deps"]:
            value = request.args.get(param)
            if value is None:
                return {"error", f"Missing required parameter `{param}`"}, 400
            params[param] = value
        deps = params["deps"].split(" ")
        env = SystemEnvironment()
        result = env.run(params["script"], deps=deps)
        return jsonify({
            "return_code": result.return_code,
            "stdout": result.stdout,
            "stderr": result.stderr
        })


api.add_resource(Session, "/tools/sessions/create")
api.add_resource(FileQA, "/tools/files/qa")
api.add_resource(FileSearch, "/tools/files/search")
api.add_resource(RunScript, "/tools/script")


if __name__ == "__main__":
    app.run(debug=True)