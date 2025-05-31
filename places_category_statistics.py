import streamlit as st
from read_data import read_from_gsheets
import altair as alt
from datetime import datetime, timedelta
import pandas as pd
import streamlit.components.v1 as components



st.set_page_config(
    page_title="Places Summary Statistics - Category Statistics",
    layout="wide"
)
#### Categroy Statistics #### 
category_stats_df = read_from_gsheets("Category stats")\
    [["Country", "naics_2", "naics_code", "safegraph_category", "safegraph_subcategory", "industry_title", "total_poi_count"]]\
    .astype({'total_poi_count': int})

category_stats_df['safegraph_subcategory'] = category_stats_df['safegraph_subcategory'].astype(str).replace("NaN", " ")
category_stats_df['safegraph_category'] = category_stats_df['safegraph_category'].astype(str).replace("NaN", " ")

global_df = category_stats_df.groupby(['naics_2', 'industry_title'])\
    .agg(total_poi_count=('total_poi_count', 'sum'))\
    .sort_values('total_poi_count', ascending=False)\
    .reset_index()\
    .rename(columns={"naics_2": "2-digit NAICS", "industry_title": "Industry Title", "total_poi_count": "Total POI"})

global_df_styled = global_df.style.apply(lambda x: ['background-color: #D7E8ED' if i % 2 == 0 else '' for i in range(len(x))], axis=0)\
    .format({"Total POI": "{:,}"})

countries = ['US', 'UK', 'CA']
dfs = []

for country in countries:
    df = (
        category_stats_df[category_stats_df['Country'] == country]
        [["naics_code", "safegraph_category", "safegraph_subcategory", "total_poi_count"]]
        .rename(columns={"naics_code": "NAICS Code", "safegraph_category": "SafeGraph Category", "safegraph_subcategory": "SafeGraph Subcategory", "total_poi_count": "Total POI"})
        .sort_values('Total POI', ascending=False)
        .reset_index(drop=True)
    )

    df['Total POI'] = df['Total POI'].astype(int).apply(lambda x: "{:,}".format(x))
    dfs.append(df)

naics_possible_df = dfs[0]
#naics_possible_df['SafeGraph Subcategory'] = ["" if pd.isna(x) else x for x in naics_possible_df['SafeGraph Subcategory']]
#naics_possible_df['SafeGraph Category'] = ["" if pd.isna(x) else x for x in naics_possible_df['SafeGraph Category']]


naics_possible_df['Category'] = naics_possible_df['NAICS Code'].astype(str) + " " + naics_possible_df['SafeGraph Category']\
      + " " + naics_possible_df['SafeGraph Subcategory'] 


possible_naics_codes = naics_possible_df['Category'].astype(str).unique()

tabs = st.tabs(["Global"] + countries)
with tabs[0]:
    # st.write("Global POI Count")
    st.dataframe(global_df_styled, use_container_width=True, hide_index=True)

for i, tab in enumerate(tabs[1:]):
    with tab:
        if i < len(dfs):
            naics_list = st.selectbox("NAICS Code:", [""] + possible_naics_codes.tolist(), key = i)
            if naics_list:
                styled_dfs = (
                    dfs[i][dfs[i]['NAICS Code'].astype(str).str.startswith(naics_list.split(" ")[0])]\
                        .style.apply(lambda x: ['background-color: #D7E8ED' if i % 2 == 0 else '' for i in range(len(x))], axis=0)
                    )
                # st.write(f"{countries[i]} POI Count")
                st.dataframe(styled_dfs, use_container_width=True, hide_index=True)
            else:
                styled_dfs = (
                    dfs[i].style.apply(lambda x: ['background-color: #D7E8ED' if i % 2 == 0 else '' for i in range(len(x))], axis=0)
                    )
                # st.write(f"{countries[i]} POI Count")
                st.dataframe(styled_dfs, use_container_width=True, hide_index=True)
#

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

css = '''
<style>
section.main > div:has(~ footer ) {
     padding-top: 0px;
    padding-bottom: 0px;
}

[data-testid="ScrollToBottomContainer"] {
    overflow: hidden;
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# Keep-alive comment: 2025-04-25 16:08:37.448725
# Keep-alive comment: 2025-04-25 16:18:34.137817
# Keep-alive comment: 2025-04-26 00:24:08.949157
# Keep-alive comment: 2025-04-26 11:24:03.527024
# Keep-alive comment: 2025-04-26 22:23:02.775775
# Keep-alive comment: 2025-04-27 09:23:33.878297
# Keep-alive comment: 2025-04-27 20:23:28.818560
# Keep-alive comment: 2025-04-28 07:23:59.230173
# Keep-alive comment: 2025-04-28 18:24:19.235404
# Keep-alive comment: 2025-04-29 05:23:48.657246
# Keep-alive comment: 2025-04-29 16:24:33.219784
# Keep-alive comment: 2025-04-30 03:23:23.411299
# Keep-alive comment: 2025-04-30 14:23:51.728110
# Keep-alive comment: 2025-05-01 01:24:02.930606
# Keep-alive comment: 2025-05-01 12:23:34.271404
# Keep-alive comment: 2025-05-01 23:23:07.385872
# Keep-alive comment: 2025-05-02 10:23:53.390332
# Keep-alive comment: 2025-05-02 21:23:04.548738
# Keep-alive comment: 2025-05-03 08:23:29.127427
# Keep-alive comment: 2025-05-03 19:23:47.241631
# Keep-alive comment: 2025-05-04 06:23:52.994166
# Keep-alive comment: 2025-05-04 17:23:01.839152
# Keep-alive comment: 2025-05-05 04:24:12.656153
# Keep-alive comment: 2025-05-05 15:23:31.734894
# Keep-alive comment: 2025-05-06 02:24:22.828815
# Keep-alive comment: 2025-05-06 13:23:24.427131
# Keep-alive comment: 2025-05-07 00:23:23.338177
# Keep-alive comment: 2025-05-07 11:23:35.911150
# Keep-alive comment: 2025-05-07 22:23:34.397724
# Keep-alive comment: 2025-05-08 09:23:36.509553
# Keep-alive comment: 2025-05-08 20:23:34.934482
# Keep-alive comment: 2025-05-09 07:23:45.003119
# Keep-alive comment: 2025-05-09 18:23:57.270057
# Keep-alive comment: 2025-05-10 05:23:40.887127
# Keep-alive comment: 2025-05-10 16:23:26.368628
# Keep-alive comment: 2025-05-11 03:23:26.731567
# Keep-alive comment: 2025-05-11 14:23:18.373405
# Keep-alive comment: 2025-05-12 01:23:23.594341
# Keep-alive comment: 2025-05-12 12:23:54.234627
# Keep-alive comment: 2025-05-12 23:23:27.318423
# Keep-alive comment: 2025-05-13 10:24:27.748808
# Keep-alive comment: 2025-05-13 21:23:28.150924
# Keep-alive comment: 2025-05-14 08:23:55.956549
# Keep-alive comment: 2025-05-14 19:23:53.316633
# Keep-alive comment: 2025-05-15 06:23:54.905350
# Keep-alive comment: 2025-05-15 17:24:24.546888
# Keep-alive comment: 2025-05-16 04:23:39.923094
# Keep-alive comment: 2025-05-16 15:22:42.893023
# Keep-alive comment: 2025-05-17 02:23:01.040174
# Keep-alive comment: 2025-05-17 13:23:44.525918
# Keep-alive comment: 2025-05-18 00:22:59.445338
# Keep-alive comment: 2025-05-18 11:23:27.668964
# Keep-alive comment: 2025-05-18 22:23:25.152913
# Keep-alive comment: 2025-05-19 09:24:01.555538
# Keep-alive comment: 2025-05-19 20:23:00.173391
# Keep-alive comment: 2025-05-20 07:23:16.449609
# Keep-alive comment: 2025-05-20 18:24:28.555938
# Keep-alive comment: 2025-05-21 05:23:00.086308
# Keep-alive comment: 2025-05-21 16:23:09.537781
# Keep-alive comment: 2025-05-22 03:23:03.802089
# Keep-alive comment: 2025-05-22 14:23:07.791104
# Keep-alive comment: 2025-05-23 01:23:06.537825
# Keep-alive comment: 2025-05-23 12:23:06.144429
# Keep-alive comment: 2025-05-23 23:23:10.156186
# Keep-alive comment: 2025-05-24 10:23:07.778927
# Keep-alive comment: 2025-05-24 21:23:04.478854
# Keep-alive comment: 2025-05-25 08:23:05.276527
# Keep-alive comment: 2025-05-25 19:23:10.252828
# Keep-alive comment: 2025-05-26 06:22:55.322579
# Keep-alive comment: 2025-05-26 17:22:59.674021
# Keep-alive comment: 2025-05-27 04:23:05.342002
# Keep-alive comment: 2025-05-27 15:23:09.806862
# Keep-alive comment: 2025-05-28 02:23:19.662360
# Keep-alive comment: 2025-05-28 13:23:09.981263
# Keep-alive comment: 2025-05-29 00:23:03.209709
# Keep-alive comment: 2025-05-29 11:22:58.433109
# Keep-alive comment: 2025-05-29 22:23:12.790277
# Keep-alive comment: 2025-05-30 09:22:58.023870
# Keep-alive comment: 2025-05-30 20:22:58.792600
# Keep-alive comment: 2025-05-31 07:23:10.867937
# Keep-alive comment: 2025-05-31 18:23:05.466165