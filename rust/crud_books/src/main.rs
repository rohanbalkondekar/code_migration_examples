use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use serde::{Deserialize, Serialize};
use std::sync::Mutex;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Book {
    id: Option<usize>,
    title: String,
    author: String,
    published_year: i32,
}

struct AppState {
    books_db: Mutex<Vec<Book>>,
}

async fn create_book(data: web::Data<AppState>, book: web::Json<Book>) -> impl Responder {
    let mut books = data.books_db.lock().unwrap();
    let mut new_book = book.into_inner();
    new_book.id = Some(books.len() + 1);
    books.push(new_book.clone());
    HttpResponse::Ok().json(new_book)
}

async fn read_books(data: web::Data<AppState>) -> impl Responder {
    let books = data.books_db.lock().unwrap();
    HttpResponse::Ok().json(books.to_vec())
}

async fn read_book(data: web::Data<AppState>, path: web::Path<usize>) -> impl Responder {
    let book_id = path.into_inner();
    let books = data.books_db.lock().unwrap();
    if let Some(book) = books.iter().find(|b| b.id == Some(book_id)) {
        HttpResponse::Ok().json(book)
    } else {
        HttpResponse::NotFound().body("Book not found")
    }
}

async fn update_book(data: web::Data<AppState>, path: web::Path<usize>, book: web::Json<Book>) -> impl Responder {
    let book_id = path.into_inner();
    let mut books = data.books_db.lock().unwrap();
    if let Some(existing_book) = books.iter_mut().find(|b| b.id == Some(book_id)) {
        existing_book.title = book.title.clone();
        existing_book.author = book.author.clone();
        existing_book.published_year = book.published_year;
        HttpResponse::Ok().json(existing_book)
    } else {
        HttpResponse::NotFound().body("Book not found")
    }
}

async fn delete_book(data: web::Data<AppState>, path: web::Path<usize>) -> impl Responder {
    let book_id = path.into_inner();
    let mut books = data.books_db.lock().unwrap();
    let initial_len = books.len();
    books.retain(|b| b.id != Some(book_id));
    if books.len() < initial_len {
        HttpResponse::Ok().json(serde_json::json!({"message": "Book deleted successfully"}))
    } else {
        HttpResponse::NotFound().body("Book not found")
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let app_state = web::Data::new(AppState {
        books_db: Mutex::new(Vec::new()),
    });

    HttpServer::new(move || {
        App::new()
            .app_data(app_state.clone())
            .route("/books", web::post().to(create_book))
            .route("/books", web::get().to(read_books))
            .route("/books/{book_id}", web::get().to(read_book))
            .route("/books/{book_id}", web::put().to(update_book))
            .route("/books/{book_id}", web::delete().to(delete_book))
    })
    .bind("0.0.0.0:8000")?
    .run()
    .await
}