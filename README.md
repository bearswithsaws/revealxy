# Revealxy

Reveal the location Reconyx trail cameras that leverage the LTE modem for remote picture uploads.

# Exif Data

Decode the log in the Exif tag MakerNote at offset 970 through 1994 using the bytes `0xd2 0x8b`

![hex editor view of image](docs/hex_editor.png)

MakerNote data at [970:1994]

All MSB set (0x80):

```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 35, 5, 13, 0, 4, 24, 0, 0, 0, 0, 0, 0, 6, 0, 0, 4, 17, 2, 8, 6, 8, 7, 8, 0, 8, 0, 14, 23, 24, 7, 0, 22, 2, 3, 0, 5, 18, 7, 23, 0, 36, 3, 14, 0, 0, 2, 0, 0, 11, 2, 4, 4, 2, 6, 8, 9, 15, 29, 34, 9, 0, 12, 8, 12, 0, 4, 2, 14, 13, 2, 7, 7, 0, 24, 0, 4, 15, 18, 14, 0, 0, 0, 1, 0, 0, 0, 0, 37, 2, 17, 4, 4, 0, 1, 22, 11, 7, 30, 35, 7, 11, 7, 5, 16, 0, 3, 4, 5, 4, 7, 3, 28, 0, 16, 0, 2, 0, 0, 0, 4, 18, 0, 1, 4, 4, 47, 5]

[0:0x7f]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

[0x80:]
[5, 35, 5, 13, 0, 4, 24, 0, 0, 0, 0, 0, 0, 6, 0, 0, 4, 17, 2, 8, 6, 8, 7, 8, 0, 8, 0, 14, 23, 24, 7, 0, 22, 2, 3, 0, 5, 18, 7, 23, 0, 36, 3, 14, 0, 0, 2, 0, 0, 11, 2, 4, 4, 2, 6, 8, 9, 15, 29, 34, 9, 0, 12, 8, 12, 0, 4, 2, 14, 13, 2, 7, 7, 0, 24, 0, 4, 15, 18, 14, 0, 0, 0, 1, 0, 0, 0, 0, 37, 2, 17, 4, 4, 0, 1, 22, 11, 7, 30, 35, 7, 11, 7, 5, 16, 0, 3, 4, 5, 4, 7, 3, 28, 0, 16, 0, 2, 0, 0, 0, 4, 18, 0, 1, 4, 4, 47, 5]
```

# LTE Modem

![Docs](docs/qeng_doc_1.png)
![Docs](docs/qeng_doc_2.png)


```
+QENG: "servingcell","NOCONN","LTE","FDD",311,480,F0A30D,319,2250,4,3,3,3D04,-79,-8,-54,16,44
```

- MCC: 310
- MNC: 480
- CellID: F0A30D / 15770381
- TAC: 3D04 / 15620

```
**MCC**: 311  
**MNC**: 480  
**LAC / TAC**: 3D04 / 15620  
**CID**: F0A30D / 15770381  
**Radio Type**: LTE

**Latitude**: 43.186111  
**Longitude**: -70.893631  
**Range**: 2545 m  
  
_3_ measurements  
**Created**: 2017-02-27T08:08:44.000Z  
**Updated**: 2017-04-15T10:15:59.000Z

Source:
https://opencellid.org/#zoom=18&lat=43.186267&lon=-70.893617
```

# Calculated Locations

## Original trophy location

![Trophy](docs/trophy_location.png)

## Prize Jar

![Prize](docs/prize_jar_location.png)

# Usage

```bash
❯ python revealxy/revealxy.py
[Archive A] Latest image on server: 003361.jpg
Latest image local: 003361.jpg
Syncing... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   
[Archive B] Latest image on server: 000960.jpg
Latest image local: 000960.jpg
Syncing... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   
Extracting cell tower data... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:10
Total images: 3361
Unique data chunnks: 1770
Geo-locating towers... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Extracting cell tower data... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:02
Total images: 862
Unique data chunnks: 223
Geo-locating towers... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Tower Details:
MCC: 311 MNC: 480 TAC: 16898 CellID: 17003523
MCC: 311 MNC: 480 TAC: 3 CellID: 15770390
MCC: 311 MNC: 480 TAC: 15620 CellID: 15770391
MCC: 311 MNC: 480 TAC: 15620 CellID: 15770381
MCC: 310 MNC: 410 TAC: 1027 CellID: 16656649
MCC: 311 MNC: 480 TAC: 15620 CellID: 15770390
MCC: 311 MNC: 480 TAC: 15620 CellID: 15770380
MCC: 311 MNC: 480 TAC: 15620 CellID: 15770370
MCC: 311 MNC: 480 TAC: 976 CellID: 15770390
MCC: 310 MNC: 410 TAC: 1799 CellID: 23149064
MCC: 310 MNC: 410 TAC: 1027 CellID: 16656833
MCC: 310 MNC: 410 TAC: 1027 CellID: 16656813
MCC: 310 MNC: 410 TAC: 1027 CellID: 16656649
MCC: 310 MNC: 410 TAC: 1799 CellID: 23149064
MCC: 310 MNC: 410 TAC: 1027 CellID: 16656650
MCC: 310 MNC: 410 TAC: 1027 CellID: 16656663
Saved map to final_map_.html
```