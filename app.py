from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        id_type = request.form.get("ID")
        id_value = request.form.get("id_value")

        if not id_type or not id_value:
            return render_template("error.html", message="Invalid input. Please try again.")

        try:
            df = pd.read_csv("data.csv")
        except Exception:
            return render_template("error.html", message="Error reading data.csv file.")

        # ✅ Handle student_id
        if id_type == "student_id":
            df_student = df[df["Student ID"].astype(str) == str(id_value)]
            if df_student.empty:
                return render_template("error.html", message="Student ID not found. Please try again.")

            total_marks = df_student["Marks"].sum()
            return render_template(
                "student.html",
                student_data=df_student.to_dict(orient="records"),
                total_marks=total_marks
            )

        # ✅ Handle course_id
        elif id_type == "course_id":
            df_course = df[df["Course ID"].astype(str) == str(id_value)]
            if df_course.empty:
                return render_template("error.html", message="Course ID not found. Please try again.")

            avg_marks = round(df_course["Marks"].mean(), 2)
            max_marks = df_course["Marks"].max()

            # Create histogram
            plt.figure()
            plt.hist(df_course["Marks"], bins=10, edgecolor="black")
            plt.title(f"Histogram for Course {id_value}")
            plt.xlabel("Marks")
            plt.ylabel("Frequency")

            os.makedirs("static", exist_ok=True)
            plt.savefig("static/histogram.png")
            plt.close()

            return render_template(
                "course.html",
                average_marks=avg_marks,
                maximum_marks=max_marks,
                hist_file="histogram.png"
            )

        else:
            return render_template("error.html", message="Invalid input. Please try again.")

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
