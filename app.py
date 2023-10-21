from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('view_data'))

@app.route('/insert-data', methods=['GET'])
def insert_data_form():
    return render_template('insert_data.html')

@app.route('/insert-data', methods=['POST'])
def insert_data():
    # Get data from the form
    store_number = request.form['store_number']
    storeLocation_Address = request.form['storeLocation_Address']
    Lab_Type = request.form['Lab_Type']
    Windows_OS_Version = request.form['Windows_OS_Version']
    Windows_Patch_Version = request.form['Windows_Patch_Version']
    POS_Type = request.form['POS_Type']
    POS_Version = request.form['POS_Version']
    # Get data for other columns similarly

    # Insert data into the SQLite database
    conn = sqlite3.connect('store_Information.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO store_Information (store_Number, storeLocation_Address, Lab_Type, Windows_OS_Version, Windows_Patch_Version, POS_Type, POS_Version) VALUES (?,?,?,?,?,?,?)", (store_number,storeLocation_Address,Lab_Type,Windows_OS_Version,Windows_Patch_Version,POS_Type,POS_Version))
    conn.commit()
    conn.close()

    return redirect('/view-data') 

@app.route('/view-data', methods=['GET'])
def view_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('store_Information.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM store_Information;")
    rows = cursor.fetchall()

    conn.close()
    return render_template('view_data.html',rows=rows)

@app.route('/edit-data/<int:id>', methods=['GET', 'POST'])
def edit_data_form(id):
    if request.method == 'GET':
        # Fetch the record from the database by ID
        conn = sqlite3.connect('store_Information.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM store_Information WHERE store_Number=?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            # Render the edit_data.html template with the record data
            return render_template('edit_data.html', row=row)
        else:
            # Handle the case where the record with the given ID is not found
            return "Record not found", 404

    if request.method == 'POST':
        # Get the updated data from the form
        store_number = request.form['store_number']
        storeLocation_Address = request.form['storeLocation_Address']
        Lab_Type = request.form['Lab_Type']
        Windows_OS_Version = request.form['Windows_OS_Version']
        Windows_Patch_Version = request.form['Windows_Patch_Version']
        POS_Type = request.form['POS_Type']
        POS_Version = request.form['POS_Version']

        # Update the record in the database
        conn = sqlite3.connect('store_Information.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE store_Information SET store_Number=?, storeLocation_Address=?, Lab_Type=?, Windows_OS_Version=?, Windows_Patch_Version=?, POS_Type=?, POS_Version=? WHERE store_Number=?",
                       (store_number, storeLocation_Address, Lab_Type, Windows_OS_Version, Windows_Patch_Version, POS_Type, POS_Version, id))
        conn.commit()
        conn.close()

        # Redirect to the view_data route after updating the record
        return redirect('/view-data')


@app.route('/delete-data/<int:id>', methods=['GET'])
def delete_data(id):
    # Delete the record from the database by ID
    conn = sqlite3.connect('store_Information.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM store_Information WHERE store_Number = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_data'))  # Redirect to the view_data page after deletion

if __name__ == '__main__':
    app.run(debug=True)

