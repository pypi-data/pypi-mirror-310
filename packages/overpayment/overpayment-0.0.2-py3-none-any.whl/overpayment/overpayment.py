import pandas as pd
import time
def rounding_off_to_zero(x):
    if abs(x) < 1:
        return 0
    else:
        return x

def start_overpayment():
    d = {'Sales Order Number' : 'Sales Order',
        'Final Employee Name' : 'Employee Name',
        'Final Position ID'   : 'Position',
        'Position Code'       : 'Position',
        'SO'                  : 'Sales Order',
        'Employee code'       : 'Employee Id',
        'Order ID(Unique ID)' :'Order ID',
        'Employee name'       : 'Employee Name',
        'Order Date'          : 'Order_Date',
        'Employee_Name'       :'Employee Name',
        'Employee_ID'         :'Employee Id',
        'Sales_Order'         : 'Sales Order',
        'Final Employee Code' : 'Employee Id'}
    print('Importing Files...')
    df = pd.read_csv('Export OIT Credited Transactions for Protections.csv', dtype = 'str')
    df.rename(columns = d, inplace = True)
    df['Crediting Value'] = df['Crediting Value'].apply(lambda x: float(x))

    new_df = df[['Sales Order', 'Crediting Value', 'Employee Name', 'Position', 'Employee Id','BU - Org']].groupby(['Employee Id','BU - Org', 'Employee Name','Sales Order','Position']).sum().reset_index()
    new_df = new_df.merge(df[['Component Name','Sales Order', 'Employee Name','Employee Id']].groupby(['Sales Order', 'Employee Name','Employee Id']).nunique().reset_index(
        ), on = ['Sales Order', 'Employee Name','Employee Id'], how = 'left')

    new_df['new_crediting_value'] = new_df['Crediting Value']/new_df['Component Name']

    # dfp = pd.read_csv('M05.57-Calc-Initial OIT Credited Order Lines.csv', dtype = 'str')
    dfo = pd.read_excel('R2 to R3 Analysis.xlsx', sheet_name = 'result', dtype = 'str')
    df_old = pd.read_excel('Cancelled and Rebook SalesOrder R2 to R3.xlsx', sheet_name = 'Orgnl SO & their rspctv New SO', dtype = 'str', header = 1)

    df_oit = pd.read_csv('Export Initial OIT Credited Transactions For Protections.csv', dtype = 'str')
    df_oit.rename(columns = d, inplace = True)
    df_oit = df_oit[df_oit['Exclude?'] == 'true']
    print('Done')
    print('Analyzing the data...')
    dfo1 = dfo[['Original Sales_Order_Number', 'old_Fiscal_Period','old_sum(line_item_net_value)']].copy()
    dfo1['Original Sales_Order_Number'] = dfo1['Original Sales_Order_Number'].str.strip()
    dfo1['old_Fiscal_Period'] = dfo1['old_Fiscal_Period'].str.strip()
    dfo1 = dfo1.sort_values(by = ['Original Sales_Order_Number', 'old_Fiscal_Period'], ascending = True)
    dfo1 = dfo1.groupby('Original Sales_Order_Number', group_keys=False).last().reset_index()
    # dfo1

    dfo2 = dfo[['New Sales_Order_Number','new_Fiscal_Period', 'new_sum(line_item_net_value)']].copy()
    dfo2['New Sales_Order_Number'] = dfo2['New Sales_Order_Number'].str.strip()
    dfo2['new_Fiscal_Period'] = dfo2['new_Fiscal_Period'].str.strip()
    dfo2 = dfo2.sort_values(by = ['New Sales_Order_Number', 'new_Fiscal_Period'], ascending = True)
    dfo2 = dfo2.groupby('New Sales_Order_Number', group_keys=False).last().reset_index()
    # dfo2

    df = dfo1.merge(new_df, how = 'left', left_on = 'Original Sales_Order_Number', right_on = 'Sales Order')
    df = df.merge(df_oit[['Sales Order','Exclude?']].drop_duplicates(), how = 'left', left_on = 'Original Sales_Order_Number', right_on = 'Sales Order', suffixes = ['_credited', '_protections'])
    df['new_crediting_value'].fillna(0, inplace = True)
    df.fillna('', inplace = True)

    df['status_old_SO'] = 'Unknown'

    df.loc[((df['new_crediting_value'] == 0) & (df['Exclude?'] == 'true')), 'status_old_SO'] = 'Not Credited, Protected'
    df.loc[((df['new_crediting_value'] != 0) & (df['Exclude?'] == 'true')), 'status_old_SO'] = 'Credited, Protected'
    df.loc[((df['new_crediting_value'] == 0) & (df['Exclude?'] != 'true')), 'status_old_SO'] = 'Not Credited, Not Protected'
    df.loc[((df['new_crediting_value'] != 0) & (df['Exclude?'] != 'true')), 'status_old_SO'] = 'Credited, Not Protected'

    df1 = df.merge(df_old[['Original Sales Order Number','New Sales Order Number']], left_on = 'Original Sales_Order_Number', right_on = 'Original Sales Order Number', how = 'left' )
    df1 = df1.merge(dfo2, left_on = 'New Sales Order Number', right_on = 'New Sales_Order_Number', how = 'left').fillna('')
    df1 = df1.merge(new_df[['Sales Order','Employee Name','new_crediting_value']] , how = 'left', left_on = ['New Sales_Order_Number','Employee Name'], right_on = ['Sales Order','Employee Name'], suffixes = ['_oldSO','_newSO'])
    df1['new_crediting_value_newSO'].fillna(0, inplace = True)
    df1.fillna('', inplace = True)


    df1['new_crediting_value_newSO'] = df1['new_crediting_value_newSO'].apply(rounding_off_to_zero)


    df1['Final_Status'] = 'Unknown'
    df1.loc[((df1['Exclude?'] == 'true') & (df1['new_crediting_value_newSO'] != 0)), 'Final_Status'] = 'Over Paid (Old SO : Protected, New SO: Credited)'
    df1.loc[((df1['Exclude?'] == 'true') & (df1['new_crediting_value_newSO'] == 0)), 'Final_Status'] = 'Old SO: Protected, New SO: Not Credited'
    df1.loc[((df1['Exclude?'] != 'true') & (df1['new_crediting_value_newSO'] != 0)), 'Final_Status'] = 'Old SO: Not Protected, New SO: Credited'
    df1.loc[((df1['Exclude?'] != 'true') & (df1['new_crediting_value_newSO'] == 0)), 'Final_Status'] = 'Under Paid (Old SO : Not Protected, New SO:Not Credited)'

    drop_col = ['Sales Order_credited', 'Sales Order_protections','Original Sales Order Number','Sales Order']
    df1.drop(drop_col, axis =1 , inplace = True)
    df1.rename(columns = {'New Sales Order Number' : 'Mapped SO from previous file'}, inplace = True)

    df1.to_csv('Updated R2 to R3 analysis.csv', index = False)

    l2 = dfo2['New Sales_Order_Number'].unique()
    l1 = df1['New Sales_Order_Number'].unique()
    so = []
    for i in l2:
        if i not in l1:
            so.append(i)

    if len(so) > 0:
        so = ['6600653501','6600653515','6600661074' ]
        df_not_found_so = pd.DataFrame(so, columns = ['New Sales_Order_Number'])
        df_not_found_so = df_not_found_so.merge(new_df, how = 'left', left_on = ['New Sales_Order_Number'], right_on = ['Sales Order'], suffixes = ['_oldSO','_newSO'])
        df_not_found_so['new_crediting_value'].fillna(0, inplace = True)
        df_not_found_so.fillna('', inplace = True)

        df_not_found_so = df_not_found_so.merge(df_oit[['Sales Order','Employee Name','Exclude?']].drop_duplicates(), how = 'left', left_on = ['New Sales_Order_Number','Employee Name'], right_on = ['Sales Order','Employee Name'], suffixes = ['_credited', '_protections'])
        df_not_found_so['Exclude?'].fillna('false', inplace = True)
        df_not_found_so.fillna('', inplace = True)
        df_not_found_so['Status'] = 'Unknown'
        df_not_found_so.loc[((df_not_found_so['Exclude?'] == 'true') & (df_not_found_so['Crediting Value'] == 0)), 'Status'] = 'Not Credited, Protected' 
        df_not_found_so.loc[((df_not_found_so['Exclude?'] == 'true') & (df_not_found_so['Crediting Value'] != 0)), 'Status'] = 'Credited, Protected' 
        df_not_found_so.loc[((df_not_found_so['Exclude?'] != 'true') & (df_not_found_so['Crediting Value'] == 0)), 'Status'] = 'Not Credited, Not Protected' 
        df_not_found_so.loc[((df_not_found_so['Exclude?'] != 'true') & (df_not_found_so['Crediting Value'] != 0)), 'Status'] = 'Credited, Not Protected' 
        df_not_found_so.to_csv('SO not found.csv', index = False)
    print('Files Created')
def main():
    start = time.time()

    start_overpayment()
    end = time.time()
    print("Execution Time : ",int(end-start) , "s")
