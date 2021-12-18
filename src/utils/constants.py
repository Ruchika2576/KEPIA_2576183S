
import plotly.express as px

# navigation bar headings and options
navigation_title = 'KEPIA NAVIGATION'
stored_set = 'Stored Set Analysis'
single_instance = 'Single Instance Analysis'
multiple_instance = 'Multiple Instances Analysis(100 Files)'
store_DB = 'Store Sets to DB(Only admin)'

# color scheme for graphs
single_orange = '#e64d00'
color_sequence = px.colors.sequential.RdBu
color_list = ['#ffbb99', '#e64d00', '#cc0044', '#800040']
two_colors = ['#ffbb99','#cc0044']

# utility strings
comma = ','
to = 'to'
horizontal_line = '***'

# kidney exchange allocator URL
kidney_exchange_allocator_url = 'https://kidney-nhs.optimalmatching.com/kidney/find.json'

# All JSON feilds
data = 'data'
recipients = 'recipients'
operation = 'operation'
altruistic_chain_length = 'altruistic_chain_length'
matches = 'matches'
source = 'sources'
altruistic = 'altruistic'
dage = 'dage'
bloodtype = 'bloodtype'
hasBloodCompatibleDonor = 'hasBloodCompatibleDonor'
cPRA = 'cPRA'
output = 'output'
exchange_data = 'exchange_data'
all_cycles = 'all_cycles'
exchanges = 'exchanges'
cycle_id = 'cycle Id'
cycle = 'cycle'
alt = 'alt'
weight = 'weight'
backarcs = 'backarcs'
description ='description'
two_way_exchanges ='two_way_exchanges'
three_way_exchanges ='three_way_exchanges'
total_transplants ='total_transplants'
donor = 'donor'

# Custom column names
matches_count = 'Matches Count'
Matches = 'Matches'
two_cycles = 'Two cycle'
three_cycles = 'Three cycle'
short_chains = 'Short Chain'
long_chains = 'Long Chain'
payload = 'payload'

# donors in set, column names
instance_id = 'Instance Id'
donors_count = 'No. of Donors'
avg_match = 'Avg No. of Matches'
max_match = 'Max No. of Matches'
alt_count = 'No. of Altruistic Donors'
nonalt_count = 'No. of Non Altruistic Donors'
multiple_source = 'Donors with Multiple Sources'
avg_age = 'Average Age of Donors'
min_age = 'Min Age of Donors'
max_age = 'Max Age of Donors'
median_age = 'Median Age of Donors'
a_type = 'A bloodtype Donors Count'
b_type = 'B bloodtype Donors Count'
o_type = 'O bloodtype Donors Count'
ab_type = 'AB bloodtype Donors Count'
no_match = 'Donors with No Matches'
min_match = 'Min No. of Matches'

recipients_count = 'No. of Recipients'
comp_count = 'No Compatible Donor count'
hascomp_count = 'Has Compatible Donor count'
a_rec_count = 'A bloodtype avg of Recipients'
b_rec_count = 'B bloodtype avg of Recipients'
o_rec_count = 'O bloodtype avg of Recipients'
ab_rec_count = 'AB bloodtype avg of Recipients'
cpra_mean = 'cPRA mean'
cpra_median = 'cPRA median'
cpra_std = 'cPRA std'

cycle_count = 'No. of Cycles'
Two_cycle_count = 'No. of Two Cycles'
Three_cycle_count = 'No. of Three Cycles'
sc_count='No. of Short chains'
lc_count = 'No. of Long chains'
avg_weight = 'Weight Avg'
med_weight = 'Weight Median'
std_weight= 'Weight std'
back_count = 'No. of Cycles with backarcs'

exc_count = 'No. of Exchange Cycles'
exc_weight='Weight of Exchanges'
two_exc_weight ='Two - way exchange'
three_way = 'Three Way exchange'
Total_transplants = 'Total Transplants'


# all success, error and warning messages
success1 = 'File Upload Successful.'
success2 = 'File Uploaded.Begin Analysis.'
success_text = ' **Zip File Extracted Successfully. Total Number of files extracted - **'

error1 = 'No file uploaded'
error2 = '!!! Exception has occurred while uploading the file try again, If Exception persists contact support.'
error3 = '!!! Exception has occurred while reading the file try again, If Exception persists contact support.'
error4 = 'Error in Response from https://kidney-nhs.optimalmatching.com/'
error5 = 'Error ocurred while fetching data from https://kidney-nhs.optimalmatching.com/'
error6 = 'No file uploaded! Refresh.'
error7 = '!!! Exception has occurred while multi_uploading the file try again, If Exception persists contact support.'
error8 = '!!! Exception has occurred while fetching data from external API. Please wait or contact if issue persist!!'

warning1 = 'Note: Refresh to upload a New File!!'
warning2 = 'File Uploading, Please Wait'
warning3 = 'Fetching Data From Database, Please Wait'
warning4 = "Please wait for Data Analysis to load"

# main headings across all pages
title = 'KEPIA'
full_form = ' ---Kidney Exchange Program Instance Analyser ---'

stored_heading = 'Stored Data Analysis'
single_instance_heading = 'Single Instance Analysis'
multiple_instance_heading = 'Multiple Instance Analysis'

# input headings across pages
multiple_file_upload = '#### Data Upload : Upload a zip file of instances for analysis'
file_upload = 'Choose a file : '
multiple_begin_button = 'Begin Analysis  '

single_file_upload = '#### Data Upload : Upload an instance file for analysis'
single_begin_analysis = 'Begin Analysis '

choose_operation = 'Choose Operation : '
choose_alt = 'Choose Altruistic Chain Length :'
operation_options = ('optimal', 'maxcard', 'pairs')
alt_options = ('1', '2')

select_stored_set = "#### Select a Set to Begin Analysis "
stored_set_option = "The exchange Cycles are stored with the following parameters - "
select_set_message ="Choose a Set (Refresh before changing the Set): "
set_options = (None, 'SetA','SetB','SetC', 'SetD', 'SetE', 'SetF')

# input display headings
upload_single_file = ' **_Uploaded File_** - '
operation_heading = ' **_Operation_ ** - '
alt_heading = '**_Altruistic Chain Length_** - '

# multiple instances headings
donor_expand_multiple = 'Analyse All Donors in the Set'
recipient_expand_multiple = 'Analyse All Recipient in the Set'
all_cycle_expand_multiple = 'Analyse All Cycles in the Set'
exchange_cycle_expand_multiple = 'Analyse All Exchanges in the Set'

donor_heading = '#### Donors Data Analysis in the Set:'
accumulative_donor = """##### Accumulative Statistics of the Donors in the set:"""
recipient_heading = """#### Recipients Data Analysis in Sets"""
accumulative_recipient ="""#### Accumulative statistics of the set"""
all_cycle_heading = """#### All cycles Analysis in Sets"""
accumulative_all_cycle = """#### Accumulative statistics of the set"""
exchange_cycle_heading = """#### Exchange cycles Analysis in Sets"""
all_cycle_accum = """#### Accumulative statistics of the set"""

heading_multiple_1 = """##### 1. Distribution of No. of Donors in the set"""
heading_multiple_2 = """##### 2. Distribution of Altruistic Donors in the set"""
heading_multiple_3 = """##### 3. Distribution of Donor Age in the set"""
heading_multiple_4 =  """##### 4.Distribution of Donor's Matches Count in the set"""
heading_multiple_5 = """##### 5. Blood Type Distribution of Donors in the set"""
heading_multiple_6 = """##### 6. Correlation of attributes in the Donor's set"""
heading_multiple_7 = """##### 7. Correlation Between two Attributes"""

heading_multiple_8 = """##### 1. Distribution of No. of Recipients in the set"""
heading_multiple_9 = """##### 2. Distribution of Recipients compatibility in the set"""
heading_multiple_10 = """##### 3. Blood Type Distribution of Recipients in the set"""
heading_multiple_11 = """##### 4. cPRA Distribution of Recipients in the set"""
heading_multiple_12 = """##### 6. Correlation of attributes in the Recipients's set"""
heading_multiple_13 = """##### 7. Correlation Between two Attributes"""
# heading_multiple_14 =
heading_multiple_14 = """ ##### 1. Distribution of No. of Cycles in the set"""
heading_multiple_15 = """##### 2. Weight Distribution of Cycles in the set"""
heading_multiple_16 = """##### 3. Cycle and chains Distribution in the set"""
heading_multiple_17 = """##### 4. Correlation of attributes in the All cycles set"""
heading_multiple_18 = """##### 5. Correlation Between two Attributes"""

heading_multiple_19 = """##### 1. Distribution of No. of Exchange Cycles in the set"""
heading_multiple_20 = """##### 2. Distribution of No. of Total Transplants"""
heading_multiple_21= """##### 3. Weight Distribution of Exchanges in the set"""
heading_multiple_22 = """##### 4. Cycle and chains Distribution in the set"""
heading_multiple_23 = """##### 5. Correlation of attributes in the Exchange Cycle set"""

sub_heading_multiple_1 ='Altruistic'
sub_heading_multiple_2 = 'Non Altruistic'
sub_heading_multiple_3 = 'Age values distribution in the sets'
sub_heading_multiple_4 = 'Distribution in the set'
sub_heading_multiple_5 = 'Correlation Matrix'
sub_heading_multiple_6 = 'Heatmap for Correlation Matrix'
sub_heading_multiple_7 = 'Select the Donor Attributes :'
sub_heading_multiple_8 = "Select attribute for X Axis:"
sub_heading_multiple_9 = "Select attribute for Y Axis:"
sub_heading_multiple_10 = 'Plot the Graph'
sub_heading_multiple_11 = 'Correlation between'
sub_heading_multiple_12  = 'Select the Recipients Attributes'
sub_heading_multiple_13 = 'Plot Scatter plot'
sub_heading_multiple_14 = 'Frequency in the Set'
sub_heading_multiple_15 = 'Select the Cycles Attributes  :'
sub_heading_multiple_16 = 'Plot the graph'
sub_heading_multiple_17 = 'Select the Exchanges Attributes  :'
sub_heading_multiple_18 = 'Plot the Graph:'
sub_heading_multiple_19 ='Weight values'
sub_heading_multiple_20 ='Description:'

graph_multi_title_1 = 'Donors Count distribution within the set  '
graph_multi_title_2 ='Altruistic Donors Distribution in the set'
graph_multi_title_3 = "Accumulative Distribution of Altruistic Donors in instances"
graph_multi_title_4 = "Distribution of Donor Age in the set"
graph_multi_title_5 ='Avg No. of Matches Count distribution  '
graph_multi_title_6 = "Accumulative Distribution in instances"
graph_multi_title_7 = 'Recipients Count distribution  '
graph_multi_title_8 ="Accumulative Distribution in instances"
graph_multi_title_9 ='No. of cycles distribution in the Set '
graph_multi_title_10 ='Weight distribution in the set'
graph_multi_title_11 ='Accumulative weight distribution in the instances  '
graph_multi_title_12 ='Distribution in the set'
graph_multi_title_13 ="Accumulative Distribution in instances"

graph_multi_title_14 ='No. of Exchange cycles distribution in the Set '
graph_multi_title_15 = 'No. of Transplants distribution in the Set '
graph_multi_title_16 = 'Exchanges Weight distribution in the set'
graph_multi_title_17 = 'Accumulative Exchanges weight distribution in the instances  '
graph_multi_title_18 = 'Accumulative Distribution in instances'

# single instances headings

donor_expand = 'Analyse Donors in the single_instance'
recipient_expand = 'Analyse All Recipient ofs the single_instance'
all_cycle_expand = 'Analyse All Cycles of the single_instance'
exchange_cycle_expand = 'Analyse Exchange Cycle of the single_instance'

single_donor_heading = ' #### Donor Data Analysis'
single_recipient_heading = '----------Recipients Data Analysis------------'
heading_1 = ' ###### 1. Total Donors : '
heading_2 = ' ###### 2. Donors with 0 matches : '
heading_3 = ' ###### 3. Altruistic Donors count : '
heading_4 = ' ###### 4. Donors with multiple Sources : '
heading_5 = ' ##### 5. Specific Donor Info (only non altruistic) - '
heading_6 = ' ##### 6. Donor Age Statistics : '
heading_7 = ' ##### 7. Donor Blood Type Distribution - '
heading_8 = ' ##### 8. Donor const.matches_count Statistics : '
heading_9 = ' ##### 9. Filter Donors : '
heading_10 = ' ###### 10. Filtered Donors List:'
heading_11 = ' ##### 1. Total No. of Recipients : '
heading_12 = " ##### 2. Recipients's Blood type Distribution "
heading_13 = ' ##### 3. Recipients Donor Compatibility Distribution : '
heading_14 = ' ##### 4. Recipients cPRA Statistics : '
heading_15 = ' ##### 5. Filter Recipients  '
heading_16 = '----------Exchange Cycle Analysis------------'
heading_17 = ' #####  Exchange Data: '
heading_18 = ' #####  Summary of Exchange Cycles: (Scroll right)'
heading_19 = ' ##### Total No. of Cycles: '
heading_20 = ' #####  Exchange Cycle Weight Statistics : '
heading_21 = ' ##### Backarcs in Exchange Data : '
heading_22 = '----------All Cycles Analysis------------'
heading_23 = ' ##### 3. Expand Specific Cycles - '
heading_24 = ' ##### 4. Cycle Weight Statistics : '
heading_25 = ' ##### 5. Backarcs : '

sub_heading_1 = ' , Donor Ids :'
sub_heading_2 = ' Sources with '
sub_heading_3 = 'Donors. '
sub_heading_4 = 'Two donors: '
sub_heading_5 = 'Three donors: '
sub_heading_6 = 'Four donors: '
sub_heading_7 = 'Select Donor Ids:'
sub_heading_8 = ' ##### 1. Cycles - '
sub_heading_9 = '  Total no. of 2 cycles - '
sub_heading_10 = '  Total no. of 3 cycles - '
sub_heading_11 = ' ##### 2. Chains - '
sub_heading_12 = '  Total no. of short chains - '
sub_heading_13 = '  Total no. of long chains - '
sub_heading_14 = 'Click to see all Exchange cycles'
sub_heading_15 = '**-----------Cycle:  **'
sub_heading_16 = 'Cycles Backarcs distribution '
sub_heading_17 = ' ##### **Donor -- **'
sub_heading_18 = ' **Source : ** '
sub_heading_19 = ' **dage : ** '
sub_heading_20 = ' **BloodType : ** '
sub_heading_21 = ' **Matches Count : ** '
sub_heading_22 = 'Select Cycle Ids:'
sub_heading_23 = 'Recipients counts'
sub_heading_24 = 'Has Compatible Donor '

form_name_1 = 'Filter Donors'
form_name_2 = 'Filter Donors'

filter_heading_1 = ' ###### Enter the Attribute Values(Default values select all donors):'
filter_heading_2 = 'Enter Age start range:'
filter_heading_3 = 'Enter Age end range:'
filter_heading_4 = 'Select Blood Type/Types:'
filter_heading_5 = 'Enter Matches count start range:'
filter_heading_6 = 'Enter Matches count end range:'
filter_heading_7 = 'Select altruistic Donor:'
filter_heading_8 = 'Total Count:'
filter_heading_9 = '1. Age Range: '
filter_heading_10 = '2. bloodtype: '
filter_heading_11 = '3. Altruistic: '
filter_heading_12 = '4. Matches Count Range:'
filter_heading_13 = ' ###### Enter the Attribute Values:'
filter_heading_14 = 'Filter Recipients:(Default Value Selects all Recipients)'
filter_heading_18 = 'Filter Recipients'
filter_heading_15 = 'Enter cPRA start range:'
filter_heading_16 = 'Enter cPRA end range:'
filter_heading_17 = 'Select Has Blood Compatible Donor:'
filter_heading_19 = ' ###### Filtered Recipients List:'
filter_heading_20 = '1. cPRA Range: '
filter_heading_21 = '3. hasBloodCompatibleDonor: '

graph_title_1 = 'Donor Age Distribution'
graph_title_2 = 'Donor blood type distribution (hover to see the bloodtype)'
graph_title_3 = 'Matches count Distribution'
graph_title_4 = 'Recipients blood type distribution (hover to see the bloodtype)'
graph_title_5 = 'Recipients Donor Compatibility distribution '
graph_title_6 = 'Recipients cPRA distribution  '
graph_title_7 = ' Chains and Cycles distribution '
graph_title_8 = 'Exchange Cycle Weight distribution  '
graph_title_9 = 'Exchange Cycles Backarcs distribution'
graph_title_10 = 'Cycle Weight distribution  '
graph_title_11 = 'Cycles Backarcs distribution'
graph_title_12 = "cPRA distribution in the sets"
graph_title_13 = 'Accumulative cPRA distribution in the instances  '

ins_string = 'Kepia@123'
head1 = "#### Data Upload : Only admin"
head2 = "Upload a zip file (10 files only) to store"
head3 = 'Enter the root File name * (File will be stored under this directory)'
head4 = 'Enter index  *(files will be stored as filename_index)'
head5 = "#### Data Delete : Only admin"
head6 = "Enter the root directory name and index"
head7 = 'Enter File name(root directory)'
head8 = 'Enter Start index'
head9 = 'Enter End index '
head10 = "delete"
head11 = "Choose a file : "
head12 = 'File Stored Successfully!!'
head13 = 'File Deleted Successfully!!'
error_head1 = "!!! Exception has occurred while uploading the file try again, If Exception persists contact support."
error_head2 = 'Zip File Upload and Extracted Successfully. Total Number of files extracted - '
error_head3 = "!!! Exception has occurred while reading the file try again, If Exception persists contact support."
enter_pas = "Enter admin password"
