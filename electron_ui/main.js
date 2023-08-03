const { app, BrowserWindow } = require('electron')
const { net } = require('electron');

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600
    })

    win.loadFile('index.html')
}

app.whenReady().then(() => {
    createWindow()
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
        
    })

})

let killRustServer = () => {
    try {
        // make a GET request to the rust server
        const data = null;
        const request = net.request('http://localhost:8080/kill_server');
        //const request = net.request('https://www.boredapi.com/api/activity/');

        // electron app dies here after request
        request.on("response", (response) => {
            console.log('Handling json');
            const data = [];
            response.on("data", (chunk) => {
                data.push(chunk);
                console.log(`CHUNK: ${chunk}`);
            })

            // handling
            request.on("end", () => {
                const json = Buffer.concat(data).toString();
                console.log(`JSON: ${json}`);
                app.quit();
            });

            request.on("finish", () => {
                console.log('Request finished');
                resolve(data);
            });

            request.on('abort', () => {
                console.log('Request is Aborted')
            });

            request.on('error', (error) => {
                console.log(`ERROR: ${JSON.stringify(error)}`)
            });

            request.on('close', (error) => {
                console.log('Last Transaction has occurred')
            });

        });

        //app.quit();
        request.end()
    }
    catch(e){
        reject(e);
        //app.quit();
    }
}

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        killRustServer();
    }
})

process.on('uncaughtException', (err) => {
    const messageBoxOptions = {
        type: "error",
        title: "Error in main process"
    };

    console.log("Error: " + err.message);

    // dialog.showMessageBoxSync(messageBoxOptions);
    app.quit();
});