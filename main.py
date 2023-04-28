from flask import Flask, g, jsonify, request
import psycopg2

app = Flask(__name__)

# Configuración de la conexión a la base de datos

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = psycopg2.connect(
                                user="postgres",
                                password="PIKqPhxx35Ymhm3MIgdR",
                                host="containers-us-west-17.railway.app",
                                port="5679",
                                database="railway"
                                )
    return db

@app.teardown_appcontext
def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

# Ruta para la página de inicio

@app.route('/', methods=['GET'])
def home():
     conn = get_db()
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM books_table")
     totalRows = cursor.fetchall()
     
     num_libros = len(totalRows)

     cursor.close()

     home_display = f"""
     <h1>API Libros
     </h1><p>Esta es una API que contiene {num_libros} libros.</p>"""

     return home_display


# 1.Ruta para obtener todos los libros

@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books_table")
    books = cursor.fetchall()

    cursor.close()

    return jsonify(books)

# 2.Ruta para añadir un libro
@app.route('/resources/book/add', methods = ['POST'])
def add_book():

    # Obtener datos del cuerpo de la peticion
    book = request.get_json()

    #Obtenemos los datos del libro a traves de los parametros de la peticion
    author= request.args.get('author')

    # Almacenar los datos en variables
    author = book['author']
    year = book['year']
    title = book['title']
    description = book['description']
    id_book = book['id']

    # Crear la conexion a la base de datos
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books_table (id, author, year, title, description) VALUES (%s, %s, %s, %s, %s)", (id_book, author, year, title, description))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'El libro ha sido añadido correctamente'})


# 3. Ruta para eliminar un libro por su id
@app.route('/resources/book/delete/<int:id>', methods = ['DELETE'])
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books_table WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    
    return jsonify({'message': 'El libro ha sido eliminado correctamente'})

# 4. Ruta para actualizar un libro 
@app.route('/resources/book/update/', methods = ['PUT'])
def update_book():
     title = request.args['title']
     year = request.args['year']

     conn = get_db()
     cursor = conn.cursor()
     cursor.execute("UPDATE books_table SET year = %s WHERE title = %s", (year, title))
     conn.commit()
     cursor.close()
     
     return jsonify({'message': 'El libro ha sido actualizado correctamente'})


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)