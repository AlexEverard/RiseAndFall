
# Dictionary
# PK   = ProvId
# Data = (ShtName, LongName , DiceLoc, pid, armies)
# DiceLoc = 2-tuple D12*D6 corresponding to hand-drawn map
PROVINCES = {
    1: ('LUS', 'Lusitania'    , (2, 5), 0, 2),
    2: ('TAR', 'Tarraconensis', (2, 6), 0, 2),
    3: ('BAE', 'Baeticia'     , (3, 1), 0, 2),
    4: ('BLR', 'Balaeric'     , (3, 2), 0, 2),
    5: ('MAU', 'Mauretania'   , (3, 3), 0, 2),
    6: ('AFR', 'Africa'       , (3, 4), 0, 2),
    7: ('ATL', 'Atlas'        , (3, 5), 0, 2),
    8: ('NUM', 'Numidia'      , (3, 6), 0, 2),
}

# When making 'Edge Entry' rolls (D3 * D6), index these to the Province PK
EDGEPROVINCES = {
    1: 8,  # NUM
    2: 6,  # AFR
    3: 5,  # MAU
}

# LINKS is a N-tuple containing 3-tuples
# from_location, to_location, link_type
# to_location should always be > from_location
# link type = 'N'(ormal), 'D'efensible
LINKS = (
    (1, 2, 'N'),  # LUS,TAR
    (1, 3, 'N'),  # LUS,BAE
    (2, 3, 'N'),  # TAR,BAE
    (2, 4, 'Y'),  # TAR,BLR
    (3, 4, 'Y'),  # BAE,BLR
    (3, 5, 'Y'),  # BAE,MAU
    (4, 6, 'Y'),  # BLR,AFR
    (5, 6, 'N'),  # MAU,AFR
    (5, 7, 'N'),  # MAU,ATL
    (6, 7, 'N'),  # AFR,ATL
    (6, 8, 'N'),  # AFR,NUM
    (7, 8, 'N'),  # ATL,NUM
)

# PROVINCE_DISPLAYS  is a N-tuple containing 2-tuples
#      tuple 1 : location
#      tuple 2 : pixel coords for centre of the overlay box
PROVINCE_DISPLAYS = (
     (1, (87 , 553)), # LUS
     (2, (172, 546)), # TAR
     (3, (96 , 639)), # BAE
     (4, (235, 650)), # BLR
     (5, (90 , 755)), # MAU
     (6, (280, 780)), # AFR
     (7, (100, 870)), # ATL
     (8, (300 ,870)), # NUM
)

