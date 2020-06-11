const express = require('express')
const path = require('path')
const app = express()
const {spawn} = require('child_process');
const port = 3000
const multipart = require('connect-multiparty');

const multipartMiddleware = multipart({
    uploadDir: './uploads'
});

function runScript(){
    return spawn('py', [
       "-u",
       path.join(__dirname, 'generate_images_from_videos.py')]);
 }

app.post('/api/upload', multipartMiddleware, (req, res) => {
    const subprocess = runScript()
    // print output of script
    subprocess.stdout.on('data', (data) => {
       console.log(`data:${data}`);
    });
    subprocess.stderr.on('data', (data) => {
       console.log(`error:${data}`);
    });
    subprocess.stderr.on('close', () => {
       console.log("Closed");
    });
    res.json({
        'message': 'File uploaded succesfully.'
    });
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`))