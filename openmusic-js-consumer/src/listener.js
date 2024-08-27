const autoBind = require('auto-bind');

class Listener {
    constructor(playlistService, mailSender) {
        this._playlistService = playlistService;
        this._mailSender = mailSender;

        autoBind(this);
    }

    async listen(message) {
        try {
            
            const { playlistId, targetEmail } = JSON.parse(message.content.toString());

            const playlists = await this._playlistService.getPlaylists(playlistId);
            const result = await this._mailSender.sendEmail(targetEmail, JSON.stringify(playlists));
            console.log(result);
            
        } catch (error) {
            console.error(error);
        }
    }
}

module.exports = Listener;