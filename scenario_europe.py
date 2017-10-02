
# Dictionary
PROVINCES = {
    (2,5): ('LUS','Lusitania'),
    (2,6): ('TAR','Tarraconensis'),
    (3,1): ('BAE','Baeticia'),
}

# LINKS is a N-tuple containing 3-tuples
#
# from_location, to_location, link_type
# to_location should always be > from_location
# link type = 'N'(ormal), 'D'efensible
LINKS = (
    ( (2,5), (2,6) ,'N' ),
    ( (2,5), (3,1) ,'N' ),
    ( (2,6), (3,1) ,'N' ),
)

# PROVINCE_DISPLAYS  is a N-tuple containing 2-tuples
#      tuple 1 : location
#      tuple 2 : pixel coords for centre of the overlay box
PROVINCE_DISPLAYS = (
     ( (2,5), ( 87,553) ), # LUS
     ( (2,6), (172,546) ), # TAR
     ( (3,1), ( 96,639) ), # BAE
)