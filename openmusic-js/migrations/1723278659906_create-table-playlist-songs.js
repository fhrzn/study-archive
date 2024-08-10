/**
 * @type {import('node-pg-migrate').ColumnDefinitions | undefined}
 */

/**
 * @param pgm {import('node-pg-migrate').MigrationBuilder}
 * @param run {() => void | undefined}
 * @returns {Promise<void> | void}
 */
exports.up = (pgm) => {
    pgm.createTable('playlist_songs', {
        id: {
            type: 'VARCHAR(50)',
            primaryKey: true,
        },
        playlist_id: {
            type: 'VARCHAR(50)',
            notNull: true,
        },
        song_id: {
            type: 'VARCHAR(50)',
            notNull: true,
        },
    });

    pgm.addConstraint('playlist_songs', 'fk_playlist_songs.playlists.id', 'FOREIGN KEY (playlist_id) REFERENCES playlists ON DELETE CASCADE');
    pgm.addConstraint('playlist_songs', 'fk_playlist_songs.songs.id', 'FOREIGN KEY (song_id) REFERENCES songs ON DELETE CASCADE');
};

/**
 * @param pgm {import('node-pg-migrate').MigrationBuilder}
 * @param run {() => void | undefined}
 * @returns {Promise<void> | void}
 */
exports.down = (pgm) => {
    pgm.dropConstraint('playlist_songs', 'fk_playlist_songs.playlist.id');
    pgm.dropConstraint('playlist_songs', 'fk_playlist_songs.songs.id');
    pgm.dropTable('playlist_songs');
};
