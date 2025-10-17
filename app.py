from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_type = request.form.get('ID')
        id_value = request.form.get('id_value')

        # Basic validation
        if not id_type or not id_value or id_value.strip() == "":
            return render_template('error.html', message="Invalid input. Please try again.")

        try:
            df = pd.read_csv('data.csv')
        except Exception:
            return render_template('error.html', message="Invalid input. Please try again.")

        if id_type == 'student_id':
            result = df[df['Student ID'] == id_value]
            if result.empty:
                return render_template('error.html', message="Invalid input. Please try again.")

            total_marks = result['Marks'].sum()
            records = result.to_dict(orient='records')

            return render_template('student.html',
                                   records=records,
                                   total=total_marks)

        elif id_type == 'course_id':
            result = df[df['Course ID'] == id_value]
            if result.empty:
                return render_template('error.html', message="Invalid input. Please try again.")

            avg_marks = round(result['Marks'].mean(), 2)
            max_marks = result['Marks'].max()

            # Save histogram
            if not os.path.exists('static'):
                os.makedirs('static')
            plt.figure()
            plt.hist(result['Marks'], bins=10, edgecolor='black')
            plt.title(f'Histogram for {id_value}')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            plt.savefig('static/histogram.png')
            plt.close()

            return render_template('course.html',
                                   average=avg_marks,
                                   maximum=max_marks,
                                   hist='histogram.png')
        else:
            return render_template('error.html', message="Invalid input. Please try again.")
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run()
