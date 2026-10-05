# Disposable harness preparation findings

Initial local runs stopped before producing a final report on three harness mistakes: SQL INSERT had fourteen placeholders for thirteen columns; V7 manifest lookup used a nonexistent topic_manifest key rather than topic; an arithmetic loop shadowed the pasted fixture's sentence-count variable. Fixed each in the V13-only witness; no prior evidence or production file changed. Subsequent complete checks passed. These were harness defects, not Gemini/provider failures or financial calibration observations.
