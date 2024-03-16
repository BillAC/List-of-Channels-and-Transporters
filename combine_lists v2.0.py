#!/usr/bin/env python

# -------------------------------------------------------------------
# Create a list of ion channels and transporters 
#
# The master gene list is created by combining data from several sources, 
# as outlined in the README.md file
#    

#from Bio import Entrez
import pandas as pd
import os

__debugging__ = False

# Select species
species = "Human"   # can be Human or Mouse

# Sets working directory
wd = r"X:\Programming\Python\channel_list\List of Channels and Transporters\lists"


###############################################################################
def IUPHAR (species):
    # Process the IUPHAR/BPS list
    #species = "Human" or "Mouse"
    in_file = 'GtoPdb_targets_and_families.xlsx'
    file_path = os.path. join (wd, in_file)
    df = pd.read_excel(file_path, skiprows=1)
    
    # Inspect the dataframe
    if __debugging__:
        type(df)    # <class 'pandas.core.frame.DataFrame'>
        df.head()
        list(df.columns.values)   # names of columns
    
    match species:
        case "Human":
            genecol = "HGNC symbol"
        case "Mouse":
            genecol = "MGI symbol"
        case "Rat":
            genecol = "RGD id"
        case _ :
            genecol = "HGNC symbol" 
    
    # get a list of the gene names
    IUPHAR = df.loc[df['Type'].isin(['lgic','other_ic', 'transporter', 'vgic'])]
    IUPHAR_genes = IUPHAR[genecol]
    IUPHAR_genes = IUPHAR_genes.to_frame()
    
    # drop rows where IUPHAR[genecol] is blank (or NaN)
    if IUPHAR_genes.isnull().values.any():
        #print('Removed NaN in IUPHAR')
        IUPHAR_genes = IUPHAR_genes.dropna()
    
    # rename to column 
    IUPHAR_genes.rename(columns = {genecol:'GeneName'}, inplace = True)
    
    # make sure that gene names are correctly capitilized
    match species:
        case "Human":
            IUPHAR_genes['GeneName'] = IUPHAR_genes['GeneName'].str.upper()
        case _ :
            IUPHAR_genes['GeneName'] = IUPHAR_genes['GeneName'].str.capitalize()
    
    # identify dups and drop them, if any
    if IUPHAR_genes.duplicated().any():
        print(IUPHAR_genes.loc[IUPHAR_genes.duplicated()], end='\n\n')
        IUPHAR_genes.drop_duplicates()
        print('Duplicates in IUPHAR have been deleted ')
    
    #IUPHAR_genes.GeneName.str.count(r'None').sum()
    
    return IUPHAR_genes


###############################################################################
def RFA (species):
    # Open the RFA-RM-19-011 list
    #sp = "Human"
    match species:
        case "Human":
            species = 'Homo sapiens (Human)'
        case "Mouse":
            species = "Mus musculus (Mouse)"
        case "Rat":
            species = "Rattus norvegicus (Rat)"
        case "Bovine":
            species = "Bos taurus (Bovine)"
        case _ :
            species = 'Homo sapiens (Human)'
    
    in_file = 'RFA-RM-19-011_Uniprot_idmapping.xlsx'
    file_path = os.path. join (wd, in_file)
    df2 = pd.read_excel(file_path)
    
    # Inspect the dataframe
    if __debugging__:
        df2.head()
        list(df2.columns.values)   # names of columns
    
    RFA = df2.loc[df2['Organism'].isin([species])]
    RFA = RFA.loc[RFA['Reviewed'].isin(['reviewed'])]
    RFA_genes = RFA['GeneName'].to_frame()
    #RFA_genes.rename(columns = {'Gene Names (primary)':'GeneName'}, inplace = True)
    RFA_genes = RFA_genes.dropna()
    
    # make sure that gene names are correctly capitilized
    match species:
        case "Human":
            RFA_genes['GeneName'] = RFA['GeneName'].str.upper()
        case _ :
            RFA_genes['GeneName'] = RFA['GeneName'].str.capitalize()
    
    # identify dups and drop them
    if RFA_genes.duplicated().any():
        print(RFA_genes.loc[RFA_genes.duplicated()], end='\n\n')
        RFA_genes.drop_duplicates()
        print('Duplicates in RFA have been deleted ')
        # make sure to check 5150 CACNG8 and 13462 KCNG4
    else:
        print('There are no duplciate genes in RFA')
    
    # rename the column
    RFA_genes = RFA_genes.reset_index(drop=True).sort_values(by=['GeneName'])
    
    return (RFA_genes)
    
###############################################################################
def TransportDB (species):
    # Open the TransportDB list
    #species = "Human"
    match species:
        case "Mouse":
            in_file = 'TransportDB_mouse_gProfiler.xlsx'
        case _ :
            in_file = 'TransportDB_human_gProfiler.xlsx'
    
    file_path = os.path. join (wd, in_file)
    df4 = pd.read_excel(file_path)
    
    # Inspect the dataframe
    if __debugging__:
        df4.head()
        list(df4.columns.values)   # names of columns
    
    TransportDB_genes = df4['name'].to_frame()
    TransportDB_genes.rename(columns = {'name':'GeneName'}, inplace = True)
    
    # make sure that gene names are correctly capitilized
    match species:
        case "Human":
            TransportDB_genes['GeneName'] = TransportDB_genes['GeneName'].str.upper()
        case _ :
            TransportDB_genes['GeneName'] = TransportDB_genes['GeneName'].str.capitalize()
    
    # remove NaN
    TransportDB_genes = TransportDB_genes.dropna()
    
    # remove 'None', if any
    if TransportDB_genes.GeneName.str.count(r'None').sum() > 0:
        indexNone = TransportDB_genes[ TransportDB_genes.GeneName.str.contains(r'None') ].index
        TransportDB_genes.drop(indexNone , inplace=True)
    
    # identify dups and drop them, if any
    if TransportDB_genes.duplicated().any():
        print(TransportDB_genes.loc[TransportDB_genes.duplicated()], end='\n\n')
        TransportDB_genes = TransportDB_genes.drop_duplicates()
        print('Duplicates in TransportDB have been deleted ')
        # 
    else:
        print('There are no duplicates human genes in TransportDB')
    
    TransportDB_genes = TransportDB_genes.reset_index(drop=True).sort_values(by=['GeneName'])
    return TransportDB_genes



###############################################################################
def Other(species):
    # Open the list of 'other' (or additional) channels and transporters
    
    #species = "Human"
    match species:
        case "Human":
            col = 'Homo sapiens (Human)'
        case "Mouse":
            col = "Mus musculus (Mouse)"
        case _ :
            col = 'Homo sapiens (Human)'
    
    in_file = 'Other_Uniprot.xlsx'
    
    file_path = os.path. join (wd, in_file)
    df3 = pd.read_excel(file_path)
    
    if __debugging__:
        df3.head()
        list(df3.columns.values)   # names of columns
    
    # Extract genes relevant to the orgamism
    df3 = df3.loc[df3['Organism'].isin([col])]
    
    other_genes = df3['GeneName']
    other_genes=other_genes.to_frame()
    
    # remove NaN
    other_genes = other_genes.dropna()
    
    # make sure that gene names are correctly capitilized
    match species:
        case "Human":
            other_genes['GeneName'] = other_genes['GeneName'].str.upper()
        case _ :
            other_genes['GeneName'] = other_genes['GeneName'].str.capitalize()
    
    # identify dups and drop them
    if other_genes.duplicated().any():
        print(other_genes.loc[other_genes.duplicated()], end='\n\n')
        other_genes = other_genes.drop_duplicates()
        print('Duplicates in other_genes have been deleted ')
        # 
    else:         
        print('There are no duplicate genes in other_genes')

    #other_genes.GeneName.str.count(r'None').sum()
    return(other_genes)

###############################################################################
# Read the gene lists
###############################################################################

IUPHAR_genes = IUPHAR(species)
print('There are ' + str(len(IUPHAR_genes)) + ' ' + species +' genes in IUPHAR')

RFA_genes = RFA(species)
print('There are ' + str(len(RFA_genes)) + ' ' + species + ' genes in the RFA')

TransportDB_genes = TransportDB (species)
print('There are ' + str(len(TransportDB_genes)) + ' ' + species + ' genes in the TransportDB list')

other_genes = Other(species)
print('There are ' + str(len(other_genes)) + ' genes in the other_genes list')


###############################################################################
# Compare other lists with TransportDB since it is the largest
###############################################################################

# Are there any genes in IUPHAR that are not in TransportDB?
#-------------------------------------------------------------
df_merged = TransportDB_genes.merge(IUPHAR_genes, how="right",  \
        left_on=["GeneName"], right_on=["GeneName"], indicator=True)
if df_merged.query("_merge == 'right_only'").size > 0:
    print('Merging TransportDB_genes with IUPHAR_genes to create a list named Master_genes')
    # create a master list that combines the two 
    toadd = df_merged.loc[df_merged['_merge'].isin(['right_only'])]['GeneName']
    toadd = toadd.to_frame()
    toadd.rename(columns = {toadd.columns.values[0]:TransportDB_genes.columns.values[0]}, inplace = True)
    Master_genes = pd.concat([TransportDB_genes, toadd], ignore_index = False)
    Master_genes.reset_index(drop=True, inplace=True)    
else:
    print('All IUPHAR_genes entries are already present in TransportDB_genes')
print('There are ' + str(len(Master_genes)) + ' genes in the Master_genes list')

# Merge genes in RFA with the master list
#-------------------------------------------------------------
df_merged = Master_genes.merge(RFA_genes, how="outer",  \
        left_on=["GeneName"], right_on=["GeneName"], indicator=True)
df_merged.reset_index(drop=True, inplace=True)

temp = df_merged.query("_merge == 'right_only'")
if temp['GeneName'].size > 0:
    print(str(temp['GeneName'].size) + ' RFA genes will be added to Master_genes')
else:
    print('All RFA_genes entries are already present in Master_genes')

Master_genes = df_merged
Master_genes.drop('_merge', axis=1, inplace=True)
print('There are ' + str(len(Master_genes)) + ' genes in the Master_genes list')    

# Are there any genes in other_genes that are not in the master list?
#-------------------------------------------------------------
df_merged = Master_genes.merge(other_genes, how="outer",  \
        left_on=["GeneName"], right_on=["GeneName"], indicator=True)
df_merged.reset_index(drop=True, inplace=True)    
    
temp = df_merged.query("_merge == 'right_only'")
if temp['GeneName'].size > 0:
    print(str(temp['GeneName'].size) + ' Other genes will be added to Master_genes')
else:
    print('All Other_genes entries are already present in Master_genes')

Master_genes = df_merged
Master_genes.drop('_merge', axis=1, inplace=True)
print('There are ' + str(len(Master_genes)) + ' genes in the ' + species + ' Master_genes list')   
       
# Export the master list
#-------------------------------------------------------------
file_name = 'Master_genes_' + species + '.xlsx'   
file_path = os.path. join (wd, file_name)
Master_genes.to_excel(file_path)




