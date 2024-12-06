import math
import pandas as pd

d = {'col1': [10, 100], 'col2': [1000, 10000]}
rpkm_df_combined = pd.DataFrame(data=d)

print(rpkm_df_combined)

rpkm_df_combined_log10 = rpkm_df_combined.applymap(math.log10)

print(rpkm_df_combined_log10)