import flask
import json

app = flask.Flask(__name__)


# returns the index of an id you are searching for in a list
def get_index(general_list, key, value):
    general_index = None
    for i in range(len(general_list)):
        if value == general_list[i][key]:
            general_index = i
            break
    return general_index


def get_books(author_id, book_list):
    authors_books = []
    id_found = False
    for book in book_list:
        if author_id in book['authors']:
            authors_books.append(book)
            id_found = True
    if id_found:
        return authors_books
    else:
        return flask.abort(404)


def get_authors(author_list, full_list):
    books_authors = []
    for author in full_list:
        if author['id'] in author_list:
            books_authors.append(author)
    return books_authors


with open('./data/authors.json', encoding='utf-8') as author_file:
    authors = json.loads(author_file.read())

with open('./data/books.json', encoding='utf-8') as book_file:
    books = json.loads(book_file.read())

num_books = 0
num_authors = 0
num_editions = 0

for book in books:
    num_books += 1
    for edition in book['editions']:
        num_editions += 1

for author in authors:
    num_authors += 1


@app.route('/')
def index():
    return flask.render_template('index.html', num_authors=num_authors, num_books=num_books, num_editions=num_editions)


@app.route('/authors/')
def show_authors():
    return flask.render_template('authors.html', authors=authors)


@app.route('/authors/<author_id>/')
def show_author(author_id):
    # check if author id is invalid
    # if author_id not in dictionary, render template
    author_index = get_index(authors, 'id', author_id)
    if author_index is None:
        flask.abort(404)
    authors_books = get_books(author_id, books)
    return flask.render_template('author.html', author=authors[author_index], author_id=author_id,
                                 authors_books=authors_books)


@app.route('/books/')
def show_books():
    return flask.render_template('books.html', books=books)


@app.route('/books/<book_id>/')
def show_book(book_id):
    book_index = get_index(books, 'id', book_id)
    if book_index is None:
        flask.abort(404)
    books_authors = get_authors(books[book_index]['authors'], authors)
    for edition in books[book_index]['editions']:
        if 'publish_date' not in edition:
            edition['publish_date'] = 'Publish Date Unavailable'
    return flask.render_template('book.html', books=books, book_id=book_id, book_index=book_index,
                                 books_authors=books_authors)


@app.route('/books/<book_id>/editions/<edition_id>')
def show_edition(book_id, edition_id):
    book_index = get_index(books, 'id', book_id)
    edition_index = get_index(books[book_index]['editions'], 'id', edition_id)
    books_authors = get_authors(books[book_index]['editions'][edition_index]['authors'], authors)
    return flask.render_template('edition.html', books=books, book_id=book_id, book_index=book_index,
                                 books_authors=books_authors, edition_index=edition_index)


@app.errorhandler(404)
def not_found(err):
    return flask.render_template('404.html', path=flask.request.path), 404


if __name__ == '__main__':
    app.run(debug=True)
