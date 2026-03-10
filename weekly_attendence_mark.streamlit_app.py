import streamlit as st
import openpyxl
import pandas as pd
import numpy as np
import re



st.title("🔢 Simple ID Matcher")

# 1. Upload both files
master_file = st.file_uploader("Upload Master students sheet", type=["xlsx"])
source_file = st.file_uploader("Upload Attendance file (IDS)", type=["xlsx"])

if master_file and source_file:
    # Load files
    df_master = pd.read_excel(master_file)
    df_source = pd.read_excel(source_file)

    # 2. Select the ID Column and the Week Column
    col_list = df_master.columns.tolist()
    
    c1, c2 = st.columns(2)
    with c1:
        id_column = st.selectbox("Select the column with IDs:", col_list)
    with c2:
        weeks = [c for c in col_list if 'week' in c.lower()]
        target_week = st.selectbox("Select the Week to mark:", weeks)

    if st.button("Mark Attendance"):
        
        found_ids = df_source.astype(str).values.flatten()
        found_ids = [str(x).strip() for x in raw_source if str(x).strip() not in ['nan', 'None', '']]
        # 4. Mark the Master File
        # Convert chosen ID column to string so they match correctly
        df_master[id_column] = df_master[id_column].astype(str).replace('nan', '')
        if found_ids:
            id_pattern = '|'.join([re.escape(id) + '$' for id in found_ids])
# 2. Check if the Master ID contains ANY of those short IDs
        if id_pattern:
            mask = df_master[id_column].str.contains(id_pattern, na=False, regex=True)
            df_master.loc[mask, target_week] = "yes"
            df_master[target_week] = df_master[target_week].astype(str).str.strip().replace('nan', '')
        total= df_master[id_column].nunique()
        count= (df_master[target_week]=='yes').sum()
        abscence=total- count
        st.success(f"Done! Marked IDs found in {target_week}")
        st.write(f'✅ Count {count}')
        st.write(f'❌ Absent {abscence}')
        st.dataframe(df_master)
        

       






