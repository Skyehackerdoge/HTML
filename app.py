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

        if not id_type or not id_value:
            return render_template('error.html', message="Invalid input. Please try again.")

        try:
            df = pd.read_csv('data.csv')
        except Exception:
            return render_template('error.html', message="Error reading data.csv file.")

        if id_type == 'student_id':
            # Filter for student_id
            data = df[df['Student ID'] == id_value]
            if data.empty:
                return render_template('error.html', message="Student ID not found. Please try again.")
            total = data['Marks'].sum()
            return render_template('student.html',
                                   tables=data.to_dict(orient='records'),
                                   total=total)
        
        elif id_type == 'course_id':
            # Filter for course_id
            data = df[df['Course ID'] == id_value]
            if data.empty:
                return render_template('error.html', message="Course ID not found. Please try again.")
            avg_marks = round(data['Marks'].mean(), 2)
            max_marks = data['Marks'].max()

            # Plot histogram
            plt.figure()
            plt.hist(data['Marks'], bins=10, edgecolor='black')
            plt.title(f'Histogram for Course {id_value}')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')

            # Save to static folder
            if not os.path.exists('static'):
                os.makedirs('static')
            hist_path = os.path.join('static', 'histogram.png')
            plt.savefig(hist_path)
            plt.close()

            return render_template('course.html',
                                   avg=avg_marks,
                                   maxv=max_marks,
                                   hist='histogram.png')
        else:
            return render_template('error.html', message="Invalid input. Please try again.")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
