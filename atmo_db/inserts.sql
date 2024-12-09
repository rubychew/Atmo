
INSERT into User (username, email, role, password) VALUES ('Username', 'username@domain.com', 'Standard', 'u-password'); 
INSERT into User (username, email, role, password) VALUES ('Adminname', 'adminname@domain.com', 'Admin', 'a-password'); 
INSERT into User (username, email, role, password) VALUES ('Ownername', 'ownername@domain.com', 'Owner', 'o-password'); 

INSERT into Audio_File (title, description, file_type, url, user_id) VALUES ('audio one', 'podcast', 'mp3', 'https://domain.com/audio_one.mp3', 1);
INSERT into Audio_File (title, description, file_type, url, user_id) VALUES ('audio two', 'recording', 'mp3', 'https://domain.com/audio_one.mp3', 2);
INSERT into Audio_File (title, description, file_type, url, user_id) VALUES ('audio three', 'audio from youtube channel', 'mp3', 'https://domain.com/audio_one.mp3', 1);
INSERT into Audio_File (title, description, file_type, url, user_id) VALUES ('some interview', 'podcast', 'mp3', 'https://domain.com/audio_one.mp3', 3);

