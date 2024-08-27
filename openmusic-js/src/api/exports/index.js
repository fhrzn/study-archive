const ExportsHandler = require('./handler');
const routes = require('./routes');

module.exports = {
    name: 'exports',
    version: '1.0.0',
    register: async (server, { producersService, playlistsService, validator }) => {
        const exportsHandler = new ExportsHandler(producersService, playlistsService, validator);
        server.route(routes(exportsHandler));
    }
}