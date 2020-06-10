const express = require('express')
const app = express()
const port = 3000
const multipart = require('connect-multiparty');

const multipartMiddleware = multipart({
    uploadDir: './uploads'
});

app.post('/api/upload', multipartMiddleware, (req, res) => {
    res.json({
        'message': 'File uploaded succesfully.'
    });
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`))