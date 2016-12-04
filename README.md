# RR Lyrae Binary Classifier
Binary classifier for RR Lyrae Stars meant for use with the lsst-event-broker framework.

## Usage
In order to use this program you must first install `period04` using `period04-v1.2.0-co140-linux-64bit.sh`, and you must install the `lsstbroker` library.

Then in order to download this program, you should run the following commands.

```bash
$ git clone https://github.com/CSC380Team8/RR-Lyrae-Binary-Classifier.git
$ cd RR-Lyrae-Binary-Classifier
```

In order to run the program, you need to run the `__main__.py` file in the `rrlyrae` directory and supply it the data files you want it to process.

```bash
$ python rrlyrae/__main__.py *.dat
```

You then need to supply the program with the database name, username, and password for the local MySQL database you are working with, and it will then being processing the data files.
