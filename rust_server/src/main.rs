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

    // path to write pid to
    const HOME_PATH: &str = "../../";

    // initialize logger
    env_logger::init();

    // get pid, and write to file
    let pid: String = std::process::id().to_string();
    log::info!("PID {}", pid);
    let from_string: String = format!("{}pid2.txt", HOME_PATH);
    let path: &Path = Path::new(&from_string);

    let mut file = match File::create(&path) {
        Ok(file) => file,
        Err(e) => {
            log::error!("Unable to create file: {}", e);
            panic!("");
        }
    };

    let pid_out = pid.as_bytes();
    match file.write_all(pid_out) {
        Ok(_) => log::info!("PID written to file: {}", pid),
        Err(e) => {
            log::error!("Unable to write pid to file: {}", e);
            panic!("");
        }
    }

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