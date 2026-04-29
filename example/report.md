# Pad Ring GDS Generation Report

## Run Settings

- Output GDS: `/home/yongfu/proj/iopad-automation/artifacts/pad_ring.gds`
- Top Cell: `PAD_RING_TOP`
- Mode: `auto`
- Metal Stack: `3lm`
- Placement Method: `even`
- Die Size (um): `2000.0 x 2000.0`

## Placement Summary

- Total instances: `505`
- Real-cell references: `505`
- Abstract fallbacks: `0`

## Instance Kinds

- corner: `4`
- filler: `476`
- pad: `25`

## Cell Usage

| Cell | Count |
|---|---:|
| bi_t | 5 |
| cor | 4 |
| dvdd | 1 |
| dvss | 1 |
| fill1 | 12 |
| fill10 | 318 |
| fill5 | 16 |
| fillnc | 130 |
| in_c | 1 |
| in_s | 17 |

## Fallback Cells

- None

## Per-Instance Placement

| Instance | Cell | Kind | Side | X (um) | Y (um) | Width (um) | Height (um) | Orientation |
|---|---|---|---|---:|---:|---:|---:|---|
| corner_sw | cor | corner | corner_sw | 0.000000 | 0.000000 | 355.000000 | 355.000000 | R0 |
| corner_se | cor | corner | corner_se | 1645.000000 | 0.000000 | 355.000000 | 355.000000 | R90 |
| corner_ne | cor | corner | corner_ne | 1645.000000 | 1645.000000 | 355.000000 | 355.000000 | R180 |
| corner_nw | cor | corner | corner_nw | 0.000000 | 1645.000000 | 355.000000 | 355.000000 | R270 |
| south_filler_0 | fill10 | filler | south | 355.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_1 | fill10 | filler | south | 365.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_2 | fill10 | filler | south | 375.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_3 | fill10 | filler | south | 385.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_4 | fill10 | filler | south | 395.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_5 | fill10 | filler | south | 405.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_6 | fill10 | filler | south | 415.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_7 | fill10 | filler | south | 425.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_8 | fill10 | filler | south | 435.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_9 | fill10 | filler | south | 445.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_10 | fill10 | filler | south | 455.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_11 | fill10 | filler | south | 465.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_12 | fill10 | filler | south | 475.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_13 | fill10 | filler | south | 485.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_14 | fill10 | filler | south | 495.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_15 | fill1 | filler | south | 505.000000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_16 | fill1 | filler | south | 506.000000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_17 | fillnc | filler | south | 507.000000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_18 | fillnc | filler | south | 507.100000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_19 | fillnc | filler | south | 507.200000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_20 | fillnc | filler | south | 507.300000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_21 | fillnc | filler | south | 507.400000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| U_S_IN0 | in_s | pad | south | 507.500000 | 0.000000 | 75.000000 | 350.000000 | R0 |
| south_filler_22 | fill10 | filler | south | 582.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_23 | fill10 | filler | south | 592.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_24 | fill10 | filler | south | 602.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_25 | fill10 | filler | south | 612.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_26 | fill10 | filler | south | 622.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_27 | fill10 | filler | south | 632.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_28 | fill10 | filler | south | 642.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_29 | fill10 | filler | south | 652.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_30 | fill10 | filler | south | 662.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_31 | fill10 | filler | south | 672.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_32 | fill10 | filler | south | 682.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_33 | fill10 | filler | south | 692.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_34 | fill10 | filler | south | 702.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_35 | fill10 | filler | south | 712.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_36 | fill10 | filler | south | 722.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_37 | fill1 | filler | south | 732.500000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_38 | fill1 | filler | south | 733.500000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_39 | fillnc | filler | south | 734.500000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_40 | fillnc | filler | south | 734.600000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_41 | fillnc | filler | south | 734.700000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_42 | fillnc | filler | south | 734.800000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_43 | fillnc | filler | south | 734.900000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| U_S_IN1 | in_s | pad | south | 735.000000 | 0.000000 | 75.000000 | 350.000000 | R0 |
| south_filler_44 | fill10 | filler | south | 810.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_45 | fill10 | filler | south | 820.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_46 | fill10 | filler | south | 830.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_47 | fill10 | filler | south | 840.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_48 | fill10 | filler | south | 850.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_49 | fill10 | filler | south | 860.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_50 | fill10 | filler | south | 870.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_51 | fill10 | filler | south | 880.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_52 | fill10 | filler | south | 890.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_53 | fill10 | filler | south | 900.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_54 | fill10 | filler | south | 910.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_55 | fill10 | filler | south | 920.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_56 | fill10 | filler | south | 930.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_57 | fill10 | filler | south | 940.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_58 | fill10 | filler | south | 950.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_59 | fill1 | filler | south | 960.000000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_60 | fill1 | filler | south | 961.000000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_61 | fillnc | filler | south | 962.000000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_62 | fillnc | filler | south | 962.100000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_63 | fillnc | filler | south | 962.200000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_64 | fillnc | filler | south | 962.300000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_65 | fillnc | filler | south | 962.400000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| U_S_IN2 | in_s | pad | south | 962.500000 | 0.000000 | 75.000000 | 350.000000 | R0 |
| south_filler_66 | fill10 | filler | south | 1037.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_67 | fill10 | filler | south | 1047.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_68 | fill10 | filler | south | 1057.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_69 | fill10 | filler | south | 1067.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_70 | fill10 | filler | south | 1077.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_71 | fill10 | filler | south | 1087.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_72 | fill10 | filler | south | 1097.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_73 | fill10 | filler | south | 1107.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_74 | fill10 | filler | south | 1117.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_75 | fill10 | filler | south | 1127.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_76 | fill10 | filler | south | 1137.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_77 | fill10 | filler | south | 1147.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_78 | fill10 | filler | south | 1157.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_79 | fill10 | filler | south | 1167.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_80 | fill10 | filler | south | 1177.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_81 | fill1 | filler | south | 1187.500000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_82 | fill1 | filler | south | 1188.500000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_83 | fillnc | filler | south | 1189.500000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_84 | fillnc | filler | south | 1189.600000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_85 | fillnc | filler | south | 1189.700000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_86 | fillnc | filler | south | 1189.800000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_87 | fillnc | filler | south | 1189.900000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| U_S_IN3 | in_s | pad | south | 1190.000000 | 0.000000 | 75.000000 | 350.000000 | R0 |
| south_filler_88 | fill10 | filler | south | 1265.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_89 | fill10 | filler | south | 1275.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_90 | fill10 | filler | south | 1285.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_91 | fill10 | filler | south | 1295.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_92 | fill10 | filler | south | 1305.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_93 | fill10 | filler | south | 1315.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_94 | fill10 | filler | south | 1325.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_95 | fill10 | filler | south | 1335.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_96 | fill10 | filler | south | 1345.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_97 | fill10 | filler | south | 1355.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_98 | fill10 | filler | south | 1365.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_99 | fill10 | filler | south | 1375.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_100 | fill10 | filler | south | 1385.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_101 | fill10 | filler | south | 1395.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_102 | fill10 | filler | south | 1405.000000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_103 | fill1 | filler | south | 1415.000000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_104 | fill1 | filler | south | 1416.000000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_105 | fillnc | filler | south | 1417.000000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_106 | fillnc | filler | south | 1417.100000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_107 | fillnc | filler | south | 1417.200000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_108 | fillnc | filler | south | 1417.300000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_109 | fillnc | filler | south | 1417.400000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| U_S_IN4 | in_s | pad | south | 1417.500000 | 0.000000 | 75.000000 | 350.000000 | R0 |
| south_filler_110 | fill10 | filler | south | 1492.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_111 | fill10 | filler | south | 1502.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_112 | fill10 | filler | south | 1512.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_113 | fill10 | filler | south | 1522.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_114 | fill10 | filler | south | 1532.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_115 | fill10 | filler | south | 1542.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_116 | fill10 | filler | south | 1552.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_117 | fill10 | filler | south | 1562.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_118 | fill10 | filler | south | 1572.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_119 | fill10 | filler | south | 1582.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_120 | fill10 | filler | south | 1592.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_121 | fill10 | filler | south | 1602.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_122 | fill10 | filler | south | 1612.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_123 | fill10 | filler | south | 1622.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_124 | fill10 | filler | south | 1632.500000 | 0.000000 | 10.000000 | 350.000000 | R0 |
| south_filler_125 | fill1 | filler | south | 1642.500000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_126 | fill1 | filler | south | 1643.500000 | 0.000000 | 1.000000 | 350.000000 | R0 |
| south_filler_127 | fillnc | filler | south | 1644.500000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_128 | fillnc | filler | south | 1644.600000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_129 | fillnc | filler | south | 1644.700000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_130 | fillnc | filler | south | 1644.800000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| south_filler_131 | fillnc | filler | south | 1644.900000 | 0.000000 | 0.100000 | 350.000000 | R0 |
| north_filler_0 | fill10 | filler | north | 355.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_1 | fill10 | filler | north | 365.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_2 | fill10 | filler | north | 375.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_3 | fill10 | filler | north | 385.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_4 | fill10 | filler | north | 395.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_5 | fill10 | filler | north | 405.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_6 | fill10 | filler | north | 415.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_7 | fill10 | filler | north | 425.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_8 | fill10 | filler | north | 435.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_9 | fill10 | filler | north | 445.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_10 | fill10 | filler | north | 455.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_11 | fill10 | filler | north | 465.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| U_N_IN0 | in_c | pad | north | 475.000000 | 1650.000000 | 75.000000 | 350.000000 | R180 |
| north_filler_12 | fill10 | filler | north | 550.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_13 | fill10 | filler | north | 560.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_14 | fill10 | filler | north | 570.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_15 | fill10 | filler | north | 580.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_16 | fill10 | filler | north | 590.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_17 | fill10 | filler | north | 600.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_18 | fill10 | filler | north | 610.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_19 | fill10 | filler | north | 620.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_20 | fill10 | filler | north | 630.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_21 | fill10 | filler | north | 640.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_22 | fill10 | filler | north | 650.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_23 | fill10 | filler | north | 660.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| U_N_IO0 | bi_t | pad | north | 670.000000 | 1650.000000 | 75.000000 | 350.000000 | R180 |
| north_filler_24 | fill10 | filler | north | 745.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_25 | fill10 | filler | north | 755.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_26 | fill10 | filler | north | 765.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_27 | fill10 | filler | north | 775.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_28 | fill10 | filler | north | 785.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_29 | fill10 | filler | north | 795.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_30 | fill10 | filler | north | 805.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_31 | fill10 | filler | north | 815.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_32 | fill10 | filler | north | 825.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_33 | fill10 | filler | north | 835.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_34 | fill10 | filler | north | 845.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_35 | fill10 | filler | north | 855.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| U_N_IO1 | bi_t | pad | north | 865.000000 | 1650.000000 | 75.000000 | 350.000000 | R180 |
| north_filler_36 | fill10 | filler | north | 940.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_37 | fill10 | filler | north | 950.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_38 | fill10 | filler | north | 960.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_39 | fill10 | filler | north | 970.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_40 | fill10 | filler | north | 980.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_41 | fill10 | filler | north | 990.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_42 | fill10 | filler | north | 1000.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_43 | fill10 | filler | north | 1010.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_44 | fill10 | filler | north | 1020.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_45 | fill10 | filler | north | 1030.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_46 | fill10 | filler | north | 1040.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_47 | fill10 | filler | north | 1050.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| U_N_IO2 | bi_t | pad | north | 1060.000000 | 1650.000000 | 75.000000 | 350.000000 | R180 |
| north_filler_48 | fill10 | filler | north | 1135.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_49 | fill10 | filler | north | 1145.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_50 | fill10 | filler | north | 1155.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_51 | fill10 | filler | north | 1165.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_52 | fill10 | filler | north | 1175.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_53 | fill10 | filler | north | 1185.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_54 | fill10 | filler | north | 1195.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_55 | fill10 | filler | north | 1205.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_56 | fill10 | filler | north | 1215.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_57 | fill10 | filler | north | 1225.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_58 | fill10 | filler | north | 1235.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_59 | fill10 | filler | north | 1245.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| U_N_IO3 | bi_t | pad | north | 1255.000000 | 1650.000000 | 75.000000 | 350.000000 | R180 |
| north_filler_60 | fill10 | filler | north | 1330.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_61 | fill10 | filler | north | 1340.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_62 | fill10 | filler | north | 1350.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_63 | fill10 | filler | north | 1360.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_64 | fill10 | filler | north | 1370.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_65 | fill10 | filler | north | 1380.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_66 | fill10 | filler | north | 1390.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_67 | fill10 | filler | north | 1400.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_68 | fill10 | filler | north | 1410.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_69 | fill10 | filler | north | 1420.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_70 | fill10 | filler | north | 1430.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_71 | fill10 | filler | north | 1440.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| U_N_IO4 | bi_t | pad | north | 1450.000000 | 1650.000000 | 75.000000 | 350.000000 | R180 |
| north_filler_72 | fill10 | filler | north | 1525.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_73 | fill10 | filler | north | 1535.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_74 | fill10 | filler | north | 1545.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_75 | fill10 | filler | north | 1555.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_76 | fill10 | filler | north | 1565.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_77 | fill10 | filler | north | 1575.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_78 | fill10 | filler | north | 1585.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_79 | fill10 | filler | north | 1595.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_80 | fill10 | filler | north | 1605.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_81 | fill10 | filler | north | 1615.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_82 | fill10 | filler | north | 1625.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| north_filler_83 | fill10 | filler | north | 1635.000000 | 1650.000000 | 10.000000 | 350.000000 | R180 |
| west_filler_0 | fill10 | filler | west | 0.000000 | 355.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_1 | fill10 | filler | west | 0.000000 | 365.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_2 | fill10 | filler | west | 0.000000 | 375.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_3 | fill10 | filler | west | 0.000000 | 385.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_4 | fill10 | filler | west | 0.000000 | 395.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_5 | fill10 | filler | west | 0.000000 | 405.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_6 | fill10 | filler | west | 0.000000 | 415.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_7 | fill10 | filler | west | 0.000000 | 425.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_8 | fill10 | filler | west | 0.000000 | 435.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_9 | fill5 | filler | west | 0.000000 | 445.000000 | 350.000000 | 5.000000 | R270 |
| west_filler_10 | fillnc | filler | west | 0.000000 | 450.000000 | 350.000000 | 0.100000 | R270 |
| west_filler_11 | fillnc | filler | west | 0.000000 | 450.100000 | 350.000000 | 0.100000 | R270 |
| west_filler_12 | fillnc | filler | west | 0.000000 | 450.200000 | 350.000000 | 0.100000 | R270 |
| west_filler_13 | fillnc | filler | west | 0.000000 | 450.300000 | 350.000000 | 0.100000 | R270 |
| west_filler_14 | fillnc | filler | west | 0.000000 | 450.400000 | 350.000000 | 0.100000 | R270 |
| west_filler_15 | fillnc | filler | west | 0.000000 | 450.500000 | 350.000000 | 0.100000 | R270 |
| west_filler_16 | fillnc | filler | west | 0.000000 | 450.600000 | 350.000000 | 0.100000 | R270 |
| U_W_GND | dvss | pad | west | 0.000000 | 450.700000 | 350.000000 | 75.000000 | R270 |
| west_filler_17 | fill10 | filler | west | 0.000000 | 525.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_18 | fill10 | filler | west | 0.000000 | 535.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_19 | fill10 | filler | west | 0.000000 | 545.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_20 | fill10 | filler | west | 0.000000 | 555.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_21 | fill10 | filler | west | 0.000000 | 565.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_22 | fill10 | filler | west | 0.000000 | 575.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_23 | fill10 | filler | west | 0.000000 | 585.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_24 | fill10 | filler | west | 0.000000 | 595.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_25 | fill10 | filler | west | 0.000000 | 605.700000 | 350.000000 | 10.000000 | R270 |
| west_filler_26 | fill5 | filler | west | 0.000000 | 615.700000 | 350.000000 | 5.000000 | R270 |
| west_filler_27 | fillnc | filler | west | 0.000000 | 620.700000 | 350.000000 | 0.100000 | R270 |
| west_filler_28 | fillnc | filler | west | 0.000000 | 620.800000 | 350.000000 | 0.100000 | R270 |
| west_filler_29 | fillnc | filler | west | 0.000000 | 620.900000 | 350.000000 | 0.100000 | R270 |
| west_filler_30 | fillnc | filler | west | 0.000000 | 621.000000 | 350.000000 | 0.100000 | R270 |
| west_filler_31 | fillnc | filler | west | 0.000000 | 621.100000 | 350.000000 | 0.100000 | R270 |
| west_filler_32 | fillnc | filler | west | 0.000000 | 621.200000 | 350.000000 | 0.100000 | R270 |
| west_filler_33 | fillnc | filler | west | 0.000000 | 621.300000 | 350.000000 | 0.100000 | R270 |
| U_W_IN0 | in_s | pad | west | 0.000000 | 621.400000 | 350.000000 | 75.000000 | R270 |
| west_filler_34 | fill10 | filler | west | 0.000000 | 696.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_35 | fill10 | filler | west | 0.000000 | 706.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_36 | fill10 | filler | west | 0.000000 | 716.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_37 | fill10 | filler | west | 0.000000 | 726.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_38 | fill10 | filler | west | 0.000000 | 736.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_39 | fill10 | filler | west | 0.000000 | 746.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_40 | fill10 | filler | west | 0.000000 | 756.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_41 | fill10 | filler | west | 0.000000 | 766.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_42 | fill10 | filler | west | 0.000000 | 776.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_43 | fill5 | filler | west | 0.000000 | 786.400000 | 350.000000 | 5.000000 | R270 |
| west_filler_44 | fillnc | filler | west | 0.000000 | 791.400000 | 350.000000 | 0.100000 | R270 |
| west_filler_45 | fillnc | filler | west | 0.000000 | 791.500000 | 350.000000 | 0.100000 | R270 |
| west_filler_46 | fillnc | filler | west | 0.000000 | 791.600000 | 350.000000 | 0.100000 | R270 |
| west_filler_47 | fillnc | filler | west | 0.000000 | 791.700000 | 350.000000 | 0.100000 | R270 |
| west_filler_48 | fillnc | filler | west | 0.000000 | 791.800000 | 350.000000 | 0.100000 | R270 |
| west_filler_49 | fillnc | filler | west | 0.000000 | 791.900000 | 350.000000 | 0.100000 | R270 |
| U_W_IN1 | in_s | pad | west | 0.000000 | 792.000000 | 350.000000 | 75.000000 | R270 |
| west_filler_50 | fill10 | filler | west | 0.000000 | 867.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_51 | fill10 | filler | west | 0.000000 | 877.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_52 | fill10 | filler | west | 0.000000 | 887.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_53 | fill10 | filler | west | 0.000000 | 897.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_54 | fill10 | filler | west | 0.000000 | 907.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_55 | fill10 | filler | west | 0.000000 | 917.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_56 | fill10 | filler | west | 0.000000 | 927.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_57 | fill10 | filler | west | 0.000000 | 937.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_58 | fill10 | filler | west | 0.000000 | 947.000000 | 350.000000 | 10.000000 | R270 |
| west_filler_59 | fill5 | filler | west | 0.000000 | 957.000000 | 350.000000 | 5.000000 | R270 |
| west_filler_60 | fillnc | filler | west | 0.000000 | 962.000000 | 350.000000 | 0.100000 | R270 |
| west_filler_61 | fillnc | filler | west | 0.000000 | 962.100000 | 350.000000 | 0.100000 | R270 |
| west_filler_62 | fillnc | filler | west | 0.000000 | 962.200000 | 350.000000 | 0.100000 | R270 |
| west_filler_63 | fillnc | filler | west | 0.000000 | 962.300000 | 350.000000 | 0.100000 | R270 |
| west_filler_64 | fillnc | filler | west | 0.000000 | 962.400000 | 350.000000 | 0.100000 | R270 |
| west_filler_65 | fillnc | filler | west | 0.000000 | 962.500000 | 350.000000 | 0.100000 | R270 |
| U_W_IN2 | in_s | pad | west | 0.000000 | 962.600000 | 350.000000 | 75.000000 | R270 |
| west_filler_66 | fill10 | filler | west | 0.000000 | 1037.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_67 | fill10 | filler | west | 0.000000 | 1047.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_68 | fill10 | filler | west | 0.000000 | 1057.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_69 | fill10 | filler | west | 0.000000 | 1067.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_70 | fill10 | filler | west | 0.000000 | 1077.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_71 | fill10 | filler | west | 0.000000 | 1087.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_72 | fill10 | filler | west | 0.000000 | 1097.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_73 | fill10 | filler | west | 0.000000 | 1107.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_74 | fill10 | filler | west | 0.000000 | 1117.600000 | 350.000000 | 10.000000 | R270 |
| west_filler_75 | fill5 | filler | west | 0.000000 | 1127.600000 | 350.000000 | 5.000000 | R270 |
| west_filler_76 | fillnc | filler | west | 0.000000 | 1132.600000 | 350.000000 | 0.100000 | R270 |
| west_filler_77 | fillnc | filler | west | 0.000000 | 1132.700000 | 350.000000 | 0.100000 | R270 |
| west_filler_78 | fillnc | filler | west | 0.000000 | 1132.800000 | 350.000000 | 0.100000 | R270 |
| west_filler_79 | fillnc | filler | west | 0.000000 | 1132.900000 | 350.000000 | 0.100000 | R270 |
| west_filler_80 | fillnc | filler | west | 0.000000 | 1133.000000 | 350.000000 | 0.100000 | R270 |
| west_filler_81 | fillnc | filler | west | 0.000000 | 1133.100000 | 350.000000 | 0.100000 | R270 |
| U_W_IN3 | in_s | pad | west | 0.000000 | 1133.200000 | 350.000000 | 75.000000 | R270 |
| west_filler_82 | fill10 | filler | west | 0.000000 | 1208.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_83 | fill10 | filler | west | 0.000000 | 1218.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_84 | fill10 | filler | west | 0.000000 | 1228.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_85 | fill10 | filler | west | 0.000000 | 1238.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_86 | fill10 | filler | west | 0.000000 | 1248.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_87 | fill10 | filler | west | 0.000000 | 1258.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_88 | fill10 | filler | west | 0.000000 | 1268.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_89 | fill10 | filler | west | 0.000000 | 1278.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_90 | fill10 | filler | west | 0.000000 | 1288.200000 | 350.000000 | 10.000000 | R270 |
| west_filler_91 | fill5 | filler | west | 0.000000 | 1298.200000 | 350.000000 | 5.000000 | R270 |
| west_filler_92 | fillnc | filler | west | 0.000000 | 1303.200000 | 350.000000 | 0.100000 | R270 |
| west_filler_93 | fillnc | filler | west | 0.000000 | 1303.300000 | 350.000000 | 0.100000 | R270 |
| west_filler_94 | fillnc | filler | west | 0.000000 | 1303.400000 | 350.000000 | 0.100000 | R270 |
| west_filler_95 | fillnc | filler | west | 0.000000 | 1303.500000 | 350.000000 | 0.100000 | R270 |
| west_filler_96 | fillnc | filler | west | 0.000000 | 1303.600000 | 350.000000 | 0.100000 | R270 |
| west_filler_97 | fillnc | filler | west | 0.000000 | 1303.700000 | 350.000000 | 0.100000 | R270 |
| U_W_IN4 | in_s | pad | west | 0.000000 | 1303.800000 | 350.000000 | 75.000000 | R270 |
| west_filler_98 | fill10 | filler | west | 0.000000 | 1378.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_99 | fill10 | filler | west | 0.000000 | 1388.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_100 | fill10 | filler | west | 0.000000 | 1398.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_101 | fill10 | filler | west | 0.000000 | 1408.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_102 | fill10 | filler | west | 0.000000 | 1418.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_103 | fill10 | filler | west | 0.000000 | 1428.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_104 | fill10 | filler | west | 0.000000 | 1438.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_105 | fill10 | filler | west | 0.000000 | 1448.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_106 | fill10 | filler | west | 0.000000 | 1458.800000 | 350.000000 | 10.000000 | R270 |
| west_filler_107 | fill5 | filler | west | 0.000000 | 1468.800000 | 350.000000 | 5.000000 | R270 |
| west_filler_108 | fillnc | filler | west | 0.000000 | 1473.800000 | 350.000000 | 0.100000 | R270 |
| west_filler_109 | fillnc | filler | west | 0.000000 | 1473.900000 | 350.000000 | 0.100000 | R270 |
| west_filler_110 | fillnc | filler | west | 0.000000 | 1474.000000 | 350.000000 | 0.100000 | R270 |
| west_filler_111 | fillnc | filler | west | 0.000000 | 1474.100000 | 350.000000 | 0.100000 | R270 |
| west_filler_112 | fillnc | filler | west | 0.000000 | 1474.200000 | 350.000000 | 0.100000 | R270 |
| west_filler_113 | fillnc | filler | west | 0.000000 | 1474.300000 | 350.000000 | 0.100000 | R270 |
| U_W_IN5 | in_s | pad | west | 0.000000 | 1474.400000 | 350.000000 | 75.000000 | R270 |
| west_filler_114 | fill10 | filler | west | 0.000000 | 1549.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_115 | fill10 | filler | west | 0.000000 | 1559.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_116 | fill10 | filler | west | 0.000000 | 1569.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_117 | fill10 | filler | west | 0.000000 | 1579.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_118 | fill10 | filler | west | 0.000000 | 1589.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_119 | fill10 | filler | west | 0.000000 | 1599.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_120 | fill10 | filler | west | 0.000000 | 1609.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_121 | fill10 | filler | west | 0.000000 | 1619.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_122 | fill10 | filler | west | 0.000000 | 1629.400000 | 350.000000 | 10.000000 | R270 |
| west_filler_123 | fill5 | filler | west | 0.000000 | 1639.400000 | 350.000000 | 5.000000 | R270 |
| west_filler_124 | fillnc | filler | west | 0.000000 | 1644.400000 | 350.000000 | 0.100000 | R270 |
| west_filler_125 | fillnc | filler | west | 0.000000 | 1644.500000 | 350.000000 | 0.100000 | R270 |
| west_filler_126 | fillnc | filler | west | 0.000000 | 1644.600000 | 350.000000 | 0.100000 | R270 |
| west_filler_127 | fillnc | filler | west | 0.000000 | 1644.700000 | 350.000000 | 0.100000 | R270 |
| west_filler_128 | fillnc | filler | west | 0.000000 | 1644.800000 | 350.000000 | 0.100000 | R270 |
| west_filler_129 | fillnc | filler | west | 0.000000 | 1644.900000 | 350.000000 | 0.100000 | R270 |
| east_filler_0 | fill10 | filler | east | 1650.000000 | 355.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_1 | fill10 | filler | east | 1650.000000 | 365.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_2 | fill10 | filler | east | 1650.000000 | 375.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_3 | fill10 | filler | east | 1650.000000 | 385.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_4 | fill10 | filler | east | 1650.000000 | 395.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_5 | fill10 | filler | east | 1650.000000 | 405.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_6 | fill10 | filler | east | 1650.000000 | 415.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_7 | fill10 | filler | east | 1650.000000 | 425.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_8 | fill10 | filler | east | 1650.000000 | 435.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_9 | fill5 | filler | east | 1650.000000 | 445.000000 | 350.000000 | 5.000000 | R90 |
| east_filler_10 | fillnc | filler | east | 1650.000000 | 450.000000 | 350.000000 | 0.100000 | R90 |
| east_filler_11 | fillnc | filler | east | 1650.000000 | 450.100000 | 350.000000 | 0.100000 | R90 |
| east_filler_12 | fillnc | filler | east | 1650.000000 | 450.200000 | 350.000000 | 0.100000 | R90 |
| east_filler_13 | fillnc | filler | east | 1650.000000 | 450.300000 | 350.000000 | 0.100000 | R90 |
| east_filler_14 | fillnc | filler | east | 1650.000000 | 450.400000 | 350.000000 | 0.100000 | R90 |
| east_filler_15 | fillnc | filler | east | 1650.000000 | 450.500000 | 350.000000 | 0.100000 | R90 |
| east_filler_16 | fillnc | filler | east | 1650.000000 | 450.600000 | 350.000000 | 0.100000 | R90 |
| U_E_PWR | dvdd | pad | east | 1650.000000 | 450.700000 | 350.000000 | 75.000000 | R90 |
| east_filler_17 | fill10 | filler | east | 1650.000000 | 525.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_18 | fill10 | filler | east | 1650.000000 | 535.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_19 | fill10 | filler | east | 1650.000000 | 545.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_20 | fill10 | filler | east | 1650.000000 | 555.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_21 | fill10 | filler | east | 1650.000000 | 565.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_22 | fill10 | filler | east | 1650.000000 | 575.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_23 | fill10 | filler | east | 1650.000000 | 585.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_24 | fill10 | filler | east | 1650.000000 | 595.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_25 | fill10 | filler | east | 1650.000000 | 605.700000 | 350.000000 | 10.000000 | R90 |
| east_filler_26 | fill5 | filler | east | 1650.000000 | 615.700000 | 350.000000 | 5.000000 | R90 |
| east_filler_27 | fillnc | filler | east | 1650.000000 | 620.700000 | 350.000000 | 0.100000 | R90 |
| east_filler_28 | fillnc | filler | east | 1650.000000 | 620.800000 | 350.000000 | 0.100000 | R90 |
| east_filler_29 | fillnc | filler | east | 1650.000000 | 620.900000 | 350.000000 | 0.100000 | R90 |
| east_filler_30 | fillnc | filler | east | 1650.000000 | 621.000000 | 350.000000 | 0.100000 | R90 |
| east_filler_31 | fillnc | filler | east | 1650.000000 | 621.100000 | 350.000000 | 0.100000 | R90 |
| east_filler_32 | fillnc | filler | east | 1650.000000 | 621.200000 | 350.000000 | 0.100000 | R90 |
| east_filler_33 | fillnc | filler | east | 1650.000000 | 621.300000 | 350.000000 | 0.100000 | R90 |
| U_E_IN0 | in_s | pad | east | 1650.000000 | 621.400000 | 350.000000 | 75.000000 | R90 |
| east_filler_34 | fill10 | filler | east | 1650.000000 | 696.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_35 | fill10 | filler | east | 1650.000000 | 706.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_36 | fill10 | filler | east | 1650.000000 | 716.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_37 | fill10 | filler | east | 1650.000000 | 726.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_38 | fill10 | filler | east | 1650.000000 | 736.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_39 | fill10 | filler | east | 1650.000000 | 746.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_40 | fill10 | filler | east | 1650.000000 | 756.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_41 | fill10 | filler | east | 1650.000000 | 766.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_42 | fill10 | filler | east | 1650.000000 | 776.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_43 | fill5 | filler | east | 1650.000000 | 786.400000 | 350.000000 | 5.000000 | R90 |
| east_filler_44 | fillnc | filler | east | 1650.000000 | 791.400000 | 350.000000 | 0.100000 | R90 |
| east_filler_45 | fillnc | filler | east | 1650.000000 | 791.500000 | 350.000000 | 0.100000 | R90 |
| east_filler_46 | fillnc | filler | east | 1650.000000 | 791.600000 | 350.000000 | 0.100000 | R90 |
| east_filler_47 | fillnc | filler | east | 1650.000000 | 791.700000 | 350.000000 | 0.100000 | R90 |
| east_filler_48 | fillnc | filler | east | 1650.000000 | 791.800000 | 350.000000 | 0.100000 | R90 |
| east_filler_49 | fillnc | filler | east | 1650.000000 | 791.900000 | 350.000000 | 0.100000 | R90 |
| U_E_IN1 | in_s | pad | east | 1650.000000 | 792.000000 | 350.000000 | 75.000000 | R90 |
| east_filler_50 | fill10 | filler | east | 1650.000000 | 867.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_51 | fill10 | filler | east | 1650.000000 | 877.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_52 | fill10 | filler | east | 1650.000000 | 887.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_53 | fill10 | filler | east | 1650.000000 | 897.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_54 | fill10 | filler | east | 1650.000000 | 907.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_55 | fill10 | filler | east | 1650.000000 | 917.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_56 | fill10 | filler | east | 1650.000000 | 927.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_57 | fill10 | filler | east | 1650.000000 | 937.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_58 | fill10 | filler | east | 1650.000000 | 947.000000 | 350.000000 | 10.000000 | R90 |
| east_filler_59 | fill5 | filler | east | 1650.000000 | 957.000000 | 350.000000 | 5.000000 | R90 |
| east_filler_60 | fillnc | filler | east | 1650.000000 | 962.000000 | 350.000000 | 0.100000 | R90 |
| east_filler_61 | fillnc | filler | east | 1650.000000 | 962.100000 | 350.000000 | 0.100000 | R90 |
| east_filler_62 | fillnc | filler | east | 1650.000000 | 962.200000 | 350.000000 | 0.100000 | R90 |
| east_filler_63 | fillnc | filler | east | 1650.000000 | 962.300000 | 350.000000 | 0.100000 | R90 |
| east_filler_64 | fillnc | filler | east | 1650.000000 | 962.400000 | 350.000000 | 0.100000 | R90 |
| east_filler_65 | fillnc | filler | east | 1650.000000 | 962.500000 | 350.000000 | 0.100000 | R90 |
| U_E_IN2 | in_s | pad | east | 1650.000000 | 962.600000 | 350.000000 | 75.000000 | R90 |
| east_filler_66 | fill10 | filler | east | 1650.000000 | 1037.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_67 | fill10 | filler | east | 1650.000000 | 1047.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_68 | fill10 | filler | east | 1650.000000 | 1057.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_69 | fill10 | filler | east | 1650.000000 | 1067.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_70 | fill10 | filler | east | 1650.000000 | 1077.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_71 | fill10 | filler | east | 1650.000000 | 1087.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_72 | fill10 | filler | east | 1650.000000 | 1097.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_73 | fill10 | filler | east | 1650.000000 | 1107.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_74 | fill10 | filler | east | 1650.000000 | 1117.600000 | 350.000000 | 10.000000 | R90 |
| east_filler_75 | fill5 | filler | east | 1650.000000 | 1127.600000 | 350.000000 | 5.000000 | R90 |
| east_filler_76 | fillnc | filler | east | 1650.000000 | 1132.600000 | 350.000000 | 0.100000 | R90 |
| east_filler_77 | fillnc | filler | east | 1650.000000 | 1132.700000 | 350.000000 | 0.100000 | R90 |
| east_filler_78 | fillnc | filler | east | 1650.000000 | 1132.800000 | 350.000000 | 0.100000 | R90 |
| east_filler_79 | fillnc | filler | east | 1650.000000 | 1132.900000 | 350.000000 | 0.100000 | R90 |
| east_filler_80 | fillnc | filler | east | 1650.000000 | 1133.000000 | 350.000000 | 0.100000 | R90 |
| east_filler_81 | fillnc | filler | east | 1650.000000 | 1133.100000 | 350.000000 | 0.100000 | R90 |
| U_E_IN3 | in_s | pad | east | 1650.000000 | 1133.200000 | 350.000000 | 75.000000 | R90 |
| east_filler_82 | fill10 | filler | east | 1650.000000 | 1208.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_83 | fill10 | filler | east | 1650.000000 | 1218.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_84 | fill10 | filler | east | 1650.000000 | 1228.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_85 | fill10 | filler | east | 1650.000000 | 1238.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_86 | fill10 | filler | east | 1650.000000 | 1248.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_87 | fill10 | filler | east | 1650.000000 | 1258.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_88 | fill10 | filler | east | 1650.000000 | 1268.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_89 | fill10 | filler | east | 1650.000000 | 1278.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_90 | fill10 | filler | east | 1650.000000 | 1288.200000 | 350.000000 | 10.000000 | R90 |
| east_filler_91 | fill5 | filler | east | 1650.000000 | 1298.200000 | 350.000000 | 5.000000 | R90 |
| east_filler_92 | fillnc | filler | east | 1650.000000 | 1303.200000 | 350.000000 | 0.100000 | R90 |
| east_filler_93 | fillnc | filler | east | 1650.000000 | 1303.300000 | 350.000000 | 0.100000 | R90 |
| east_filler_94 | fillnc | filler | east | 1650.000000 | 1303.400000 | 350.000000 | 0.100000 | R90 |
| east_filler_95 | fillnc | filler | east | 1650.000000 | 1303.500000 | 350.000000 | 0.100000 | R90 |
| east_filler_96 | fillnc | filler | east | 1650.000000 | 1303.600000 | 350.000000 | 0.100000 | R90 |
| east_filler_97 | fillnc | filler | east | 1650.000000 | 1303.700000 | 350.000000 | 0.100000 | R90 |
| U_E_IN4 | in_s | pad | east | 1650.000000 | 1303.800000 | 350.000000 | 75.000000 | R90 |
| east_filler_98 | fill10 | filler | east | 1650.000000 | 1378.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_99 | fill10 | filler | east | 1650.000000 | 1388.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_100 | fill10 | filler | east | 1650.000000 | 1398.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_101 | fill10 | filler | east | 1650.000000 | 1408.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_102 | fill10 | filler | east | 1650.000000 | 1418.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_103 | fill10 | filler | east | 1650.000000 | 1428.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_104 | fill10 | filler | east | 1650.000000 | 1438.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_105 | fill10 | filler | east | 1650.000000 | 1448.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_106 | fill10 | filler | east | 1650.000000 | 1458.800000 | 350.000000 | 10.000000 | R90 |
| east_filler_107 | fill5 | filler | east | 1650.000000 | 1468.800000 | 350.000000 | 5.000000 | R90 |
| east_filler_108 | fillnc | filler | east | 1650.000000 | 1473.800000 | 350.000000 | 0.100000 | R90 |
| east_filler_109 | fillnc | filler | east | 1650.000000 | 1473.900000 | 350.000000 | 0.100000 | R90 |
| east_filler_110 | fillnc | filler | east | 1650.000000 | 1474.000000 | 350.000000 | 0.100000 | R90 |
| east_filler_111 | fillnc | filler | east | 1650.000000 | 1474.100000 | 350.000000 | 0.100000 | R90 |
| east_filler_112 | fillnc | filler | east | 1650.000000 | 1474.200000 | 350.000000 | 0.100000 | R90 |
| east_filler_113 | fillnc | filler | east | 1650.000000 | 1474.300000 | 350.000000 | 0.100000 | R90 |
| U_E_IN5 | in_s | pad | east | 1650.000000 | 1474.400000 | 350.000000 | 75.000000 | R90 |
| east_filler_114 | fill10 | filler | east | 1650.000000 | 1549.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_115 | fill10 | filler | east | 1650.000000 | 1559.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_116 | fill10 | filler | east | 1650.000000 | 1569.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_117 | fill10 | filler | east | 1650.000000 | 1579.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_118 | fill10 | filler | east | 1650.000000 | 1589.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_119 | fill10 | filler | east | 1650.000000 | 1599.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_120 | fill10 | filler | east | 1650.000000 | 1609.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_121 | fill10 | filler | east | 1650.000000 | 1619.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_122 | fill10 | filler | east | 1650.000000 | 1629.400000 | 350.000000 | 10.000000 | R90 |
| east_filler_123 | fill5 | filler | east | 1650.000000 | 1639.400000 | 350.000000 | 5.000000 | R90 |
| east_filler_124 | fillnc | filler | east | 1650.000000 | 1644.400000 | 350.000000 | 0.100000 | R90 |
| east_filler_125 | fillnc | filler | east | 1650.000000 | 1644.500000 | 350.000000 | 0.100000 | R90 |
| east_filler_126 | fillnc | filler | east | 1650.000000 | 1644.600000 | 350.000000 | 0.100000 | R90 |
| east_filler_127 | fillnc | filler | east | 1650.000000 | 1644.700000 | 350.000000 | 0.100000 | R90 |
| east_filler_128 | fillnc | filler | east | 1650.000000 | 1644.800000 | 350.000000 | 0.100000 | R90 |
| east_filler_129 | fillnc | filler | east | 1650.000000 | 1644.900000 | 350.000000 | 0.100000 | R90 |
## Effective Signoff Config

| Item | Value |
|---|---|
| LVS runset | `/home/yongfu/proj/iopad-automation/tools/globalfoundries-pdk-libs-gf180mcu_fd_pr/rules/klayout/lvs/gf180mcu.lvs` |
| LVS log | `/home/yongfu/proj/iopad-automation/artifacts/lvs_check.log` |
| LVS substrate | `gf180mcu_gnd` |
| LVS stack | `3lm` |
| LVS metal_top | `30K` |
| LVS metal_level | `3LM` |
| LVS mim_option | `A` |
| LVS poly_res | `1K` |
| LVS mim_cap | `2` |
| DRC enabled (effective) | `true` |
| DRC runset | `/home/yongfu/proj/iopad-automation/tools/globalfoundries-pdk-libs-gf180mcu_fd_pr/rules/klayout/drc/gf180mcu.drc` |
| DRC log | `/home/yongfu/proj/iopad-automation/artifacts/drc_check.log` |
| DRC run_mode | `flat` |
| DRC feol | `true` |
| DRC beol | `true` |
| DRC offgrid | `true` |
| DRC conn_drc | `false` |
| DRC density | `false` |
| DRC antenna | `false` |
| DRC stack | `3lm` |
| DRC metal_top | `30K` |
| DRC metal_level | `3LM` |
| DRC mim_option | `A` |

## Signoff Verdict

| Check | Verdict |
|---|---|
| DRC clean | `not-clean (9278 violations)` |
| LVS clean | `not-clean (extraction errors)` |

## Signoff Artifacts

| Item | Status | Path |
|---|---|---|
| GDS | generated | `/home/yongfu/proj/iopad-automation/artifacts/pad_ring.gds` |
| Netlist (extracted) | generated | `/home/yongfu/proj/iopad-automation/artifacts/pad_ring_extracted.cir` |
| LVS report DB | failed | `/home/yongfu/proj/iopad-automation/artifacts/pad_ring.lvsdb` |
| DRC report DB | present | `/home/yongfu/proj/iopad-automation/artifacts/pad_ring_drc.lyrdb` |

### Notes

- DRC execution is controlled by `--drc-check/--no-drc-check` (or `--drc/--no-drc`) and `signoff.drc.enabled` in `io.yaml`.
- LVS check in this flow is the layout extraction stage (`--lvs-check/--no-lvs-check` or `--netlist/--no-netlist`).

