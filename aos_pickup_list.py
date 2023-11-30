# %% [markdown]
# # Pickup List with shipping - 2021/11/27

# %%
import pandas as pd
import numpy as np

df1 = pd.read_csv('source/Cin7-Stock-27-11-2023.txt')
df2 = pd.read_csv('source/OrdersExport-27-11-2023.csv', parse_dates = ['Created Date'], dtype={'Delivery Postal Code': str, 'Billing Postal Code': str, 'Sales Rep':str, 'Tracking Code': str, 'Carrier':str, 'Surcharge Description': str,'Cancellation Date':str})

#fix20201104 adding SOH
product_list = df1[['Code','Name','StockAvail','SOH','AOSInternational-Brisbane','AOSInternational-Melbourne','AOSInternational-GoldCoast','AOSInternational-Sydney']]
order_list = df2[['Created Date','Email','Order Id','Order Ref','Item Code', 'Item Qty', 'Branch','Freight Description','Phone','First Name','Last Name','Item Row Format']]

df_merge = order_list.merge(product_list, left_on='Item Code', right_on='Code').sort_values(by=['Order Id'])

#df_merge.head(10)
#print(df_merge)
#df_merge

# %%
def fixOrderDate(df):
    created_datetime = pd.to_datetime(df['Created Date'])
    df['created_datetime'] = created_datetime

fixOrderDate(df_merge)

# %%
#Export to CSV
def export_to_file(df,fname):
    df.to_csv('output/'+fname+'.csv', mode='w', columns=['Created Date','Order Ref','First Name','Last Name','Email','Phone','Freight Description','Branch','Custom Email','Email List','OrderedProduct'], index = False, encoding='utf-8')

def export_to_excel_file(df,fname):
    df.to_excel('output/'+fname+'.xlsx', columns=['Created Date','Order Ref','First Name','Last Name','Email','Phone','Freight Description','Branch','Custom Email','Email List','OrderedProduct'], index = False, header=['_CreatedDate','_OrderRef','_FirstName','_LastName','_Email','_Phone','_FreightDescription','_Branch','_CustomEmail','_EmailList','_OrderedProduct'])

#fix20201104 adding SOH
def export_to_file_debug(df,fname):
    df.to_csv('output/'+fname+'.csv', mode='w', columns=['Created Date','Order Ref','OrderedProduct','First Name','Last Name','Email','Phone','Freight Description','Branch','Code','SOH','StockAvail', 'Item Qty','CurrentAvail','AOSInternational-Brisbane','AOSInternational-Melbourne','AOSInternational-GoldCoast','AOSInternational-Sydney'], index = False)

#added 11/16/2021
def export_to_file_debug_excel(df,fname):
    df.to_excel('output/'+fname+'.xlsx', columns=['Created Date','Order Ref','OrderedProduct','First Name','Last Name','Email','Phone','Freight Description','Branch','Code','SOH','StockAvail', 'Item Qty','CurrentAvail','AOSInternational-Brisbane','AOSInternational-Melbourne','AOSInternational-GoldCoast','AOSInternational-Sydney','Item Row Format','CurrentAvail'], index = False)

#added 20210112
def export_to_excel_debug(df,fname):
    df.to_excel('output/'+fname+'.xlsx', columns=['Created Date','Order Ref','OrderedProduct','Code','Name','First Name','Last Name','Email','Phone','Freight Description','Branch','SOH','StockAvail', 'Item Qty','CurrentAvail','AOSInternational-Brisbane','AOSInternational-Melbourne','AOSInternational-GoldCoast','AOSInternational-Sydney'], index = False)


#added 20201113 adding extra export list
def hide_email(ename, edomain):
    return ename.str[:-3] +'***@'+ edomain

#added 20201113 adding extra export list
def export_to_file_for_customer(df,fname,storename):
    email_part1 = df['Email'].str.split('@').str[0]
    email_part2 = df['Email'].str.split('@').str[1]
    modified_email = hide_email(email_part1, email_part2)

    modified_phone = df['Phone'].str.replace(' ','').str[:-6]+'******'

    df['Your Email'] = modified_email
    df['Your Phone'] = modified_phone

    df['Your Pickup Store'] = storename

    df.to_csv('output/'+fname+'.csv', mode='w', columns=['Created Date','Order Ref','Your Email','Your Phone','Your Pickup Store','Branch'], index = False, header=['Ordered Date','Order Ref','Your Email','Your Phone','Your Pickup Store','Ordered Branch'])



# %%
#drop ItemRowFormat = Parent, these are combo items that does not exist
#df_merge = df_merge['Item Row Format'] != 'Parent'
indexNames = df_merge[ df_merge['Item Row Format'] == 'Parent' ].index
df_merge.drop(indexNames , inplace=True)


len(df_merge)

# %%
#STEP1
#modified 20211116 a full list with shipping and pickups
#old list: pick_up_list = ["BNE Pickup","Gold Coast Pickup(下單後下週四取貨)","MEL Pickup","SYD Pickup"]

all_list = ["BNE Pickup","Gold Coast Pickup(下單後下週四取貨)","MEL Pickup","SYD Pickup","Free Shipping - No Frozen Food","Free Shipping - Frozen Food - BNE Designated Area","Free Shipping - Frozen Food - Gold Coast Designated Area","Free Shipping - Special Item","Seekit Shipping - No Frozen Food","Seekit Shipping - Frozen Food - BNE Designated Area","Seekit Shipping - Frozen Food - Gold Coast Designated Area","Seekit Shipping - No Frozen Food","Seekit Shipping - Frozen Food - MEL Designated Area","Free Shipping - No Frozen Food","Free Shipping - Special Item","Free Shipping - Frozen Food - MEL Designated Area","Seekit Shipping - No Frozen Food","Seekit Shipping - Frozen Food - SYD Designated Area","Free Shipping - No Frozen Food","Free Shipping - Special Item","Free Shipping - Frozen Food - SYD Designated Area"]

for index, row in df_merge.iterrows():
    if row['Freight Description'] not in all_list:
        df_merge = df_merge[df_merge['Order Id'] != row['Order Id']]

len(df_merge)

#df_merge.loc[df_merge['Order Ref'] == 'Bri17291']

# %%
#CURRENT SHIPPINGS
# BRIS
# Free Shipping - No Frozen Food'
# Free Shipping - Frozen Food - BNE Designated Area
# Free Shipping - Special Item
# Seekit Shipping - No Frozen Food
# Seekit Shipping - Frozen Food - BNE Designated Area
# GOL
# Free Shipping - Frozen Food - Gold Coast Designated Area
# Seekit Shipping - Frozen Food - Gold Coast Designated Area
# MEL
# Seekit Shipping - No Frozen Food
# Seekit Shipping - Frozen Food - MEL Designated Area
# Free Shipping - No Frozen Food
# Free Shipping - Special Item
# Free Shipping - Frozen Food - MEL Designated Area
# SYD
# Seekit Shipping - No Frozen Food
# Seekit Shipping - Frozen Food - SYD Designated Area
# Free Shipping - No Frozen Food
# Free Shipping - Special Item
# Free Shipping - Frozen Food - SYD Designated Area

# %%
#Create new df's according to each branch
#Select multiple conditions >>> df["A"][(df["B"] > 50) & (df["C"] == 900)]

#BRIS df
df_bris=pd.DataFrame()
#append all pickup orders
df_bris = df_bris.append(df_merge[(df_merge['Branch'] == 'AOS International - Brisbane, QLD') & (df_merge['Freight Description'] == 'BNE Pickup')])
#all all shipping orders
df_bris = df_bris.append(df_merge[(df_merge['Branch'] == 'AOS International - Brisbane, QLD') & ((df_merge['Freight Description'] == 'Free Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Free Shipping - Frozen Food - BNE Designated Area') | (df_merge['Freight Description'] == 'Free Shipping - Special Item') | (df_merge['Freight Description'] == 'Seekit Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Seekit Shipping - Frozen Food - BNE Designated Area'))])

#list out all shipping orders
#len(df_merge.loc[(df_merge['Branch'] == 'AOS International - Brisbane, QLD') & ((df_merge['Freight Description'] == 'Free Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Free Shipping - Frozen Food - BNE Designated Area') | (df_merge['Freight Description'] == 'Free Shipping - Special Item') | (df_merge['Freight Description'] == 'Seekit Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Seekit Shipping - Frozen Food - BNE Designated Area'))])
len(df_bris)

# %%
#MEL df
df_mel=pd.DataFrame()
#append all pickup orders
df_mel = df_mel.append(df_merge[(df_merge['Branch'] == 'AOS International - Melbourne, VIC') & (df_merge['Freight Description'] == 'MEL Pickup')])
#all all shipping orders
df_mel = df_mel.append(df_merge[(df_merge['Branch'] == 'AOS International - Melbourne, VIC') & ((df_merge['Freight Description'] == 'Seekit Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Seekit Shipping - Frozen Food - MEL Designated Area') | (df_merge['Freight Description'] == 'Free Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Free Shipping - Special Item') | (df_merge['Freight Description'] == 'Free Shipping - Frozen Food - MEL Designated Area'))])

len(df_mel)

# %%
#GOL df
df_gold=pd.DataFrame()
#note: branch = brisbane
#append all pickup orders
df_gold = df_gold.append(df_merge[(df_merge['Branch'] == 'AOS International - Brisbane, QLD') & (df_merge['Freight Description'] == 'Gold Coast Pickup(下單後下週四取貨)')])
#all all shipping orders
df_gold = df_gold.append(df_merge[(df_merge['Branch'] == 'AOS International - Brisbane, QLD') & ((df_merge['Freight Description'] == 'Free Shipping - Frozen Food - Gold Coast Designated Area') | (df_merge['Freight Description'] == 'Seekit Shipping - Frozen Food - Gold Coast Designated Area'))])

len(df_gold)

# %%
#SYD df
df_syd=pd.DataFrame()
#append all pickup orders
df_syd = df_syd.append(df_merge[(df_merge['Branch'] == 'AOS International - Sydney, NSW') & (df_merge['Freight Description'] == 'SYD Pickup')])
#all all shipping orders
df_syd = df_syd.append(df_merge[(df_merge['Branch'] == 'AOS International - Sydney, NSW') & ((df_merge['Freight Description'] == 'Seekit Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Seekit Shipping - Frozen Food - SYD Designated Area') | (df_merge['Freight Description'] == 'Free Shipping - No Frozen Food') | (df_merge['Freight Description'] == 'Free Shipping - Special Item') | (df_merge['Freight Description'] == 'Free Shipping - Frozen Food - SYD Designated Area') )])

len(df_syd)

# %%
#fix20201104 add this function
def sort_data2(df):
    newdf = df.sort_values(['created_datetime'], ascending=True)
    return newdf


#fix20201104 fix sorting
df_bris = sort_data2(df_bris)
df_gold = sort_data2(df_gold)
df_mel = sort_data2(df_mel)
df_syd = sort_data2(df_syd)

len(df_bris)
len(df_syd)
len(df_mel)
len(df_syd)

# %%
import math
def calculate_local_stock(df, stock_location):
    d = {} #a compare list
    df['CurrentAvail'] = ''
    for index, row in df.iterrows():
        if row['Code'] in d.keys():
            #print('had before')
            #print(d[row['Code']])
            #print(math.isnan(d[row['Code']]))
            #print(row['Item Qty'])
            df.at[index, 'CurrentAvail'] = d[row['Code']]-row['Item Qty']
            d[row['Code']] = d[row['Code']]-row['Item Qty']
        else:
            #print('new prod')
            #print(d)
            current_available = float(row[stock_location]-row['Item Qty'])
            df.at[index, 'CurrentAvail'] = current_available

            #add a new code to dictionary comparelist
            prod_code = row['Code']
            d[prod_code.format(index)] = current_available

    return df

df_mel = calculate_local_stock(df_mel, 'AOSInternational-Melbourne')
df_bris = calculate_local_stock(df_bris, 'AOSInternational-Brisbane')
df_gold = calculate_local_stock(df_gold, 'AOSInternational-GoldCoast')
df_syd = calculate_local_stock(df_syd, 'AOSInternational-Sydney')
len(df_mel)
len(df_bris)
len(df_gold)
len(df_syd)

# %%
def remove_no_stock(df):
    for index, row in df.iterrows():
        row['CurrentAvail']
        if row['CurrentAvail'] < 0 or np.isnan(row['CurrentAvail']):

            #key fix !!!!! remove all order ref found in this if statement
            indexNames = df[ df['Order Ref'] == row['Order Ref'] ].index
            df.drop(indexNames , inplace=True)

    return df

df_mel = remove_no_stock(df_mel)
df_bris = remove_no_stock(df_bris)
df_gold = remove_no_stock(df_gold)
df_syd = remove_no_stock(df_syd)
len(df_mel)
len(df_bris)
len(df_gold)
len(df_syd)

# %%
#modified 20210112

def makeOrderList(df):
    df['OrderedProduct']=''
    for index, row in df.iterrows():
        df_tmp_mel = pd.DataFrame()
        df_tmp_mel = df.loc[df['Order Ref'] == row['Order Ref']]

        orderd_product = ""
        for index, row in df_tmp_mel.iterrows():
            orderd_product += row['Name'] + '/'

        df.at[df['Order Ref'] == row['Order Ref'], 'OrderedProduct'] = orderd_product #todo :change to something faster

print('making order list')
makeOrderList(df_bris)
makeOrderList(df_mel)
makeOrderList(df_gold)
makeOrderList(df_syd)
print('finished making order list')


# %%
#STEP6 Get only unique Orders
def make_unique_orders(df):
    df = df.drop_duplicates(subset ="Order Id")
    return df

df_mel = make_unique_orders(df_mel)
df_bris = make_unique_orders(df_bris)
df_gold = make_unique_orders(df_gold)
df_syd = make_unique_orders(df_syd)

#print_result(df_gold, 'AOSInternational-GoldCoast')
len(df_mel)

# %%
#added1113 make sending email list
def make_sending_email_list(df):
    emailList = df['Email'].str.cat(sep=',')
    #print(emailList)
    df.at[0, 'Email List'] = emailList

#added1113 make custom email content
def make_custom_content(df):
    for index, row in df.iterrows():
        custom_email = '''Hi {0}
        Your Order: {1}, made on {2} is Now Ready for Pick Up at {3}.
        Order Items: {4}
        If you have any enquires, kindly contact us at: info@aosint.com.au'''
        #assign value
        df.at[index, 'Custom Email']= custom_email.format(row['First Name'], row['Order Ref'], row['Created Date'], row['Branch'], row['OrderedProduct'])

#added20211015 fix telephone format
def fix_telephone_format(df):
    df['Phone'] = df['Phone'].str.replace('+', '')
    #print(df['Phone'])

make_custom_content(df_bris)
make_custom_content(df_mel)
make_custom_content(df_gold)
make_custom_content(df_syd)
make_sending_email_list(df_bris)
make_sending_email_list(df_mel)
make_sending_email_list(df_gold)
make_sending_email_list(df_syd)
fix_telephone_format(df_bris)
fix_telephone_format(df_mel)
fix_telephone_format(df_gold)
fix_telephone_format(df_syd)

# %%
#export for internal use
export_to_excel_file(df_mel,'output_mel_0110')
export_to_excel_file(df_bris,'output_bris_0110')
export_to_excel_file(df_syd,'output_syd_010')
export_to_excel_file(df_gold,'output_gold_0110')


# %%
#added 20201113 export for customers
# export_to_file_for_customer(df_bris,'output_bris_customer_v1', 'Seekit Brisbane')
# export_to_file_for_customer(df_mel,'output_mel_customer_v1', 'Seekit Melbourne')
# export_to_file_for_customer(df_gold,'output_gold_customer_v1', 'Seekit Goldcost')
# export_to_file_for_customer(df_syd,'output_sdy_customer_v1', 'Seekit Sydney')

# %%



