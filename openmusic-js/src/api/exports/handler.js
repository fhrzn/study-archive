const autoBind = require('auto-bind');

class ExportsHandler {
    constructor(producersService, playlistsService, validator) {
        this._producersService = producersService;
        this._playlistsService = playlistsService;
        this._validator = validator;

        autoBind(this);
    }

    async postExportPlaylistHandler(request, h) {
        this._validator.validateExportPlaylistPayload(request.payload);
        await this._playlistsService.verifyPlaylistOwner(request.params.playlistId, request.auth.credentials.id);

        const message = {
            playlistId: request.params.playlistId,
            userId: request.auth.credentials.id,
            targetEmail: request.payload.targetEmail,
        };

        await this._producersService.sendMessage('export:playlist', JSON.stringify(message));

        const response = h.response({
            status: 'success',
            message: 'Permintaan anda dalam antrian',
        });
        response.code(201);
        return response;
    }
}

module.exports = ExportsHandler;