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
# Keep-alive comment: 2025-06-01 05:23:03.477615
# Keep-alive comment: 2025-06-01 16:23:17.509433
# Keep-alive comment: 2025-06-02 03:23:19.064887
# Keep-alive comment: 2025-06-02 14:23:10.142726
# Keep-alive comment: 2025-06-03 01:23:00.280079
# Keep-alive comment: 2025-06-03 12:23:15.012782
# Keep-alive comment: 2025-06-03 23:23:10.978464
# Keep-alive comment: 2025-06-04 10:23:10.113463
# Keep-alive comment: 2025-06-04 21:22:49.025860
# Keep-alive comment: 2025-06-05 08:23:12.448547
# Keep-alive comment: 2025-06-05 19:23:02.352058
# Keep-alive comment: 2025-06-06 06:23:00.107823
# Keep-alive comment: 2025-06-06 17:22:43.309844
# Keep-alive comment: 2025-06-07 04:22:45.078512
# Keep-alive comment: 2025-06-07 15:22:54.442419
# Keep-alive comment: 2025-06-08 02:22:59.476736
# Keep-alive comment: 2025-06-08 13:23:01.340815
# Keep-alive comment: 2025-06-09 00:22:43.599551
# Keep-alive comment: 2025-06-09 11:22:58.533428
# Keep-alive comment: 2025-06-09 22:23:07.004090
# Keep-alive comment: 2025-06-10 09:23:10.267527
# Keep-alive comment: 2025-06-10 20:23:03.038077
# Keep-alive comment: 2025-06-11 07:23:04.134308
# Keep-alive comment: 2025-06-11 18:24:52.674622
# Keep-alive comment: 2025-06-12 05:23:01.287750
# Keep-alive comment: 2025-06-12 16:23:04.702117
# Keep-alive comment: 2025-06-13 03:23:05.715691
# Keep-alive comment: 2025-06-13 14:22:55.110148
# Keep-alive comment: 2025-06-14 01:23:15.148071
# Keep-alive comment: 2025-06-14 12:23:01.843639
# Keep-alive comment: 2025-06-14 23:22:53.238220
# Keep-alive comment: 2025-06-15 10:22:40.184200
# Keep-alive comment: 2025-06-15 21:23:13.558348
# Keep-alive comment: 2025-06-16 08:23:10.833608
# Keep-alive comment: 2025-06-16 19:22:54.766244
# Keep-alive comment: 2025-06-17 06:23:31.596496
# Keep-alive comment: 2025-06-17 17:22:59.612375
# Keep-alive comment: 2025-06-18 04:23:05.694296
# Keep-alive comment: 2025-06-18 15:23:04.949245
# Keep-alive comment: 2025-06-19 02:23:03.356205
# Keep-alive comment: 2025-06-19 13:23:03.290038
# Keep-alive comment: 2025-06-20 00:22:59.843725
# Keep-alive comment: 2025-06-20 11:23:49.193095
# Keep-alive comment: 2025-06-20 22:23:08.541297
# Keep-alive comment: 2025-06-21 09:22:53.758925
# Keep-alive comment: 2025-06-21 20:23:06.039504
# Keep-alive comment: 2025-06-22 07:22:58.787523
# Keep-alive comment: 2025-06-22 18:22:49.958840
# Keep-alive comment: 2025-06-23 05:23:05.847223
# Keep-alive comment: 2025-06-23 16:22:59.435008
# Keep-alive comment: 2025-06-24 03:23:05.878259
# Keep-alive comment: 2025-06-24 14:22:45.510809
# Keep-alive comment: 2025-06-25 01:22:39.452095
# Keep-alive comment: 2025-06-25 12:23:01.735570
# Keep-alive comment: 2025-06-25 23:23:03.792310
# Keep-alive comment: 2025-06-26 10:23:11.435374
# Keep-alive comment: 2025-06-26 21:24:36.033050
# Keep-alive comment: 2025-06-27 08:23:04.602861
# Keep-alive comment: 2025-06-27 19:23:01.189079
# Keep-alive comment: 2025-06-28 06:23:08.163484
# Keep-alive comment: 2025-06-28 17:22:58.332027
# Keep-alive comment: 2025-06-29 04:22:47.822383
# Keep-alive comment: 2025-06-29 15:22:37.965202
# Keep-alive comment: 2025-06-30 02:22:59.412441
# Keep-alive comment: 2025-06-30 13:22:41.534830
# Keep-alive comment: 2025-07-01 00:24:45.617429
# Keep-alive comment: 2025-07-01 11:23:01.412899
# Keep-alive comment: 2025-07-01 22:23:05.171226
# Keep-alive comment: 2025-07-02 09:22:59.097901
# Keep-alive comment: 2025-07-02 20:24:48.280390
# Keep-alive comment: 2025-07-03 07:23:13.832191
# Keep-alive comment: 2025-07-03 18:22:39.789168
# Keep-alive comment: 2025-07-04 05:23:02.365407
# Keep-alive comment: 2025-07-04 16:22:58.431299
# Keep-alive comment: 2025-07-05 03:22:56.937804
# Keep-alive comment: 2025-07-05 14:23:02.307818
# Keep-alive comment: 2025-07-06 01:23:00.341659
# Keep-alive comment: 2025-07-06 12:22:56.862881
# Keep-alive comment: 2025-07-06 23:22:58.548273
# Keep-alive comment: 2025-07-07 10:22:59.303570
# Keep-alive comment: 2025-07-07 21:22:58.138727
# Keep-alive comment: 2025-07-08 08:23:02.607029
# Keep-alive comment: 2025-07-08 19:22:58.549580
# Keep-alive comment: 2025-07-09 06:23:09.373515
# Keep-alive comment: 2025-07-09 17:23:42.841200
# Keep-alive comment: 2025-07-10 04:22:57.773424
# Keep-alive comment: 2025-07-10 15:23:04.000376
# Keep-alive comment: 2025-07-11 02:22:56.753419
# Keep-alive comment: 2025-07-11 13:22:57.956132
# Keep-alive comment: 2025-07-12 00:22:43.956519
# Keep-alive comment: 2025-07-12 11:23:02.045561
# Keep-alive comment: 2025-07-12 22:22:58.052174
# Keep-alive comment: 2025-07-13 09:22:57.965034
# Keep-alive comment: 2025-07-13 20:22:42.718966
# Keep-alive comment: 2025-07-14 07:22:55.533626
# Keep-alive comment: 2025-07-14 18:23:18.716310
# Keep-alive comment: 2025-07-15 05:23:08.654543
# Keep-alive comment: 2025-07-15 16:23:03.324266
# Keep-alive comment: 2025-07-16 03:23:02.573500
# Keep-alive comment: 2025-07-16 14:23:03.842012
# Keep-alive comment: 2025-07-17 01:22:58.088839
# Keep-alive comment: 2025-07-17 12:23:04.817229
# Keep-alive comment: 2025-07-17 23:22:56.266235
# Keep-alive comment: 2025-07-18 10:23:18.449419
# Keep-alive comment: 2025-07-18 21:22:57.851612
# Keep-alive comment: 2025-07-19 08:23:37.951763
# Keep-alive comment: 2025-07-19 19:22:42.858421
# Keep-alive comment: 2025-07-20 06:23:07.178893
# Keep-alive comment: 2025-07-20 17:23:13.436452
# Keep-alive comment: 2025-07-21 04:23:07.941205
# Keep-alive comment: 2025-07-21 15:22:55.143917
# Keep-alive comment: 2025-07-22 02:23:17.417944
# Keep-alive comment: 2025-07-22 13:23:31.320545
# Keep-alive comment: 2025-07-23 00:23:04.496438
# Keep-alive comment: 2025-07-23 11:22:54.430829
# Keep-alive comment: 2025-07-23 22:22:57.333518
# Keep-alive comment: 2025-07-24 09:23:13.952876
# Keep-alive comment: 2025-07-24 20:22:59.529186
# Keep-alive comment: 2025-07-25 07:22:54.257198
# Keep-alive comment: 2025-07-25 18:22:59.334224
# Keep-alive comment: 2025-07-26 05:22:53.007852
# Keep-alive comment: 2025-07-26 16:22:57.881034
# Keep-alive comment: 2025-07-27 03:22:52.902811
# Keep-alive comment: 2025-07-27 14:22:43.301875
# Keep-alive comment: 2025-07-28 01:23:04.700671
# Keep-alive comment: 2025-07-28 12:23:00.184044
# Keep-alive comment: 2025-07-28 23:22:58.069826
# Keep-alive comment: 2025-07-29 10:22:33.689588
# Keep-alive comment: 2025-07-29 21:23:03.932592
# Keep-alive comment: 2025-07-30 08:23:00.033858
# Keep-alive comment: 2025-07-30 19:23:08.923180
# Keep-alive comment: 2025-07-31 06:23:13.272642
# Keep-alive comment: 2025-07-31 17:22:59.137307
# Keep-alive comment: 2025-08-01 04:22:57.032926
# Keep-alive comment: 2025-08-01 15:23:08.761134
# Keep-alive comment: 2025-08-02 02:22:52.459536
# Keep-alive comment: 2025-08-02 13:23:03.325310
# Keep-alive comment: 2025-08-03 00:22:58.743996
# Keep-alive comment: 2025-08-03 11:23:04.000188
# Keep-alive comment: 2025-08-03 22:22:58.652176
# Keep-alive comment: 2025-08-04 09:22:55.844764
# Keep-alive comment: 2025-08-04 20:23:00.427543
# Keep-alive comment: 2025-08-05 07:23:03.074774
# Keep-alive comment: 2025-08-05 18:23:04.617362
# Keep-alive comment: 2025-08-06 05:22:58.309078
# Keep-alive comment: 2025-08-06 16:24:49.433420
# Keep-alive comment: 2025-08-07 03:23:02.523326
# Keep-alive comment: 2025-08-07 14:23:04.892880
# Keep-alive comment: 2025-08-08 01:22:53.337889
# Keep-alive comment: 2025-08-08 12:23:04.648758
# Keep-alive comment: 2025-08-08 23:23:04.726673
# Keep-alive comment: 2025-08-09 10:22:57.754593
# Keep-alive comment: 2025-08-09 21:23:20.415478
# Keep-alive comment: 2025-08-10 08:23:04.367138
# Keep-alive comment: 2025-08-10 19:23:04.158443
# Keep-alive comment: 2025-08-11 06:22:58.708371
# Keep-alive comment: 2025-08-11 17:23:04.773565
# Keep-alive comment: 2025-08-12 04:23:04.687621
# Keep-alive comment: 2025-08-12 15:22:56.424111
# Keep-alive comment: 2025-08-13 02:23:04.379597
# Keep-alive comment: 2025-08-13 13:23:01.664080
# Keep-alive comment: 2025-08-14 00:22:57.489330
# Keep-alive comment: 2025-08-14 11:23:05.758532
# Keep-alive comment: 2025-08-14 22:22:58.876173
# Keep-alive comment: 2025-08-15 09:22:58.559476
# Keep-alive comment: 2025-08-15 20:22:48.267022
# Keep-alive comment: 2025-08-16 07:23:12.525096
# Keep-alive comment: 2025-08-16 18:22:59.415382
# Keep-alive comment: 2025-08-17 05:23:02.049991
# Keep-alive comment: 2025-08-17 16:22:57.269972
# Keep-alive comment: 2025-08-18 03:22:59.364434
# Keep-alive comment: 2025-08-18 14:23:00.589630
# Keep-alive comment: 2025-08-19 01:22:59.002763
# Keep-alive comment: 2025-08-19 12:23:05.342783
# Keep-alive comment: 2025-08-19 23:23:26.285905
# Keep-alive comment: 2025-08-20 10:23:01.411214
# Keep-alive comment: 2025-08-20 21:23:04.026863
# Keep-alive comment: 2025-08-21 08:23:00.668174
# Keep-alive comment: 2025-08-21 19:23:05.339417
# Keep-alive comment: 2025-08-22 06:23:04.261146
# Keep-alive comment: 2025-08-22 17:22:59.509758
# Keep-alive comment: 2025-08-23 04:23:08.260953
# Keep-alive comment: 2025-08-23 15:22:57.695824
# Keep-alive comment: 2025-08-24 02:22:57.588013
# Keep-alive comment: 2025-08-24 13:22:58.649594
# Keep-alive comment: 2025-08-25 00:23:04.947257
# Keep-alive comment: 2025-08-25 11:23:04.459228
# Keep-alive comment: 2025-08-25 22:22:59.266121
# Keep-alive comment: 2025-08-26 09:23:00.657879
# Keep-alive comment: 2025-08-26 20:23:04.771416
# Keep-alive comment: 2025-08-27 07:23:09.188339
# Keep-alive comment: 2025-08-27 18:22:39.201313
# Keep-alive comment: 2025-08-28 05:23:09.931797
# Keep-alive comment: 2025-08-28 16:22:59.466394
# Keep-alive comment: 2025-08-29 03:22:43.164972
# Keep-alive comment: 2025-08-29 14:22:50.245538
# Keep-alive comment: 2025-08-30 01:22:48.239540
# Keep-alive comment: 2025-08-30 12:22:43.905002
# Keep-alive comment: 2025-08-30 23:22:47.358395
# Keep-alive comment: 2025-08-31 10:22:43.452752
# Keep-alive comment: 2025-08-31 21:22:54.670541
# Keep-alive comment: 2025-09-01 08:22:58.387945
# Keep-alive comment: 2025-09-01 19:22:54.924414
# Keep-alive comment: 2025-09-02 06:22:43.779874
# Keep-alive comment: 2025-09-02 17:22:55.421877
# Keep-alive comment: 2025-09-03 04:22:47.580201
# Keep-alive comment: 2025-09-03 15:22:50.762158
# Keep-alive comment: 2025-09-04 02:22:52.580120
# Keep-alive comment: 2025-09-04 13:23:02.914645
# Keep-alive comment: 2025-09-05 00:22:43.789084
# Keep-alive comment: 2025-09-05 11:22:39.930335
# Keep-alive comment: 2025-09-05 22:22:48.690450
# Keep-alive comment: 2025-09-06 09:22:44.466742
# Keep-alive comment: 2025-09-06 20:22:43.899569
# Keep-alive comment: 2025-09-07 07:22:49.206583
# Keep-alive comment: 2025-09-07 18:22:49.128202
# Keep-alive comment: 2025-09-08 05:22:45.257887
# Keep-alive comment: 2025-09-08 16:22:51.132098
# Keep-alive comment: 2025-09-09 03:23:15.725659
# Keep-alive comment: 2025-09-09 14:22:51.263380
# Keep-alive comment: 2025-09-10 01:22:43.115800
# Keep-alive comment: 2025-09-10 12:22:55.806072
# Keep-alive comment: 2025-09-10 23:22:44.054039
# Keep-alive comment: 2025-09-11 10:22:47.004880
# Keep-alive comment: 2025-09-11 21:22:44.296497
# Keep-alive comment: 2025-09-12 08:22:59.333253
# Keep-alive comment: 2025-09-12 19:22:49.730212
# Keep-alive comment: 2025-09-13 06:22:37.468548
# Keep-alive comment: 2025-09-13 17:22:44.089801
# Keep-alive comment: 2025-09-14 04:22:34.108822
# Keep-alive comment: 2025-09-14 15:22:45.552523
# Keep-alive comment: 2025-09-15 02:22:43.237322
# Keep-alive comment: 2025-09-15 13:22:46.315267
# Keep-alive comment: 2025-09-16 00:22:44.257421
# Keep-alive comment: 2025-09-16 11:22:49.900213
# Keep-alive comment: 2025-09-16 22:22:43.623033
# Keep-alive comment: 2025-09-17 09:22:46.484621
# Keep-alive comment: 2025-09-17 20:22:55.708904
# Keep-alive comment: 2025-09-18 07:22:51.405356
# Keep-alive comment: 2025-09-18 18:22:51.069086
# Keep-alive comment: 2025-09-19 05:22:45.242657
# Keep-alive comment: 2025-09-19 16:23:20.288648
# Keep-alive comment: 2025-09-20 03:22:48.738389
# Keep-alive comment: 2025-09-20 14:22:50.496858
# Keep-alive comment: 2025-09-21 01:22:50.008866
# Keep-alive comment: 2025-09-21 12:22:50.145529
# Keep-alive comment: 2025-09-21 23:22:44.961658
# Keep-alive comment: 2025-09-22 10:22:48.078334
# Keep-alive comment: 2025-09-22 21:22:44.527633
# Keep-alive comment: 2025-09-23 08:22:47.166154
# Keep-alive comment: 2025-09-23 19:22:52.391432
# Keep-alive comment: 2025-09-24 06:22:45.333737
# Keep-alive comment: 2025-09-24 17:22:51.627255
# Keep-alive comment: 2025-09-25 04:25:02.736284
# Keep-alive comment: 2025-09-25 15:22:55.941632
# Keep-alive comment: 2025-09-26 02:22:50.956948
# Keep-alive comment: 2025-09-26 13:22:55.031045
# Keep-alive comment: 2025-09-26 19:31:22.107969
# Keep-alive comment: 2025-09-27 05:31:27.051325
# Keep-alive comment: 2025-09-27 15:31:21.859641
# Keep-alive comment: 2025-09-28 01:31:25.958720
# Keep-alive comment: 2025-09-28 11:31:27.426867
# Keep-alive comment: 2025-09-28 21:31:26.772123
# Keep-alive comment: 2025-09-29 07:31:33.387363
# Keep-alive comment: 2025-09-29 17:31:42.612975
# Keep-alive comment: 2025-09-30 03:31:21.278556
# Keep-alive comment: 2025-09-30 13:31:28.301187
# Keep-alive comment: 2025-09-30 23:31:46.216076
# Keep-alive comment: 2025-10-01 09:31:54.689280
# Keep-alive comment: 2025-10-01 19:31:27.543353
# Keep-alive comment: 2025-10-02 05:31:55.197255
# Keep-alive comment: 2025-10-02 15:31:53.312224
# Keep-alive comment: 2025-10-03 01:31:26.261713
# Keep-alive comment: 2025-10-03 11:31:47.413925
# Keep-alive comment: 2025-10-03 21:31:22.020401
# Keep-alive comment: 2025-10-04 07:31:21.249051
# Keep-alive comment: 2025-10-04 17:31:32.038353
# Keep-alive comment: 2025-10-05 03:31:25.768864
# Keep-alive comment: 2025-10-05 13:31:30.866515
# Keep-alive comment: 2025-10-05 23:31:51.544367
# Keep-alive comment: 2025-10-06 09:31:57.433778
# Keep-alive comment: 2025-10-06 19:31:30.918134
# Keep-alive comment: 2025-10-07 05:31:28.601830
# Keep-alive comment: 2025-10-07 15:31:50.651941
# Keep-alive comment: 2025-10-08 01:31:26.620106
# Keep-alive comment: 2025-10-08 11:31:28.627732
# Keep-alive comment: 2025-10-08 21:31:27.793081
# Keep-alive comment: 2025-10-09 07:31:30.878745
# Keep-alive comment: 2025-10-09 17:31:30.684993
# Keep-alive comment: 2025-10-10 03:31:17.033785
# Keep-alive comment: 2025-10-10 13:31:09.265957
# Keep-alive comment: 2025-10-10 23:31:21.838196
# Keep-alive comment: 2025-10-11 09:31:27.371022
# Keep-alive comment: 2025-10-11 19:31:21.155393
# Keep-alive comment: 2025-10-12 05:31:24.533555
# Keep-alive comment: 2025-10-12 15:31:30.096908
# Keep-alive comment: 2025-10-13 01:31:23.604933
# Keep-alive comment: 2025-10-13 11:31:55.311289
# Keep-alive comment: 2025-10-13 21:31:17.848512
# Keep-alive comment: 2025-10-14 07:31:22.168262
# Keep-alive comment: 2025-10-14 17:31:25.029880
# Keep-alive comment: 2025-10-15 03:31:22.091535
# Keep-alive comment: 2025-10-15 13:31:25.044792
# Keep-alive comment: 2025-10-15 23:31:28.129010
# Keep-alive comment: 2025-10-16 09:31:24.443647
# Keep-alive comment: 2025-10-16 19:31:30.279744
# Keep-alive comment: 2025-10-17 05:31:28.426520
# Keep-alive comment: 2025-10-17 15:31:45.392168
# Keep-alive comment: 2025-10-18 01:31:22.988695
# Keep-alive comment: 2025-10-18 11:31:47.524351
# Keep-alive comment: 2025-10-18 21:31:57.188864
# Keep-alive comment: 2025-10-19 07:31:16.932235
# Keep-alive comment: 2025-10-19 17:31:52.060616
# Keep-alive comment: 2025-10-20 03:31:50.856607
# Keep-alive comment: 2025-10-20 13:31:29.886099
# Keep-alive comment: 2025-10-20 23:31:23.170606
# Keep-alive comment: 2025-10-21 09:31:29.346927
# Keep-alive comment: 2025-10-21 19:33:30.670987
# Keep-alive comment: 2025-10-22 05:31:24.089240
# Keep-alive comment: 2025-10-22 15:32:29.870770
# Keep-alive comment: 2025-10-23 01:31:22.265930
# Keep-alive comment: 2025-10-23 11:31:35.879916
# Keep-alive comment: 2025-10-23 21:31:25.050127
# Keep-alive comment: 2025-10-24 07:32:43.666181
# Keep-alive comment: 2025-10-24 17:31:34.503583
# Keep-alive comment: 2025-10-25 03:31:27.619477
# Keep-alive comment: 2025-10-25 13:31:51.363734
# Keep-alive comment: 2025-10-25 23:31:23.730823
# Keep-alive comment: 2025-10-26 09:31:16.847303
# Keep-alive comment: 2025-10-26 19:31:53.895372
# Keep-alive comment: 2025-10-27 05:31:34.059169
# Keep-alive comment: 2025-10-27 15:31:50.369517
# Keep-alive comment: 2025-10-28 01:31:26.787465
# Keep-alive comment: 2025-10-28 11:31:29.343529
# Keep-alive comment: 2025-10-28 21:31:17.720358
# Keep-alive comment: 2025-10-29 07:31:24.455197
# Keep-alive comment: 2025-10-29 17:31:33.841812
# Keep-alive comment: 2025-10-30 03:31:23.767677
# Keep-alive comment: 2025-10-30 13:31:55.782619
# Keep-alive comment: 2025-10-30 23:31:29.103271
# Keep-alive comment: 2025-10-31 09:32:43.615138
# Keep-alive comment: 2025-10-31 19:31:18.798974
# Keep-alive comment: 2025-11-01 05:31:27.372179
# Keep-alive comment: 2025-11-01 15:31:16.183737
# Keep-alive comment: 2025-11-02 01:31:28.235170
# Keep-alive comment: 2025-11-02 11:31:29.377882
# Keep-alive comment: 2025-11-02 21:31:43.464941
# Keep-alive comment: 2025-11-03 07:31:24.924322
# Keep-alive comment: 2025-11-03 17:31:30.593499
# Keep-alive comment: 2025-11-04 03:31:28.489637
# Keep-alive comment: 2025-11-04 13:31:56.500882
# Keep-alive comment: 2025-11-04 23:31:48.183404
# Keep-alive comment: 2025-11-05 09:32:00.268741
# Keep-alive comment: 2025-11-05 19:31:28.937110
# Keep-alive comment: 2025-11-06 05:31:58.394418
# Keep-alive comment: 2025-11-06 15:31:42.262914
# Keep-alive comment: 2025-11-07 01:31:26.552825
# Keep-alive comment: 2025-11-07 11:31:32.494371
# Keep-alive comment: 2025-11-07 21:31:30.349222
# Keep-alive comment: 2025-11-08 07:31:17.511354
# Keep-alive comment: 2025-11-08 17:31:33.098343
# Keep-alive comment: 2025-11-09 03:32:07.216735
# Keep-alive comment: 2025-11-09 13:31:28.868447
# Keep-alive comment: 2025-11-09 23:31:18.716906
# Keep-alive comment: 2025-11-10 09:31:25.636098
# Keep-alive comment: 2025-11-10 19:31:40.847007
# Keep-alive comment: 2025-11-11 05:31:25.485011
# Keep-alive comment: 2025-11-11 15:31:23.901217
# Keep-alive comment: 2025-11-12 01:31:30.463079
# Keep-alive comment: 2025-11-12 11:31:33.659205
# Keep-alive comment: 2025-11-12 21:31:50.835610
# Keep-alive comment: 2025-11-13 07:31:13.792721
# Keep-alive comment: 2025-11-13 17:31:25.355898
# Keep-alive comment: 2025-11-14 03:31:31.446284
# Keep-alive comment: 2025-11-14 13:31:52.450610
# Keep-alive comment: 2025-11-14 23:31:23.933578
# Keep-alive comment: 2025-11-15 09:31:27.394202
# Keep-alive comment: 2025-11-15 19:31:32.934786
# Keep-alive comment: 2025-11-16 05:31:24.596532
# Keep-alive comment: 2025-11-16 15:31:28.796352
# Keep-alive comment: 2025-11-17 01:31:19.255924
# Keep-alive comment: 2025-11-17 11:31:52.579146
# Keep-alive comment: 2025-11-17 21:31:21.207253
# Keep-alive comment: 2025-11-18 07:31:23.890110
# Keep-alive comment: 2025-11-18 17:31:24.768099
# Keep-alive comment: 2025-11-19 03:31:27.180565
# Keep-alive comment: 2025-11-19 13:31:20.516330
# Keep-alive comment: 2025-11-19 23:31:21.894294
# Keep-alive comment: 2025-11-20 09:31:29.686910
# Keep-alive comment: 2025-11-20 19:33:19.188076
# Keep-alive comment: 2025-11-21 05:31:24.667998
# Keep-alive comment: 2025-11-21 15:31:30.178848
# Keep-alive comment: 2025-11-22 01:31:33.061198
# Keep-alive comment: 2025-11-22 11:31:17.930640
# Keep-alive comment: 2025-11-22 21:31:29.065222
# Keep-alive comment: 2025-11-23 07:31:29.761700
# Keep-alive comment: 2025-11-23 17:31:32.779700
# Keep-alive comment: 2025-11-24 03:31:23.044176
# Keep-alive comment: 2025-11-24 13:31:20.749704
# Keep-alive comment: 2025-11-24 23:31:30.606009
# Keep-alive comment: 2025-11-25 09:31:52.074446
# Keep-alive comment: 2025-11-25 19:31:26.325347
# Keep-alive comment: 2025-11-26 05:31:39.111381
# Keep-alive comment: 2025-11-26 15:31:40.345510
# Keep-alive comment: 2025-11-27 01:31:29.469303
# Keep-alive comment: 2025-11-27 11:31:26.107577
# Keep-alive comment: 2025-11-27 21:31:19.291994
# Keep-alive comment: 2025-11-28 07:31:17.597067
# Keep-alive comment: 2025-11-28 17:31:30.141689
# Keep-alive comment: 2025-11-29 03:31:23.963892
# Keep-alive comment: 2025-11-29 13:31:34.515455
# Keep-alive comment: 2025-11-29 23:31:24.067514
# Keep-alive comment: 2025-11-30 09:31:25.445577
# Keep-alive comment: 2025-11-30 19:31:17.297222
# Keep-alive comment: 2025-12-01 05:31:14.243439
# Keep-alive comment: 2025-12-01 15:31:21.578780
# Keep-alive comment: 2025-12-02 01:31:04.436857
# Keep-alive comment: 2025-12-02 11:31:27.012424
# Keep-alive comment: 2025-12-02 21:31:29.484124
# Keep-alive comment: 2025-12-03 07:31:26.668067
# Keep-alive comment: 2025-12-03 17:31:34.522562
# Keep-alive comment: 2025-12-04 03:31:24.456278
# Keep-alive comment: 2025-12-04 13:31:22.148426
# Keep-alive comment: 2025-12-04 23:31:23.475334
# Keep-alive comment: 2025-12-05 09:31:24.052670
# Keep-alive comment: 2025-12-05 19:31:18.671694
# Keep-alive comment: 2025-12-06 05:31:23.829234
# Keep-alive comment: 2025-12-06 15:31:10.651383
# Keep-alive comment: 2025-12-07 01:31:19.562519
# Keep-alive comment: 2025-12-07 11:31:23.322227
# Keep-alive comment: 2025-12-07 21:31:19.695803
# Keep-alive comment: 2025-12-08 07:31:33.027136
# Keep-alive comment: 2025-12-08 17:31:19.821278
# Keep-alive comment: 2025-12-09 03:31:23.125640
# Keep-alive comment: 2025-12-09 13:31:23.187311
# Keep-alive comment: 2025-12-09 23:31:24.029735
# Keep-alive comment: 2025-12-10 09:31:25.864803
# Keep-alive comment: 2025-12-10 19:31:30.133379
# Keep-alive comment: 2025-12-11 05:31:04.478264
# Keep-alive comment: 2025-12-11 15:31:27.782252
# Keep-alive comment: 2025-12-12 01:31:23.348839
# Keep-alive comment: 2025-12-12 11:31:11.643996
# Keep-alive comment: 2025-12-12 21:31:29.603727
# Keep-alive comment: 2025-12-13 07:31:22.199081
# Keep-alive comment: 2025-12-13 17:31:24.624912
# Keep-alive comment: 2025-12-14 03:31:26.897092
# Keep-alive comment: 2025-12-14 13:31:22.269130
# Keep-alive comment: 2025-12-14 23:31:17.637369
# Keep-alive comment: 2025-12-15 09:31:23.555183
# Keep-alive comment: 2025-12-15 19:31:23.398520
# Keep-alive comment: 2025-12-16 05:31:30.469199
# Keep-alive comment: 2025-12-16 15:31:19.598188
# Keep-alive comment: 2025-12-17 01:31:50.716654
# Keep-alive comment: 2025-12-17 11:31:17.863680
# Keep-alive comment: 2025-12-17 21:34:34.121746
# Keep-alive comment: 2025-12-18 07:31:24.812037
# Keep-alive comment: 2025-12-18 17:31:37.772138
# Keep-alive comment: 2025-12-19 03:31:33.061394
# Keep-alive comment: 2025-12-19 13:31:27.678720
# Keep-alive comment: 2025-12-19 23:32:01.872543
# Keep-alive comment: 2025-12-20 09:31:08.577483
# Keep-alive comment: 2025-12-20 19:31:23.896986
# Keep-alive comment: 2025-12-21 05:31:21.946254
# Keep-alive comment: 2025-12-21 15:31:06.916904
# Keep-alive comment: 2025-12-22 01:31:21.419870
# Keep-alive comment: 2025-12-22 11:31:24.259963
# Keep-alive comment: 2025-12-22 21:31:08.201695
# Keep-alive comment: 2025-12-23 07:31:25.870146
# Keep-alive comment: 2025-12-23 17:31:27.198640
# Keep-alive comment: 2025-12-24 03:31:14.076454
# Keep-alive comment: 2025-12-24 13:31:09.086452
# Keep-alive comment: 2025-12-24 23:31:16.063959
# Keep-alive comment: 2025-12-25 09:31:29.355774
# Keep-alive comment: 2025-12-25 19:31:23.746184
# Keep-alive comment: 2025-12-26 05:31:23.414992
# Keep-alive comment: 2025-12-26 15:31:22.500212
# Keep-alive comment: 2025-12-27 01:31:17.510950
# Keep-alive comment: 2025-12-27 11:31:21.310331
# Keep-alive comment: 2025-12-27 21:31:22.437059
# Keep-alive comment: 2025-12-28 07:31:22.496979
# Keep-alive comment: 2025-12-28 17:31:29.342889
# Keep-alive comment: 2025-12-29 03:31:17.590310
# Keep-alive comment: 2025-12-29 13:31:23.827511
# Keep-alive comment: 2025-12-29 23:31:18.798883
# Keep-alive comment: 2025-12-30 09:31:08.754051
# Keep-alive comment: 2025-12-30 19:31:27.134422
# Keep-alive comment: 2025-12-31 05:31:19.829648
# Keep-alive comment: 2025-12-31 15:31:20.197228
# Keep-alive comment: 2026-01-01 01:31:29.555266
# Keep-alive comment: 2026-01-01 11:31:24.906218
# Keep-alive comment: 2026-01-01 21:31:35.612808
# Keep-alive comment: 2026-01-02 07:31:25.269679
# Keep-alive comment: 2026-01-02 17:31:24.093766
# Keep-alive comment: 2026-01-03 03:31:20.745738
# Keep-alive comment: 2026-01-03 13:31:25.500337
# Keep-alive comment: 2026-01-03 23:31:27.088193
# Keep-alive comment: 2026-01-04 09:31:19.006129
# Keep-alive comment: 2026-01-04 19:31:25.577203
# Keep-alive comment: 2026-01-05 05:31:24.394105
# Keep-alive comment: 2026-01-05 15:31:29.961580
# Keep-alive comment: 2026-01-06 01:31:19.568673
# Keep-alive comment: 2026-01-06 11:31:20.637350
# Keep-alive comment: 2026-01-06 21:31:19.710482
# Keep-alive comment: 2026-01-07 07:31:18.858420
# Keep-alive comment: 2026-01-07 17:31:19.198717
# Keep-alive comment: 2026-01-08 03:31:26.603511
# Keep-alive comment: 2026-01-08 13:31:21.417449
# Keep-alive comment: 2026-01-08 23:31:18.496556
# Keep-alive comment: 2026-01-09 09:31:19.739805
# Keep-alive comment: 2026-01-09 19:31:24.254464
# Keep-alive comment: 2026-01-10 05:31:27.792899
# Keep-alive comment: 2026-01-10 15:31:12.724902
# Keep-alive comment: 2026-01-11 01:31:20.350981
# Keep-alive comment: 2026-01-11 11:31:28.459278
# Keep-alive comment: 2026-01-11 21:31:22.678118
# Keep-alive comment: 2026-01-12 07:31:25.465962
# Keep-alive comment: 2026-01-12 17:31:23.154789
# Keep-alive comment: 2026-01-13 03:31:20.681491
# Keep-alive comment: 2026-01-13 13:31:15.822005
# Keep-alive comment: 2026-01-13 23:31:27.804490
# Keep-alive comment: 2026-01-14 09:31:21.526656
# Keep-alive comment: 2026-01-14 19:31:26.043636
# Keep-alive comment: 2026-01-15 05:31:23.835235
# Keep-alive comment: 2026-01-15 15:31:35.248820
# Keep-alive comment: 2026-01-16 01:31:27.163573
# Keep-alive comment: 2026-01-16 11:31:35.002545
# Keep-alive comment: 2026-01-16 21:31:22.581345
# Keep-alive comment: 2026-01-17 07:31:07.580652
# Keep-alive comment: 2026-01-17 17:31:22.102356
# Keep-alive comment: 2026-01-18 03:31:23.643056
# Keep-alive comment: 2026-01-18 13:31:19.182464
# Keep-alive comment: 2026-01-18 23:31:28.324130
# Keep-alive comment: 2026-01-19 09:31:27.733107
# Keep-alive comment: 2026-01-19 19:31:21.867200
# Keep-alive comment: 2026-01-20 05:31:18.019317
# Keep-alive comment: 2026-01-20 15:31:25.985741
# Keep-alive comment: 2026-01-21 01:31:23.127833
# Keep-alive comment: 2026-01-21 11:31:20.780180
# Keep-alive comment: 2026-01-21 21:31:25.401059
# Keep-alive comment: 2026-01-22 07:31:26.376618
# Keep-alive comment: 2026-01-22 17:31:18.710684
# Keep-alive comment: 2026-01-23 03:31:58.437796
# Keep-alive comment: 2026-01-23 13:31:32.241445
# Keep-alive comment: 2026-01-23 23:31:25.063675
# Keep-alive comment: 2026-01-24 09:31:34.026783
# Keep-alive comment: 2026-01-24 19:31:27.026968
# Keep-alive comment: 2026-01-25 05:31:19.195996
# Keep-alive comment: 2026-01-25 15:31:28.999280
# Keep-alive comment: 2026-01-26 01:31:24.620094
# Keep-alive comment: 2026-01-26 11:31:25.300053
# Keep-alive comment: 2026-01-26 21:31:28.710673
# Keep-alive comment: 2026-01-27 07:31:26.761153
# Keep-alive comment: 2026-01-27 17:31:30.316243
# Keep-alive comment: 2026-01-28 03:31:25.403910
# Keep-alive comment: 2026-01-28 13:31:27.070200
# Keep-alive comment: 2026-01-28 23:32:47.746410
# Keep-alive comment: 2026-01-29 09:31:30.021611
# Keep-alive comment: 2026-01-29 19:31:18.017926
# Keep-alive comment: 2026-01-30 05:31:08.724895
# Keep-alive comment: 2026-01-30 15:31:25.362224
# Keep-alive comment: 2026-01-31 01:31:32.614983
# Keep-alive comment: 2026-01-31 11:31:29.218061
# Keep-alive comment: 2026-01-31 21:31:28.691600
# Keep-alive comment: 2026-02-01 07:31:33.722392
# Keep-alive comment: 2026-02-01 17:31:26.668766
# Keep-alive comment: 2026-02-02 03:31:39.993170
# Keep-alive comment: 2026-02-02 13:31:42.524640
# Keep-alive comment: 2026-02-02 23:32:37.205378
# Keep-alive comment: 2026-02-03 09:31:30.197227
# Keep-alive comment: 2026-02-03 19:32:51.821279
# Keep-alive comment: 2026-02-04 05:31:33.230190
# Keep-alive comment: 2026-02-04 15:31:35.216434
# Keep-alive comment: 2026-02-05 01:31:28.651090
# Keep-alive comment: 2026-02-05 11:31:30.373267