const express = require('express')
const path = require('path')
var cors = require('cors')
const app = express()
app.use(cors())
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
        res.json({
            Success: true
        });
    });
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`))