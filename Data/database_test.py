# Create nonrelational list of courses
# this is a hack, and may be better
# refactored as a relational database

# optimization is going to get interesting

# Use Strings as unique identifiers to start
# create optimizations later
# quick version ->
# dirty optimization is to index list once
# then replace string identifiers

# Degree coreqs and 
cs_degree_all_courses = [
    "SLS1106", 
    "ENC1101", 
    "IDS1380", 
    "MAC2311", 
    "EGN1007C", 
    "ENC2210", 
    "COP2271C", 
    "MAC2312", 
    "PHY2048",
    "PHY2048L",
    "COP2272C",
    "COP3353C",
    "MAD2014",
    "MAS3114",
    "PHY2049",
    "PHY2049L",
    "COP3330C",
    "COP3710",
    "CDA2108",
    "EEL3702C",
    "STA2023",
    "DIG2520",
    "COP4415",
    "COP4531",
    "MAP2302",
    "MAD3401",
    "CNT3004",
    "IDS4941",
    "CEN4010",
    "CAP4630",
    "EEL4768C",
    "STA3032",
    "CDA3100",
    "COP4610",
    "COP4934C",
    "COP4935C",
    "COP4020",
    "IDS2114"
]

cs_concentration_electives = [
    "COP2034",
    "COP3834C",
    "CEN4088",
    "CAP4122",
    "CEN4213",
    "CIS4369",
    "CNT4409",
    "CAP4410",
    "COP4520",
    "CNT4526",
    "CAP4612",
    "COP4620",
    "COP4656",
    "EEL4664C",
    "CEN4721",
    "CAP4830",
    "COP4930"
]

cs_concentration_cyber_gaming_courses = [
    "CAP4034",
    "CAP4052",
    "CAP4056",
    "CAP4730",
]
cs_concentration_cyber_security_courses = [
    "CIS4203",
    "CIS4204",
    "CIS4362",
    "CIS4367"
]

arts_and_humanities = [
    "ARH2000",
    "PHI2010"
]

# Group one: students are required to take courses from social sciences
# in two different social sciences categories
social_sciences_one = [
    "AMH2010",
    "AMH2020",
    "AMH2930"
]

social_sciences_two = [
    "ECO2013",
    "ECO2023",
    "PSY2012"
]

# on track sheet, listed as "Natural Science Elective"
# named natural_sciences for consistency
natural_sciences = [
    "BSC1010",
    "BSC1010L",
    "CHM2045",
    "CHM2045L"
]