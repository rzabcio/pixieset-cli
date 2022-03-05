Tools for Pixieset service
=======================================================

## Install
```
$ git clone git@github.com:rzabcio/pixieset-cli.git
$ cd pixieset-cli
```

If requirements are not installed automatically:
```
$ pip install csv fire pathlib
```

## Prepare files from order CSV file
Download csv file. Launch:
```
python pixieset.py order order-123456.csv --src_dir ../photos --dst_dir ../orders
```
