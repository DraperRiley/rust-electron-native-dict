#[allow(unused_imports)]
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder, middleware};
use std;

#[actix_web::main]
pub async fn run() -> std::io::Result<()> {

    HttpServer::new(|| {
        App::new()
            .wrap(middleware::Logger::default())
            .service(hello)
            .service(dick)
    })
    .bind(("192.168.0.245", 8080))?
    .run()
    .await
}

#[get("/")]
async fn hello() -> impl Responder {
    HttpResponse::Ok().body("I cum blood and")
}

#[get("/dick/")]
async fn dick() -> impl Responder {
    HttpResponse::Ok().body("Dicks")
}