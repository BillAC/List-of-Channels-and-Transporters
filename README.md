# List of Channels and Transporters

This repository was created in an attempt to compile a relatively comprehensive list of ion channels and transporters. The lists is focused on humans and mice.

## Sources

There are several sources available that list channels and transporters. They are partially overlapping with many entries unique to a given source. Here, we use the following sources:

### The IUPHAR/BPS Guide to Pharmacology repository

The IUPHAR/BPS Guide to Pharmacology repository is an open-access, expert-curated, online database that provides succinct overviews and key references for pharmacological targets and their recommended experimental ligands. It includes protein targets and ligand molecules, including approved drugs, small molecules, peptides and antibodies ([Harding et al](Nucleic%20Acids%20Res.%202024%20Jan%205;52(D1):D1438-D1449.%20doi:%2010.1093/nar/gkad944), PMID: 37897341). We queried database release 2023.3 on March 15, 2024, which listed 3,140 human targets and 2,968 mouse targets. Of interest to our needs are types ligand-gated ion channels (lgic), voltage-gated ion channels (vgic), other ion channels (other_ic), and transporters (transporter). This narrows the list to 830 and 802 targets for human and mouse respectively. The downloaded file (in CSV) was converted to Excel format (GtoPdb_targets_and_families.xlsx).

### RFA-RM-19-011

This NIH initiative, [Illuminating the Druggable Genome](https://commonfund.nih.gov/idg/index) (IDG), is directed to stimulate research into understudied proteins (non-olfactory GPCRs, protein kinases, and ion channels). [RFA-RM-19-011](https://grants.nih.gov/grants/guide/rfa-files/RFA-RM-19-011.html) listed 62 understudied ion channels (RFA-RM-19-011.xls). Using the [ID mapping](https://www.uniprot.org/id-mapping) tool of Uniprot, gene names were obtained for human, rat and mouse and saved in Excel format (RFA-RM-19-011_Uniprot_idmapping.xlsx).

### TransportDB

[TransportDB 2.0](http://www.membranetransport.org/transportDB2/index.html) is a relational database describing the predicted cytoplasmic membrane transport protein complement for organisms whose complete genome sequences are available. The transport proteins for each organism are classified into protein families according to the [TC classification system](tcdb.org), and functional/substrate predictions are provided. A [search](http://www.membranetransport.org/transportDB2/index.html) was performed March 15, 2024 for organism “Mus musculus”, which resulted in a list of 1,290 transport proteins. A search for “Homo sapiens” listed 1,467 transport proteins. These files are respectively saved as “TransportDB_mouse.csv” and “TransportDB_human.csv”.

The TransportDB exported files contain NCBI Reference Sequence protein names (e.g. NP_006832). We used g:Profiler [ID conversion tool](https://biit.cs.ut.ee/gprofiler/convert) to extract other relevant information, including gene names, for both of the species. The resulting outputs were respectively saved in Excel format as “TransportDB_human_gProfiler.xlsx” and “TransportDB_mouse_gProfiler.xlsx”.

### “Other” channel genes

A list of ion channels and transporters was compiled by the Coetzee lab over the years. Gene names for mouse and human ion channels and transporters were extracted from this repository, focusing on those not represented in the databases above. The gene names for mouse and human ion channels and transporters were cross-checked using the Uniprot ID mapper tool. The output of this tool was saved as an Excel file (Other_Uniprot.xlsx).

## Combining the lists

A script is provided, written in Python 3, to combine the various lists. The script is not meant to be robust and is used interactively as needed. The species to be used is declared near the top of the program, and should be either “Human” or “Mouse”. The working directory can also be defined. Provided that all the gene lists are present in the working directory, and named correctly, the script should produce an Excel file named according to the species selected (e.g. 'Master_genes_Human.xlsx').

### Formatting the output

The output of the Python script is a simple list of gene names. One can use an online gene name conversion tool to produce other relevant information. For example, we have used the Uniprot ID mapper tool to produce the two files named: “ICT_Master_list_Human.xlsx” and “ICT_Master_list_Mouse.xlsx”. For convenience, these two files are supplied in the root directory of this repository.

# License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

The vast majority of the gene lists are in the public domain, as described in “Sources”. The user is granted permission to freely use and distribute the gene names present in the “Other” channel genes list.

You should have received a copy of the GNU General Public License along with this program. If not, see \<http://www.gnu.org/licenses/\>.
