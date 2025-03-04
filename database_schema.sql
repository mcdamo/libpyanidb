CREATE TABLE `atb` (
  `aid` mediumint(8) unsigned NOT NULL default '0',
  `totaleps` smallint(5) unsigned default NULL,
  `eps` smallint(5) unsigned default NULL,
  `specials` smallint(5) unsigned default NULL,
  `rating` smallint(5) unsigned default NULL,
  `votes` mediumint(8) unsigned default NULL,
  `temprating` smallint(5) unsigned default NULL,
  `tempvotes` mediumint(8) unsigned default NULL,
  `reviewrating` smallint(5) unsigned default NULL,
  `reviews` mediumint(8) unsigned default NULL,
  `aired` bigint(20) default NULL,
  `ended` bigint(20) default NULL,
  `apid` text,
  `annid` text,
  `allcid` text,
  `anfoid` text,
  `url` text,
  `pic` text,
  `year` tinytext,
  `type` tinytext,
  `romaji` text,
  `kanji` text,
  `name` text,
  `othername` text,
  `shortnames` text,
  `synonyms` text,
  `categories` text,
  `relatedaids` text,
  `relatedtypes` TEXT DEFAULT NULL,
  `tags` TEXT DEFAULT NULL,
  `tagids` TEXT DEFAULT NULL,
  `tagweights` TEXT DEFAULT NULL,
  `agerestricted` TINYINT DEFAULT,
  `producernames` text,
  `producerids` text,
  `awards` text,
  `status` int(10) unsigned default NULL,
  PRIMARY KEY  (`aid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `dtb` (
  `did` mediumint(8) unsigned NOT NULL default '0',
  `name` text,
  `status` int(10) unsigned default NULL,
  PRIMARY KEY  (`did`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `etb` (
  `eid` int(10) unsigned NOT NULL default '0',
  `aid` mediumint(8) unsigned default NULL,
  `length` smallint(5) unsigned default NULL,
  `rating` smallint(5) unsigned default NULL,
  `votes` mediumint(8) unsigned default NULL,
  `epno` tinytext,
  `name` text,
  `romaji` text,
  `kanji` text,
  `status` int(10) unsigned default NULL,
  PRIMARY KEY  (`eid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `ftb` (
  `fid` bigint(20) unsigned NOT NULL default '0',
  `aid` mediumint(8) unsigned default NULL,
  `eid` int(10) unsigned default NULL,
  `gid` mediumint(8) unsigned default NULL,
  `lid` bigint(20) unsigned default NULL,
  `state` mediumint(8) unsigned default NULL,
  `size` bigint(20) unsigned default NULL,
  `ed2k` text,
  `md5` text,
  `sha1` text,
  `crc32` text,
  `dublang` text,
  `sublang` text,
  `quality` text,
  `source` text,
  `audiocodec` text,
  `audiobitrate` mediumint(8) unsigned default NULL,
  `videocodec` text,
  `videobitrate` mediumint(8) unsigned default NULL,
  `resolution` text,
  `filetype` text,
  `length` mediumint(8) unsigned default NULL,
  `description` text,
  `filename` mediumtext,
  `status` int(10) unsigned default NULL,
  PRIMARY KEY  (`fid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `gtb` (
  `gid` mediumint(8) unsigned default NULL,
  `rating` smallint(5) unsigned default NULL,
  `votes` mediumint(8) unsigned default NULL,
  `animes` mediumint(8) unsigned default NULL,
  `files` bigint(20) unsigned default NULL,
  `name` text,
  `shortname` text,
  `ircchannel` text,
  `ircserver` text,
  `url` text,
  `status` int(10) unsigned default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `jtb` (
  `did` mediumint(8) unsigned default NULL,
  `orig` text,
  `name` text,
  `ed2k` text,
  `md5` text,
  `sha1` text,
  `crc32` text,
  `size` bigint(20) unsigned default NULL,
  `fid` bigint(20) unsigned default NULL,
  `lid` bigint(20) unsigned default NULL,
  `uid` mediumint(8) unsigned default NULL,
  `status` int(10) unsigned default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `ltb` (
  `lid` bigint(20) unsigned default NULL,
  `fid` bigint(20) unsigned default NULL,
  `eid` int(10) unsigned default NULL,
  `aid` mediumint(8) unsigned default NULL,
  `gid` mediumint(8) unsigned default NULL,
  `date` bigint(20) unsigned default NULL,
  `state` tinyint(3) unsigned default NULL,
  `viewdate` bigint(20) unsigned default NULL,
  `storage` text,
  `source` text,
  `other` text,
  `status` int(10) unsigned default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `ptb` (
  `pid` mediumint(8) unsigned default NULL,
  `name` text,
  `shortname` text,
  `othername` text,
  `type` text,
  `pic` text,
  `url` text,
  `status` int(10) unsigned default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
