from django.test import TestCase



# api/v1/ [name='api-root']
# api/v1/ <drf_format_suffix:format> [name='api-root']
# api/v1/drf-auth/
# api/v1/auth/ ^users/$ [name='customuser-list']
# api/v1/auth/ ^users\.(?P<format>[a-z0-9]+)/?$ [name='customuser-list']
# api/v1/auth/ ^users/activation/$ [name='customuser-activation']
# api/v1/auth/ ^users/activation\.(?P<format>[a-z0-9]+)/?$ [name='customuser-activation']
# api/v1/auth/ ^users/me/$ [name='customuser-me']
# api/v1/auth/ ^users/me\.(?P<format>[a-z0-9]+)/?$ [name='customuser-me']

# api/v1/auth/ ^users/resend_activation/$ [name='customuser-resend-activation']
# api/v1/auth/ ^users/resend_activation\.(?P<format>[a-z0-9]+)/?$ [name='customuser-resend-activation']

# api/v1/auth/ ^users/reset_password/$ [name='customuser-reset-password']
# api/v1/auth/ ^users/reset_password\.(?P<format>[a-z0-9]+)/?$ [name='customuser-reset-password']
# api/v1/auth/ ^users/reset_password_confirm/$ [name='customuser-reset-password-confirm']
# api/v1/auth/ ^users/reset_password_confirm\.(?P<format>[a-z0-9]+)/?$ [name='customuser-reset-password-confirm']

# api/v1/auth/ ^users/reset_email/$ [name='customuser-reset-username']
# api/v1/auth/ ^users/reset_email\.(?P<format>[a-z0-9]+)/?$ [name='customuser-reset-username']
# api/v1/auth/ ^users/reset_email_confirm/$ [name='customuser-reset-username-confirm']
# api/v1/auth/ ^users/reset_email_confirm\.(?P<format>[a-z0-9]+)/?$ [name='customuser-reset-username-confirm']

# api/v1/auth/ ^users/set_password/$ [name='customuser-set-password']
# api/v1/auth/ ^users/set_password\.(?P<format>[a-z0-9]+)/?$ [name='customuser-set-password']

# api/v1/auth/ ^users/set_email/$ [name='customuser-set-username']
# api/v1/auth/ ^users/set_email\.(?P<format>[a-z0-9]+)/?$ [name='customuser-set-username']
# api/v1/auth/ ^users/(?P<id>[^/.]+)/$ [name='customuser-detail']
# api/v1/auth/ ^users/(?P<id>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='customuser-detail']
# api/v1/auth/ [name='api-root']
# api/v1/auth/ <drf_format_suffix:format> [name='api-root']
# api/v1/auth/ ^jwt/create/? [name='jwt-create']
# api/v1/auth/ ^jwt/refresh/? [name='jwt-refresh']
# api/v1/auth/ ^jwt/verify/? [name='jwt-verify']
# ^auth/
# api/v1/token/ [name='token']
# api/v1/token/refresh/ [name='token_refresh']
# api/v1/token/verify/ [name='token_verify']
# ^media/(?P<path>.*)$
# ^static/(?P<path>.*)$


LazySet = ('NZ-CHAT', 'Europe/Belgrade', 'Asia/Yekaterinburg', 'Europe/San_Marino', 'Singapore', 'Turkey',
         'Antarctica/Vostok', 'America/Phoenix', 'Africa/Maseru', 'Etc/GMT-11', 'Pacific/Pohnpei', 'Pacific/Majuro',
         'Etc/GMT0', 'Asia/Ulaanbaatar', 'Europe/Guernsey', 'Pacific/Auckland', 'Europe/Vatican', 'Africa/Monrovia',
         'Asia/Pyongyang', 'Atlantic/Madeira', 'US/Aleutian', 'Canada/Saskatchewan', 'Asia/Khandyga', 'Australia/NSW',
         'America/Buenos_Aires', 'Asia/Macau', 'Africa/Porto-Novo', 'Asia/Phnom_Penh', 'Etc/GMT-3',
         'Australia/Victoria', 'Etc/GMT+11', 'Asia/Omsk', 'Australia/Yancowinna', 'Asia/Ashgabat', 'Asia/Dili',
         'Asia/Riyadh', 'Etc/GMT-4', 'Australia/Canberra', 'America/Grenada', 'America/Tortola', 'Africa/Bamako',
         'America/Noronha', 'Indian/Kerguelen', 'Africa/Lusaka', 'Europe/Vienna', 'Asia/Hovd', 'Asia/Bishkek',
         'America/Port-au-Prince', 'America/North_Dakota/New_Salem', 'Asia/Ho_Chi_Minh', 'America/Danmarkshavn',
         'America/Cambridge_Bay', 'America/Porto_Velho', 'Europe/Malta', 'Indian/Chagos', 'Asia/Istanbul',
         'Africa/Dar_es_Salaam', 'America/Nome', 'America/Virgin', 'Etc/GMT-13', 'Europe/Minsk', 'America/Yellowknife',
         'Asia/Anadyr', 'Asia/Atyrau', 'America/Campo_Grande', 'Asia/Sakhalin', 'Asia/Kolkata', 'America/Cayman',
         'Atlantic/Stanley', 'Mexico/BajaSur', 'Europe/Moscow', 'Africa/Nouakchott', 'Europe/Astrakhan', 'GMT0',
         'Asia/Qatar', 'PST8PDT', 'Asia/Famagusta', 'Australia/Broken_Hill', 'Europe/Paris', 'Indian/Comoro',
         'America/Argentina/Catamarca', 'US/Eastern', 'America/Indiana/Marengo', 'US/Central', 'Asia/Bangkok',
         'America/Sitka', 'Europe/Podgorica', 'America/Nassau', 'America/Resolute', 'Iran', 'Australia/Hobart',
         'Africa/Brazzaville', 'Pacific/Bougainville', 'America/St_Vincent', 'Universal', 'Africa/Kampala',
         'Europe/Gibraltar', 'Mexico/General', 'Asia/Aden', 'ROC', 'America/Mazatlan', 'EST5EDT', 'America/Toronto',
         'Asia/Vientiane', 'Asia/Qyzylorda', 'Asia/Ashkhabad', 'Asia/Makassar', 'Asia/Thimbu', 'Europe/Kirov',
         'US/Hawaii', 'America/Whitehorse', 'Europe/Volgograd', 'America/Anguilla', 'Etc/Zulu', 'Etc/GMT-2',
         'America/Indiana/Petersburg', 'Asia/Chongqing', 'Etc/GMT-8', 'Asia/Jakarta', 'Asia/Kathmandu',
         'America/Coral_Harbour', 'Africa/Ceuta', 'Asia/Tashkent', 'Libya', 'Atlantic/Canary', 'Asia/Qostanay',
         'America/Mexico_City', 'Pacific/Tahiti', 'America/Eirunepe', 'America/Merida', 'Hongkong', 'Pacific/Fakaofo',
         'Antarctica/Rothera', 'America/Matamoros', 'Africa/Sao_Tome', 'America/Edmonton', 'America/St_Johns',
         'Navajo', 'Africa/Libreville', 'Asia/Almaty', 'America/Recife', 'Asia/Bahrain', 'Iceland', 'Etc/GMT+10',
         'Pacific/Galapagos', 'Asia/Tehran', 'Africa/Kigali', 'Canada/Newfoundland', 'Africa/Lubumbashi',
         'America/Winnipeg', 'Canada/Atlantic', 'Japan', 'America/Blanc-Sablon', 'NZ', 'Antarctica/Mawson',
         'Asia/Amman', 'Etc/Greenwich', 'Europe/Budapest', 'Africa/Lome', 'America/Ensenada', 'America/Dawson_Creek',
         'Antarctica/Davis', 'Africa/Ndjamena', 'Pacific/Apia', 'GB', 'Etc/GMT+4', 'Pacific/Chatham',
         'America/Kentucky/Monticello', 'Chile/EasterIsland', 'America/Argentina/Jujuy', 'Australia/Melbourne',
         'Pacific/Guadalcanal', 'Africa/Mbabane', 'Asia/Dubai', 'Africa/Bangui', 'Europe/Luxembourg',
         'America/Glace_Bay', 'Atlantic/Azores', 'Australia/South', 'Etc/GMT', 'Etc/GMT+7', 'America/Catamarca',
         'Antarctica/McMurdo', 'Atlantic/Cape_Verde', 'Pacific/Wallis', 'Asia/Seoul', 'Antarctica/DumontDUrville',
         'Antarctica/South_Pole', 'Asia/Thimphu', 'Australia/Lord_Howe', 'Pacific/Samoa', 'Africa/Blantyre',
         'America/Nipigon', 'Australia/Eucla', 'Asia/Tokyo', 'Asia/Yakutsk', 'America/Chicago', 'Asia/Katmandu',
         'Africa/Asmara', 'Antarctica/Macquarie', 'Etc/GMT-9', 'Etc/UCT', 'Europe/Kyiv', 'Africa/Windhoek',
         'America/El_Salvador', 'Eire', 'Africa/Gaborone', 'Asia/Taipei', 'Etc/GMT+5', 'Asia/Barnaul', 'America/Rosario',
         'America/Santo_Domingo', 'America/Kentucky/Louisville', 'America/Lower_Princes', 'Canada/Mountain',
         'Europe/Simferopol', 'America/Argentina/ComodRivadavia', 'America/Jujuy', 'Pacific/Yap', 'Africa/Malabo',
         'Asia/Kuala_Lumpur', 'Europe/Ulyanovsk', 'Australia/Perth', 'EST', 'America/Atikokan', 'Australia/Brisbane',
         'America/Santa_Isabel', 'America/Indianapolis', 'Europe/Athens', 'Jamaica', 'America/Argentina/Salta',
         'America/Fort_Wayne', 'Indian/Antananarivo', 'America/North_Dakota/Beulah', 'America/Santarem',
         'Asia/Singapore', 'Asia/Chungking', 'Kwajalein', 'Asia/Aqtobe', 'America/Puerto_Rico', 'Pacific/Nauru',
         'Asia/Muscat', 'Europe/Sarajevo', 'America/Argentina/Buenos_Aires', 'America/Mendoza', 'America/Curacao',
         'America/La_Paz', 'Australia/Queensland', 'America/Indiana/Indianapolis', 'PRC', 'US/Samoa',
         'Africa/Djibouti', 'America/Hermosillo', 'Mexico/BajaNorte', 'US/Pacific', 'Australia/Sydney',
         'America/Rankin_Inlet', 'US/East-Indiana', 'Australia/ACT', 'America/Swift_Current', 'Cuba',
         'Etc/GMT-0', 'Asia/Samarkand', 'Etc/GMT-7', 'America/Guayaquil', 'Israel', 'MST7MDT', 'America/Aruba',
         'Africa/Dakar', 'Pacific/Wake', 'Asia/Saigon', 'Asia/Rangoon', 'Asia/Novosibirsk', 'Etc/GMT+12',
         'Asia/Tbilisi', 'Australia/North', 'America/Lima', 'Asia/Tomsk', 'Africa/Asmera', 'America/Kralendijk',
         'America/Monterrey', 'Europe/Lisbon', 'America/New_York', 'America/Indiana/Knox', 'Africa/Algiers',
         'Africa/Douala', 'Chile/Continental', 'Asia/Tel_Aviv', 'Africa/Freetown', 'Europe/Isle_of_Man',
         'Pacific/Truk', 'Asia/Chita', 'Etc/GMT-14', 'GMT-0', 'America/Port_of_Spain', 'Asia/Yerevan',
         'Europe/Amsterdam', 'Indian/Maldives', 'Europe/Busingen', 'Europe/Nicosia', 'Asia/Oral', 'Europe/Ljubljana',
         'Asia/Dushanbe', 'Zulu', 'America/Fort_Nelson', 'Africa/Banjul', 'Portugal', 'America/Iqaluit', 'EET',
         'Asia/Hong_Kong', 'Europe/Oslo', 'Africa/Addis_Ababa', 'Africa/Nairobi', 'America/Paramaribo',
         'Europe/Copenhagen', 'Europe/Kaliningrad', 'Europe/Jersey', 'America/Metlakatla', 'America/Tegucigalpa',
         'Indian/Christmas', 'America/Bahia', 'Indian/Cocos', 'America/Vancouver', 'America/Adak', 'Pacific/Funafuti',
         'Indian/Reunion', 'Africa/Bissau', 'America/Cayenne', 'America/Menominee', 'Europe/Bucharest', 'Asia/Harbin',
         'Indian/Mayotte', 'Etc/GMT+9', 'America/Argentina/Ushuaia', 'US/Indiana-Starke', 'Canada/Pacific',
         'Africa/Kinshasa', 'Africa/El_Aaiun', 'America/Indiana/Winamac', 'Atlantic/Faroe', 'Africa/Accra',
         'Pacific/Kanton', 'Australia/Darwin', 'Pacific/Easter', 'Asia/Yangon', 'Pacific/Port_Moresby', 'US/Arizona',
         'Indian/Mahe', 'Europe/Vilnius', 'Europe/Madrid', 'Europe/Skopje', 'America/Thunder_Bay', 'Asia/Aqtau',
         'America/Yakutat', 'America/Bahia_Banderas', 'America/Argentina/Mendoza', 'Europe/Brussels', 'Pacific/Niue',
         'Asia/Kuwait', 'Europe/Helsinki', 'America/Bogota', 'Pacific/Chuuk', 'Africa/Casablanca', 'Etc/GMT-6',
         'America/Montevideo', 'MET', 'Asia/Jayapura', 'America/Martinique', 'Canada/Central', 'Europe/Saratov',
         'Europe/Stockholm', 'America/Goose_Bay', 'Africa/Luanda', 'Pacific/Pago_Pago', 'Brazil/East',
         'Pacific/Tongatapu', 'America/Shiprock', 'Pacific/Marquesas', 'Atlantic/Faeroe', 'Asia/Hebron', 'America/Grand_Turk', 'Africa/Bujumbura', 'America/St_Barthelemy', 'America/Argentina/Cordoba', 'America/Indiana/Vincennes', 'America/Montreal', 'CST6CDT', 'Asia/Srednekolymsk', 'Europe/Rome', 'Canada/Eastern', 'Pacific/Midway', 'Australia/LHI', 'Antarctica/Syowa', 'America/Boa_Vista', 'Europe/Tiraspol', 'Pacific/Ponape', 'America/Ciudad_Juarez', 'Europe/Samara', 'America/Araguaina', 'America/Creston', 'America/Godthab', 'Europe/Uzhgorod', 'America/Antigua', 'Europe/Zagreb', 'Europe/Chisinau', 'Africa/Ouagadougou', 'America/Havana', 'Europe/Dublin', 'Europe/Prague', 'Asia/Urumqi', 'Pacific/Pitcairn', 'Asia/Nicosia', 'Atlantic/St_Helena', 'Asia/Dhaka', 'Asia/Dacca', 'Asia/Kashgar', 'Pacific/Norfolk', 'Brazil/West', 'Pacific/Gambier', 'Pacific/Guam', 'America/Asuncion', 'America/Scoresbysund', 'Europe/Vaduz', 'America/Argentina/San_Luis', 'America/Argentina/La_Rioja', 'Asia/Beirut', 'Europe/Zurich', 'Asia/Baghdad', 'Asia/Krasnoyarsk', 'Asia/Irkutsk', 'America/St_Lucia', 'Europe/Riga', 'UCT', 'America/Managua', 'Brazil/DeNoronha', 'America/Thule', 'Etc/GMT+6', 'Africa/Mogadishu', 'America/Cordoba', 'America/Miquelon', 'America/Ojinaga', 'America/Dawson', 'Pacific/Noumea', 'Pacific/Kosrae', 'America/St_Thomas', 'Etc/UTC', 'America/Boise', 'Africa/Lagos', 'America/Belize', 'America/Rio_Branco', 'GB-Eire', 'Europe/Warsaw', 'Atlantic/Jan_Mayen', 'Asia/Jerusalem', 'Europe/Mariehamn', 'Pacific/Fiji', 'Australia/Lindeman', 'MST', 'America/Halifax', 'Asia/Manila', 'America/St_Kitts', 'Africa/Harare', 'Etc/GMT+2', 'GMT+0', 'Poland', 'America/Punta_Arenas', 'Europe/Bratislava', 'Africa/Johannesburg', 'CET', 'Europe/Tallinn', 'Europe/Sofia', 'Pacific/Palau', 'ROK', 'America/Fortaleza', 'Etc/GMT+1', 'Etc/GMT-12', 'Africa/Juba', 'Brazil/Acre', 'HST', 'Africa/Abidjan', 'Etc/GMT-5', 'US/Michigan', 'America/Knox_IN', 'Africa/Niamey', 'Asia/Novokuznetsk', 'Etc/GMT-10', 'America/Montserrat', 'Europe/Tirane', 'Asia/Calcutta', 'Pacific/Efate', 'America/Denver', 'Asia/Kabul', 'Asia/Kuching', 'Asia/Colombo', 'America/Tijuana', 'America/Argentina/Rio_Gallegos', 'Asia/Karachi', 'Asia/Shanghai', 'Etc/Universal', 'America/Panama', 'Europe/Monaco', 'America/Atka', 'Canada/Yukon', 'America/Marigot', 'America/Caracas', 'Antarctica/Casey', 'America/Guyana', 'America/Manaus', 'America/Porto_Acre', 'Europe/Kiev', 'Asia/Vladivostok', 'Pacific/Honolulu', 'America/Nuuk', 'Asia/Macao', 'Europe/Berlin', 'Africa/Tunis', 'America/Inuvik', 'America/Barbados', 'Pacific/Tarawa', 'Pacific/Kwajalein', 'Etc/GMT+3', 'Europe/Belfast', 'America/Louisville', 'Asia/Ulan_Bator', 'Atlantic/Reykjavik', 'America/Argentina/Tucuman', 'Asia/Magadan', 'America/Maceio', 'America/Cancun', 'Pacific/Saipan', 'America/Jamaica', 'Asia/Kamchatka', 'Etc/GMT+0', 'America/Detroit', 'Pacific/Enderbury', 'Asia/Choibalsan', 'America/Anchorage', 'US/Mountain', 'Etc/GMT+8', 'Asia/Baku', 'Etc/GMT-1', 'Indian/Mauritius', 'Pacific/Kiritimati', 'GMT', 'Antarctica/Palmer', 'Egypt', 'WET', 'W-SU', 'America/Rainy_River', 'Atlantic/South_Georgia', 'Asia/Brunei', 'Africa/Tripoli', 'America/Argentina/San_Juan', 'America/Indiana/Vevay', 'America/Indiana/Tell_City', 'America/Pangnirtung', 'America/Chihuahua', 'Europe/Zaporozhye', 'Africa/Conakry', 'Europe/London', 'America/Regina', 'Africa/Khartoum', 'Antarctica/Troll', 'Pacific/Johnston', 'Europe/Istanbul', 'America/Costa_Rica', 'US/Alaska', 'Asia/Ujung_Pandang', 'Arctic/Longyearbyen', 'Africa/Cairo', 'America/Cuiaba', 'America/Sao_Paulo', 'Asia/Pontianak', 'Europe/Andorra', 'Asia/Ust-Nera', 'Atlantic/Bermuda', 'Australia/Adelaide', 'America/Santiago', 'Pacific/Rarotonga', 'Australia/West', 'UTC', 'America/Moncton', 'America/Guatemala', 'America/Juneau', 'Australia/Currie', 'Asia/Gaza', 'America/Belem', 'America/Los_Angeles', 'Africa/Timbuktu', 'Greenwich', 'Australia/Tasmania', 'America/North_Dakota/Center', 'America/Dominica', 'Africa/Maputo', 'Asia/Damascus', 'America/Guadeloupe')

tic = 0
for _ in LazySet:

    if 'Etc/GMT+3' in _:
        print(_, tic, sep=' | ')
        continue
    else:
        tic += 1
