import pandas as pd
pd.options.mode.chained_assignment = None

file = 'Carpenters_Glasgow.csv'
df = pd.read_csv(file)

# d1 = {'https://www.facebook.com/JSS-joiners-2334784586744760/': set(), 'http://www.qualityjoiners.com': {'rodger@qualityjoiners.com'}, 'http://www.hendryjoinersandbuilders.co.uk/': {'kirk@hendryjoiners.com', 'badge181_25_gs@2x.png'}, 'http://www.procraftjoinery.co.uk': {'scott@procraftjoinery.co.uk'}, 'http://www.kingslandcontracts.co.uk': {'info@kingslandcontracts.co.uk'}, 'http://www.apchomeimprovements.co.uk': {'info@apchomeimprovements.co.uk'}, 'http://www.glasgowjoineryservices.co.uk': set(), 'http://www.yessshomeimprovements.co.uk': {'info@yessshomeimprovements.co.uk'}}
d1 = {'http://www.hendryjoinersandbuilders.co.uk/': {'kirk@hendryjoiners.com', 'badge181_25_gs@2x.png'}, 'http://www.procraftjoinery.co.uk': {'scott@procraftjoinery.co.uk'}, 'http://www.kingslandcontracts.co.uk': {'info@kingslandcontracts.co.uk'}, 'http://www.apchomeimprovements.co.uk': {'info@apchomeimprovements.co.uk'}, 'http://www.glasgowjoineryservices.co.uk': set(), 'http://www.yessshomeimprovements.co.uk': {'info@yessshomeimprovements.co.uk'}}

# df['emails'] = ''
for (url, emails) in d1.items():
    emails = ", ".join(emails)

    df.loc[df['website'] == url, 'emails'] = emails

    # matching_rows = df[df['website'] == url]
    # print(emails)
    # matching_rows['emails'] = emails

print(df['emails'])
df.to_csv(f'{file}', index=False)