from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from _5_1ToFE import ice_break_with

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary_and_facts, interests, ice_breakers, profile_pic_url = ice_break_with(
        name=name
    )
    return jsonify(
        {
            "summary_and_facts": summary_and_facts.to_dict(),
            "interests": interests.to_dict(),
            "ice_breakers": ice_breakers.to_dict(),
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":

    # 5000번 포트가 Flask의 기본인데, 아이패드 사이드카가 5000번 포트 이용중이라 커스텀
    app.run(port=5001, host="0.0.0.0", debug=True)