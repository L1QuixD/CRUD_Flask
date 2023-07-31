#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


get_ipython().system('pip install watchdog --upgrade')


# In[13]:


from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# In[24]:


app = Flask(__name__)
api = Api(app)
DATABASE_URI = 'sqlite:///C:\sqlite\data1.db'
engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# In[25]:


class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    dob = Column(Date, nullable=False)
    amount_due = Column(Integer, default=0)


# In[26]:


Base.metadata.create_all(engine)


# In[ ]:





# In[ ]:





# In[ ]:





# In[27]:


# Error Handling
@app.errorhandler(Exception)
def handle_error(e):
    logging.exception("An error occurred:")
    return jsonify({'message': 'An error occurred. Please check the logs for details.'}), 500


# In[28]:


@app.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        student = Student(first_name=data['first_name'],
                          last_name=data['last_name'],
                          dob=data['dob'],
                          amount_due=data['amount_due'])

        session = Session()
        session.add(student)
        session.commit()
        session.close()

        return jsonify({'message': 'Student created successfully'}), 201
    except KeyError:
        return jsonify({'message': 'Invalid data provided'}), 400
    except Exception as e:
        return jsonify({'message': 'Failed to create student', 'error': str(e)}), 500


# In[29]:


@app.route('/students', methods=['GET'])
def get_all_students():
    try:
        session = Session()
        students = session.query(Student).all()
        session.close()

        results = [
            {
                'student_id': student.student_id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'dob': student.dob.isoformat(),
                'amount_due': student.amount_due
            }
            for student in students
        ]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch students', 'error': str(e)}), 500


# In[30]:


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()

        session = Session()
        student = session.query(Student).filter_by(student_id=student_id).first()
        if student is None:
            session.close()
            return jsonify({'message': 'Student not found'}), 404

        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.dob = data['dob']
        student.amount_due = data['amount_due']

        session.commit()
        session.close()

        return jsonify({'message': 'Student updated successfully'}), 200
    except KeyError:
        return jsonify({'message': 'Invalid data provided'}), 400
    except Exception as e:
        return jsonify({'message': 'Failed to update student', 'error': str(e)}), 500


# In[31]:


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        session = Session()
        student = session.query(Student).filter_by(student_id=student_id).first()

        if student is None:
            session.close()
            return jsonify({'message': 'Student not found'}), 404

        session.delete(student)
        session.commit()
        session.close()

        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete student', 'error': str(e)}), 500


# In[36]:


if __name__ == '__main__':
    app.run(debug=True)


# In[37]:


get_ipython().run_line_magic('tb', '')


# In[ ]:




