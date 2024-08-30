const autoBind = require('auto-bind');

class PlaylistsHandler {
    constructor(service, validator) {
        this._service = service;
        this._validator = validator;

        autoBind(this);
    }

    async postPlaylistHandler(request, h) {
        this._validator.validatePostPlaylistPayload(request.payload);

        const payload = {...request.payload, owner:  request.auth.credentials.id};

        const playlistId = await this._service.addPlaylist(payload);

        const response = h.response({
            status:'success',
            message: 'Playlist berhasil ditambahkan',
            data: { playlistId }
        });
        response.code(201);
        return response;
    }

    async getPlaylistsHandler(request) {
        const { id: owner } = request.auth.credentials;
        const playlists = await this._service.getPlaylists(owner);
        return {
            status:'success',
            data: { playlists }
        };
    }

    async deletePlaylistHandler(request) {
        const { id } = request.params;
        const { id: owner } = request.auth.credentials;
        await this._service.deletePlaylist(id, owner);
        return {
            status:'success',
            message: 'Playlist berhasil dihapus'
        }
    }

    async postSongToPlaylist(request, h) {
        const { id: playlistId } = request.params;
        const { id: owner } = request.auth.credentials;
        const { songId } = request.payload;

        this._validator.validatePostPlaylistSongPayload(request.payload);
        const playlistSongId = await this._service.addSongToPlaylist(playlistId, owner, songId);

        const response = h.response({
            status:'success',
            message: 'Lagu berhasil ditambahkan ke playlist',
            data: { playlistSongId }
        });

        response.code(201);
        return response;
    }

    async getSongsFromPlaylist(request) {
        const { id: playlistId } = request.params;
        const { id: owner } = request.auth.credentials;

        this._validator.validatePostPlaylistSongPayload(request.payload);
        const playlist = await this._service.getSongsFromPlaylist(playlistId, owner);

        return {
            status:'success',
            data: { playlist }
        };
    }

    async deleteSongFromPlaylist(request) {
        const { id: playlistId } = request.params;
        const { id: owner } = request.auth.credentials;
        const { songId } = request.payload;

        this._validator.validatePostPlaylistSongPayload(request.payload);
        await this._service.removeSongFromPlaylist(playlistId, owner, songId);

        return {
            status:'success',
            message: 'Lagu berhasil dihapus dari playlist'
        };
    }
}

module.exports = PlaylistsHandler;