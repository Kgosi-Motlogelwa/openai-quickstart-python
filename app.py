import json
import logging
import os

import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.getLogger('flask_cors').level = logging.DEBUG

@app.route("/", methods=("GET", "POST"))
@cross_origin()
def index():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = json.loads(request.data)
        print("data: ", data['syllabus'], data['syllabusPoint'])
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(data['syllabus'], data['syllabusPoint']),
            max_tokens=2048,
            temperature=0.2,
        )
        return response.choices[0].text
    else:
        return 'Content-Type not supported!'
    
    # if request.method == "POST":
    #     print("This is a POST Method")
    #     syllabus = request.form["syllabus"]
    #     syllabusPoint = request.form["syllabusPoint"]
    #     print("syllabus: ", syllabus, "syllabusPoint: ", syllabusPoint)
    #     response = openai.Completion.create(
    #         model="text-davinci-003",
    #         prompt=generate_prompt(syllabus, syllabusPoint),
    #         max_tokens=2048,
    #         temperature=0.2,
    #     )
    #     print("response: ", response)
    #     response.headers.add("Access-Control-Allow-Origin", "*")
    #     # logging.getLogger('flask_cors').level = logging.DEBUG
    #     return response
    # logging.getLogger('flask_cors').level = logging.DEBUG
    # return  'Get Request Not Possible'


def generate_prompt(syllabus, syllabusPoint):
    return """Give me one or more example problems to help me learn:  
        {syllabusPoint} I'm preparing for {syllabus} without the solution.
        Insert the text breakForAnswer between the problem and solution.
        Output the solution after the text breakForAnswer.
        Write any equations in latex. Make solution as detailed as possible. 
        """

@app.route("/lesson", methods=["POST"])
@cross_origin()
def post_example():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = json.loads(request.data)
        print("data: ", data['syllabus'], data['syllabusPoint'])
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt_forLesson(data['syllabus'], data['syllabusPoint']),
            max_tokens=2048,
            temperature=0.2,
        )
        return response.choices[0].text
    else:
        return 'Content-Type not supported!'
    
    
def generate_prompt_forLesson(syllabusLocal, syllabusPointLocal):
    print(syllabusPointLocal)
    return """Teach me:  
        {syllabusPointLocal} in 10 minutes. I'm preparing for {syllabusLocal}.
        Write any equations in latex. Make explanation as detailed as possible. 
        """