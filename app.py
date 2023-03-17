import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        syllabus = request.form["syllabus"]
        syllabusPoint = request.form["syllabusPoint"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(syllabus, syllabusPoint),
            max_tokens=2048,
            temperature=0.2,
        )
        print(response)
        return response
    return  'Get Request Not Possible'


def generate_prompt(syllabus, syllabusPoint):
    return """Give me one or more example problems to help me learn:  
        {syllabusPoint}I'm preparing for {syllabus} without the solution. 
        The response shouldn't include, "I hope this helps! Let me know if you have any questions".
        Write any equations in latex. Make solution as detailed as possible. OUTPUT ONLY a javascript object for example {question: 'Solve the equation $2x + 3 = 11$', solution: '$x = 4$'}

        """
