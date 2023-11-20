
# Networks Lab   

authors are aman.gupta@iitgn.ac.in and rugved.patil@iitgn.ac.in






## Part One

#### 

```
sudo python3 part\ 1\ default.py
```

```
sudo python3 part\ 1\ clockwise.py
```

| Routing Congiuration     | Description                |
| :----------------------- | :------------------------- |
| `part 1 default.py`      | h1 -> rA -> rB -> h5             |
| `part 1 clockwise.py`    | h1 -> rA -> rB -> rC -> h5       |

## Part Two

```
sudo python3 part\ 2.py --config b --scheme reno --loss 1
```

| Parameter     | Description                       |
| :--------------- | :-------------------------------- |
| `--config` | **Required** One of (b, c) |
| `--scheme` | **NOT Required** One of (reno, cubic, vegas, bbr)|
|`--loss`|**NOT Required** % of loss between 1 and 100|



