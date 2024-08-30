/**
 * @type {import('node-pg-migrate').ColumnDefinitions | undefined}
 */

/**
 * @param pgm {import('node-pg-migrate').MigrationBuilder}
 * @param run {() => void | undefined}
 * @returns {Promise<void> | void}
 */
exports.up = (pgm) => {
    pgm.createTable('user_album_likes', {
        id:{
            type: 'VARCHAR(50)',
            primaryKey: true,
        },
        user_id: {
            type: 'VARCHAR(50)',
            notNull: true,
        },
        album_id: {
            type: 'VARCHAR(50)',
            notNull: true,
        }
    })

    pgm.addConstraint('user_album_likes', 'fk_user_album_likes.users.id', 'FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE');
    pgm.addConstraint('user_album_likes', 'fk_user_album_likes.albums.id', 'FOREIGN KEY (album_id) REFERENCES albums (id) ON DELETE CASCADE');

};

/**
 * @param pgm {import('node-pg-migrate').MigrationBuilder}
 * @param run {() => void | undefined}
 * @returns {Promise<void> | void}
 */
exports.down = (pgm) => {
    pgm.dropConstraint('user_album_likes', 'fk_user_album_likes.users.id');
    pgm.dropConstraint('user_album_likes', 'fk_user_album_likes.albums.id');
    pgm.dropTable('user_album_likes');
};
