#[allow(unused_imports)]
use actix_web::{error, Error, get, post, web, App, HttpResponse, HttpServer, Responder, middleware, Result};
use std;
use futures::StreamExt;
use serde::{Deserialize, Serialize};
use env_logger;

#[derive(Serialize, Deserialize)]
struct PidObj {
    pid: String,
}

const MAX_SIZE: usize = 262_144;

#[actix_web::main]
pub async fn run() -> std::io::Result<()> {

    let addr: &str = "localhost";
    let port: u16 = 8080;

    log::info!("Server bound to http://{}:{}/", addr, port);

    HttpServer::new(|| {
        App::new()
            .wrap(middleware::Logger::default())
            .service(hello)
            .service(test)
            .service(kill_server)
    })
    .bind((addr, port))?
    .run()
    .await
}

#[get("/")]
async fn hello() -> impl Responder {
    HttpResponse::Ok().body("main entry")
}

#[get("/test")]
async fn test() -> impl Responder {
    HttpResponse::Ok().body("test")
}

#[get("/kill_server")]
async fn kill_server() ->  Result<impl Responder> {

    log::info!("Server received KILL request");
    std::process::exit(1);
    // build obj and fill with pid, send
    let pid: String = std::process::id().to_string();

    let obj = PidObj {
        pid: pid.to_string(),
    };

    Ok(web::Json(obj))
}

