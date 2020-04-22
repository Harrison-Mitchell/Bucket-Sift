# Bucket Sift
Generates metadata about public S3 bucket files without needing S3 command line tools or credentials.

It outputs:
* Total bucket size
* Total number of files
* Filetype list and occurrences
* 10 newest files
* 10 largest files
* Whether public anonymous uploading is enabled
* A `files.txt` list
* A `tree.txt` of all files + dirs
* A `dirTree.txt` of all dirs

### Dependencies
* Python >= 3.5
* dateutil, xmltodict, requests (`pip install python-dateutil xmltodict requests`)

### Usage
`./sift.py <S3 bucket URL>`

### Example output
```
./sift.py australia-post.s3.amazonaws.com

                   ____
                  (_  _)
        .  .       / /
     .`_._'_..    / /
     \   o   /   / /
      \ /   /  _/ /_ 
`. ~. `\___/'./~.' /.~'`.
.`'`.`.'`'`.~.`'~.`'`.~`
  B u c k e t   S i f t

Pulled 3392 files
3392 files totaling 0.024 GB

Number of files by type ignoring single occurrences
  .js            1947
  .json          308
  .md            283
  .npmignore     60
  .yml           53
  .jpg           21
  .html          9
  .txt           7
  .jshintrc      4
  .png           4
  .eslintignore  4
  .eslintrc      4
  .1             4
  .gif           2
  .log           2
  .js/           2
  .js/test/      2
  .sh            2
  .gitmodules    2
  .targ          2
  .conf          2
  .editorconfig  2
  .coffee        2
  .xml           2
  .markdown      2
  .dat           2

Newest files
  2016-12-06	http://australia-post.s3.amazonaws.com/carded/carded05.jpg
  2016-12-06	http://australia-post.s3.amazonaws.com/carded/carded01.jpg
  2016-12-06	http://australia-post.s3.amazonaws.com/carded/carded02.jpg
  2016-12-06	http://australia-post.s3.amazonaws.com/carded/carded03.jpg
  2016-12-06	http://australia-post.s3.amazonaws.com/carded/carded04.jpg
  2016-11-30	http://australia-post.s3.amazonaws.com/fetch.gif
  2016-11-30	http://australia-post.s3.amazonaws.com/carded/
  2016-11-30	http://australia-post.s3.amazonaws.com/track_statuses/status_unknown.jpg
  2016-11-30	http://australia-post.s3.amazonaws.com/track_statuses/with_driver.jpg
  2016-11-30	http://australia-post.s3.amazonaws.com/track_statuses/added_to_system.jpg

Largest files
  2.048 MB	http://australia-post.s3.amazonaws.com/fetch.gif
  2.048 MB	http://australia-post.s3.amazonaws.com/staging/app/img/fetch.gif
  2.027 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/bignumber.js/test/div.js
  0.842 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/bignumber.js/test/base-out.js
  0.516 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/lodash/lodash.js
  0.358 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/bignumber.js/test/toFraction.js
  0.357 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/bignumber.js/test/times.js
  0.28 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/bignumber.js/test/minus.js
  0.278 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/bignumber.js/test/plus.js
  0.272 MB	http://australia-post.s3.amazonaws.com/staging/node_modules/bignumber.js/test/cmp.js

Anon upload disabled
```