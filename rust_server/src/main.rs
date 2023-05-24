use util;
//use server;
use log;
use env_logger;

fn main() {

    env_logger::init();
    log::debug!("Result: {0}", util::build_db::add(5, 5));

/*
    let server_init = server::server::run();
    match server_init {
        Ok(server_init) => {
            log::info!("Successfully initialized server: {:?}", server_init);
        }
        Err(err) => {
            log::error!("Unable to initialize server: {}", err);
        }
    };        
*/

    log::info!("Exiting...");
}