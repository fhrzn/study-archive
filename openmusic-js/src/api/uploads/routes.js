const path = require('path');

const routes = (handler) => [
    {
        method: 'POST',
        path: '/albums/{albumId}/covers',
        handler: handler.postUploadAlbumCoverHandler,
        options: {
            payload: {
                allow: 'multipart/form-data',
                multipart: true,
                output: 'stream',
                maxBytes: 512000
            }
        }
    },
    {
        method: 'GET',
        path: '/upload/{param*}',
        handler: {
            directory: {
                path: path.resolve(__dirname, 'file'),
            }
        }
    }
];

module.exports = routes;