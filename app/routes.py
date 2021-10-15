from flask import Blueprint

hello_world_bp = Blueprint("hello_world", __name__)

@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    my_beautiful_response_body = "Hello, World!"
    return my_beautiful_response_body

@hello_world_bp.route("/hello-world/JSON", methods=["GET"])
def hello_world_json():
    return {
        "name" : "Rhyannon",
        "message" : "Hi y'all",
        "hobbies" : ["Coding", "Movies", "Abolition"],
        }, 201