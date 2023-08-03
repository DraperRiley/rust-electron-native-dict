use util;
use server;
use log;
use env_logger;
use std::process;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::fmt;

fn main() {

    // initialize logger
    env_logger::init();

    // start server
    let server_init = server::server::run();
    match server_init {
        Ok(server_init) => {
            log::info!("Successfully initialized server: {:?}", server_init);
        }
        Err(err) => {
            log::error!("Unable to initialize server: {}", err);
        }
    };        

    // end main
    log::info!("Exiting...");
}