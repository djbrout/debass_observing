import pandas as pd
import numpy as np

df = pd.read_pickle('tns.pkl')

sources = ['ZTF','Pan-STARRS1','ATLAS','GaiaAlerts']
sources = ['ZTF','ATLAS']

wwsources = df['discovery_data_source'].str.contains('|'.join(sources))

wwhostredshift = (df['host_redshift'].astype(float)<.08) | (df['host_redshift'].astype(str) == 'None')
wwsnredshift = (df['redshift'].astype(float)<.08) | (df['redshift'].astype(str) == 'None')

wwbrightmag = df['brightmag']<18.9
wwdiscmag = df['discoverymag']<19.2
wwisia = df['isIa']

#print(df[wwisia])

print(df[(wwdiscmag | wwbrightmag) & wwsources & wwsnredshift])

#print(df[wwisia & wwsources & wwsnredshift])
#print(df[(wwdiscmag | wwbrightmag) & wwisia & wwsources & wwsnredshift])

import matplotlib.pyplot as plt

bins = np.arange(0,.1,.01)
plt.hist(df[wwisia & wwsources & wwsnredshift]['redshift'],bins=bins,label='all Ias '+str(len(df[wwisia & wwsources & wwsnredshift]['redshift'])))
plt.hist(df[(wwdiscmag | wwbrightmag) & wwisia & wwsources & wwsnredshift]['redshift'],bins=bins,label='with prepeak cuts')
plt.xlabel('redshift')
plt.legend()
plt.tight_layout()
plt.savefig('prepeak_cuts_eff.png')
print('open prepeak_cuts_eff.png')
