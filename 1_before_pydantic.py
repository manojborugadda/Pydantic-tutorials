def insert_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("inserted into the DB")
    else:
        raise TypeError('Incorrect data type')
    


def update_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("updtaed into the DB")
    else:
        raise TypeError('Incorrect data type')

insert_patient_data('manoj',25)
update_patient_data('manoj',28)