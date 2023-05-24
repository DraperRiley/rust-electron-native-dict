#!/usr/bin/env bash
echo -e "Starting Electron app."
npm start --silent --prefix electron_ui/ & 1> /dev/null
RUST_LOG=trace cargo run -q --manifest-path rust_server/Cargo.toml