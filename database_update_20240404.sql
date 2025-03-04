ALTER TABLE atb ADD relatedtypes TEXT DEFAULT NULL AFTER relatedaids,
  ADD tags TEXT DEFAULT NULL AFTER relatedtypes,
  ADD tagids TEXT DEFAULT NULL AFTER tags,
  ADD tagweights TEXT DEFAULT NULL AFTER tagids,
  ADD agerestricted TINYINT DEFAULT NULL AFTER tagweights;
