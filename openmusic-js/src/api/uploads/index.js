const UploadsHandler = require('./handler');
const routes = require('./routes');


module.exports = {
    name: 'uploads',
    version: '1.0.0',
    register: async (server, { uploadService, albumService, validator }) => {
        const uploadsHandler = new UploadsHandler(uploadService, albumService, validator);
        server.route(routes(uploadsHandler));
    }
};