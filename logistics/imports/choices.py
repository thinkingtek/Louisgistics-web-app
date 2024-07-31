EMAIL_SUBJECTS = (
    ('', 'Email Subject'),
    ('complain', 'Complain'),
    ('testimonial', 'Testimonial'),
    ('inquiry', 'Inquiry'),
    ('others', 'Others'),
)
STATUS = (
    ('', 'Status (intransit/delivered)'),
    ('in-transit', 'In-Transit'),
    ('delivered', 'Delivered'),
    ('packaging', 'Packaging'),
    ('not-shipped', 'Not Shipped'),
)
UNIT_OF_MEASUREMENT = (
    ('', 'Kg/Lbs'),
    ('l', 'L'),
    ('kg', 'Kg'),
    ('lbs', 'lbs')
)
SUBSTANCE_TYPE = (
    ('', 'Liquid/Solid'),
    ('liquid', 'Liquid'),
    ('solid', 'Solid'),
    ('both', 'Both')
)
TRANSPORT_METHOD = (
    ('', 'Select (Air/Land)'),
    ('air', 'Air'),
    ('land', 'Land'),
    ('water', 'Water')
)

states_options = (
    ('', '- Choose State -'),
    ('delta', 'Delta'),
    ('bayelsa', 'Bayelsa'),
    ('rivers', 'Rivers'),
    ('abuja', 'Abuja'),
    ('cross-rivers', 'Cross-Rivers'),
    ('akwa-ibom', 'Akwa-Ibom'),
    ('anambra', 'Anambra'),
    ('enugu', 'Enugu'),
    ('imo', 'Imo'),
    ('lagos', 'Lagos'),
    ('ogun', 'Ogun')
)

STATES = sorted(states_options, key=lambda x: x[1])
