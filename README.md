The [main branch](https://github.com/dnzggg/COGNISIM) is working only with the evolution tournament file, and the [Axelrod branch](https://github.com/dnzggg/COGNISIM/tree/Axelrod) with the Axelrod tournament file.

-------
Running
Install Python from https://www.python.org/downloads/release/python-380/.

To install all the dependencies, run:
```bash
pip install -r requirements.txt
```
    

To run the GUI, run:
```bash
python main.py
```

To split event files, run:
```bash
python split_event_file.py
```
This creates a directory of the event file name, and splits the event file into specific agents:

```
.
├───event_file_name
    ├───conductor1
    │   ├───events.pl
    │   └───fluents.pl
    ├───player1
    │   ├───events.pl
    │   └───fluents.pl
    └───player2
        ├───events.pl
        └───fluents.pl
```
