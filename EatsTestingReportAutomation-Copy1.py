{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "#Importing Libraries\n",
    "\n",
    "from queryrunner_client import Client\n",
    "from warnings import filterwarnings\n",
    "filterwarnings(\"ignore\")\n",
    "import os\n",
    "from google_auth_oauthlib.flow import InstalledAppFlow\n",
    "from google.auth.transport.requests import Request\n",
    "import pickle\n",
    "from googleapiclient.discovery import build\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import pygsheets\n",
    "from datetime import datetime\n",
    "import pypostmaster\n",
    "\n",
    "from IPython.display import HTML\n",
    "from premailer import transform\n",
    "from urllib.parse import urlparse, urlencode\n",
    "\n",
    "pd.set_option('display.max_columns', None)\n",
    "\n",
    "from datetime import datetime\n",
    "import pytz\n",
    "\n",
    "from IPython.core.display import display,HTML"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      " ---- Authorization completed ---- \n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Setting up google sheet authorization\n",
    "\n",
    "SCOPES = ['https://www.googleapis.com/auth/drive']\n",
    "\n",
    "#     \"\"\"Shows basic usage of the Drive v3 API.\n",
    "#     Prints the names and ids of the first 10 files the user has access to.\n",
    "#     \"\"\"\n",
    "creds = None\n",
    "\n",
    "if os.path.exists('token.pickle'):\n",
    "    with open('token.pickle', 'rb') as token:\n",
    "        creds = pickle.load(token)\n",
    "# If there are no (valid) credentials available, let the user log in.\n",
    "if not creds or not creds.valid:\n",
    "    if creds and creds.expired and creds.refresh_token:\n",
    "        creds.refresh(Request())\n",
    "    else:\n",
    "        flow = InstalledAppFlow.from_client_secrets_file(\n",
    "            'client_secrets.json', SCOPES)\n",
    "        creds = flow.run_local_server(host='localhost',\n",
    "    port=8088)\n",
    "    # Save the credentials for the next run\n",
    "    with open('token.pickle', 'wb') as token:\n",
    "        pickle.dump(creds, token)\n",
    "\n",
    "service = build('drive', 'v3', credentials=creds)\n",
    "print('\\n ---- Authorization completed ---- \\n')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# defining function to pull data from google sheet\n",
    "\n",
    "def pull_sheet_data(SCOPES,SPREADSHEET_ID,RANGE_NAME):\n",
    "#     creds = gsheet_api_check(SCOPES)\n",
    "    service = build('sheets', 'v4', credentials=creds)\n",
    "    sheet = service.spreadsheets()\n",
    "    result = sheet.values().get(\n",
    "        spreadsheetId=SPREADSHEET_ID,\n",
    "        range=RANGE_NAME).execute()\n",
    "    values = result.get('values', [])\n",
    "    \n",
    "    if not values:\n",
    "        print('No data found.')\n",
    "    else:\n",
    "        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,\n",
    "                                  range=RANGE_NAME).execute()\n",
    "        data = rows.get('values')\n",
    "        print(\"COMPLETE: Data copied\")\n",
    "        return data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Format Table"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 117,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "COMPLETE: Data copied\n"
     ]
    }
   ],
   "source": [
    "# Importing Form Responses 2 sheet - Feature info table\n",
    "\n",
    "SPREADSHEET_ID = '1N6LOtg4Ip9yaW9xOGpxGYMXcOpx8t7kNeDCiK46Cw_w'\n",
    "data = pull_sheet_data(SCOPES,SPREADSHEET_ID,\"Form Responses 2!A:Z\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 118,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "COMPLETE: Data copied\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "140"
      ]
     },
     "execution_count": 118,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Importing Counter value\n",
    "\n",
    "Counter = int(pull_sheet_data(SCOPES,SPREADSHEET_ID, \"Counter!A2\")[0][0])\n",
    "Counter"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 120,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Getting all rows from the counter value\n",
    "\n",
    "data_format = pd.DataFrame(data)\n",
    "data_format.columns = data_format.iloc[0]\n",
    "data_format = data_format[1:] \n",
    "data_format = data_format.reset_index(drop=True)\n",
    "\n",
    "data_format=data_format[Counter:Counter+1]\n",
    "data_format=data_format.rename(columns={'OS Platform':'OS'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 122,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "21"
      ]
     },
     "execution_count": 122,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(data_format)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "data_format"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 123,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# data_format=data_format[data_format['Status']!='sent'].reset_index(drop=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 124,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "COMPLETE: Data copied\n"
     ]
    }
   ],
   "source": [
    "# Importing Build info details\n",
    "\n",
    "Build = pull_sheet_data(SCOPES,SPREADSHEET_ID,\"Build Info!A:C\")\n",
    "\n",
    "\n",
    "build_info=pd.DataFrame(Build)\n",
    "build_info.columns = build_info.iloc[0]\n",
    "build_info = build_info[1:] \n",
    "build_info = build_info.reset_index(drop=True)\n",
    "build_info=build_info.rename(columns={'OS':'Build_OS'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 126,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Okay\n"
     ]
    }
   ],
   "source": [
    "# merging form responses with build info - MASTER table\n",
    "\n",
    "df_ctest = pd.merge(data_format.assign(key=0), build_info.assign(key=0), on=['key']).drop('key', axis=1)\n",
    "df_ctest2 = df_ctest[((df_ctest['App'] == 'Eats & Carbon') & ((df_ctest['Build_OS'].str.contains('_E'))|((df_ctest['Build_OS'].str.contains('_C')))))|((df_ctest['App'] == 'Postmates & Carbon') & ((df_ctest['Build_OS'].str.contains('_P'))|((df_ctest['Build_OS'].str.contains('_C')))))|((df_ctest['App'] == 'Helix') & ((df_ctest['Build_OS'].str.contains('_H'))))]\n",
    "data_format_build = df_ctest2[((df_ctest2['OS'] == 'Both') & ((df_ctest2['Build_OS'].str.contains('Android'))|((df_ctest2['Build_OS'].str.contains('iOS')))))|((df_ctest2['OS'] == 'Android') & (df_ctest2['Build_OS'].str.contains('Android')))|((df_ctest2['OS'] == 'iOS') & (df_ctest2['Build_OS'].str.contains('iOS')))].reset_index()\n",
    "data_format_build['Date']=pd.to_datetime(data_format_build['Timestamp']).dt.date\n",
    "data_format_build = data_format_build.drop_duplicates(keep='first')\n",
    "if len(data_format_build)>0:\n",
    "    print('Okay')\n",
    "else: blah"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 129,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "COMPLETE: Data copied\n"
     ]
    }
   ],
   "source": [
    "# Importing T3 Board details\n",
    "\n",
    "T3 = pull_sheet_data(SCOPES,SPREADSHEET_ID,\"T3 Board!A:F\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 130,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Getting dashboard and master file links in T3 Board sheet\n",
    "\n",
    "df_T3Board= pd.DataFrame(T3)\n",
    "df_T3Board.columns = df_T3Board.iloc[0]\n",
    "df_T3Board = df_T3Board[1:] \n",
    "df_T3Board = df_T3Board.reset_index(drop=True)\n",
    "\n",
    "def create_clickable_pipeline(id):\n",
    "    url_template= '''<a href=\"{link}\" target=\"_blank\">{id}</a> '''.format(link=id[1],id=id[0])\n",
    "    return url_template\n",
    "\n",
    "df_T3Board[\"Jira Board\"]= df_T3Board[['Feature Name','Link']].apply(create_clickable_pipeline,axis=1)\n",
    "\n",
    "df_T3Board=df_T3Board.fillna(\"\")\n",
    "df_T3Board[\"Test Suite - Android\"]=\"\"\n",
    "df_T3Board[\"Test Suite - iOS\"]=\"\"\n",
    "df_T3Board[\"Test Suite - Web\"]=\"\"\n",
    "\n",
    "for i in range(len(df_T3Board)):\n",
    "    if(df_T3Board['Master sheet Android'][i]!=\"\"):\n",
    "        def create_clickable_pipeline(id):\n",
    "            url_template= '''<a href=\"{link}\" target=\"_blank\">Test Suite - Android</a> '''.format(link=id)\n",
    "            return url_template\n",
    "        df_T3Board[\"Test Suite - Android\"][i]= create_clickable_pipeline(df_T3Board['Master sheet Android'][i])\n",
    "    else:\n",
    "        df_T3Board[\"Test Suite - Android\"][i]=\"\"\n",
    "        \n",
    "    if(df_T3Board['Master sheet IOS'][i]!=\"\"):\n",
    "        def create_clickable_pipeline(id):\n",
    "            url_template= '''<a href=\"{link}\" target=\"_blank\">Test Suite - iOS</a> '''.format(link=id)\n",
    "            return url_template\n",
    "        df_T3Board[\"Test Suite - iOS\"][i]= create_clickable_pipeline(df_T3Board['Master sheet IOS'][i])\n",
    "    else:\n",
    "        df_T3Board[\"Test Suite - iOS\"][i]=\"\"\n",
    "        \n",
    "    if(df_T3Board['Master sheet WEB'][i]!=\"\"):\n",
    "        def create_clickable_pipeline(id):\n",
    "            url_template= '''<a href=\"{link}\" target=\"_blank\">Test Suite - Web</a> '''.format(link=id)\n",
    "            return url_template\n",
    "        df_T3Board[\"Test Suite - Web\"][i]= create_clickable_pipeline(df_T3Board['Master sheet WEB'][i])\n",
    "    else:\n",
    "        df_T3Board[\"Test Suite - Web\"][i]=\"\"\n",
    "        \n",
    "\n",
    "df_T3Board['MasterFile'] = df_T3Board['Test Suite - Android']+' '+df_T3Board['Test Suite - iOS']+' '+df_T3Board['Test Suite - Web']\n",
    "\n",
    "df_T3Board.drop(['Test Suite - Android','Test Suite - iOS','Test Suite - Web','Master sheet Android','Master sheet IOS','Master sheet WEB','Link'], axis=1,inplace=True)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Bug Summary Table"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 134,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "COMPLETE: Data copied\n"
     ]
    }
   ],
   "source": [
    "# Importing Form Responses 3 sheet - Bugs Summary Table\n",
    "\n",
    "data2 = pull_sheet_data(SCOPES,SPREADSHEET_ID,\"Form Responses 3!A:Z\")\n",
    "\n",
    "\n",
    "df_Defects=pd.DataFrame(data2)\n",
    "df_Defects.columns = df_Defects.iloc[0]\n",
    "df_Defects = df_Defects[1:] \n",
    "df_Defects = df_Defects.reset_index(drop=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 138,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Converting mobtest id links\n",
    "\n",
    "def create_clickable_pipeline4(id_str):\n",
    "    ids = id_str.split(',')  # split the comma-separated IDs\n",
    "    clickable_ids = []\n",
    "    for id in ids:\n",
    "        id = id.strip()  # remove whitespace around the ID\n",
    "        if id not in ['0', 'NA']:\n",
    "            url_template = '''<a href=\"https://t3.uberinternal.com/browse/{id}\" target=\"_blank\">{id}</a>'''.format(id=str(id))\n",
    "            clickable_ids.append(url_template)\n",
    "        else:\n",
    "            clickable_ids.append(id)\n",
    "    return ', '.join(clickable_ids) or None\n",
    "\n",
    "\n",
    "df_Defects[\"Ticket ID\"]= df_Defects['Ticket ID'].apply(lambda x: create_clickable_pipeline4(x) if ',' in str(x) else create_clickable_pipeline4(str(x)))\n",
    "df_Defects['Date']=pd.to_datetime(df_Defects['Timestamp']).dt.date\n",
    "df_Defects.index+=1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 139,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# merging t3 board table with MASTER table\n",
    "\n",
    "df_cum=pd.merge(data_format_build,df_T3Board, on=['Feature Name'],how='left')\n",
    "df_cum.index+=1\n",
    "df_cum = df_cum.applymap(lambda x: \"0\" if x == \"\" else x)\n",
    "df_cum['Tickets filed on JIRA']=df_cum['Tickets filed on JIRA'].astype(int)\n",
    "df_cum=df_cum.fillna('0')\n",
    "\n",
    "df_cum['Pass - Android']=df_cum['Pass - Android'].astype(int)\n",
    "df_cum['Fail - Android']=df_cum['Fail - Android'].astype(int)\n",
    "df_cum['Block - Android']=df_cum['Block - Android'].astype(int)\n",
    "df_cum['Pass - iOS']=df_cum['Pass - iOS'].astype(int)\n",
    "df_cum['Fail - iOS']=df_cum['Fail - iOS'].astype(int)\n",
    "df_cum['Block - iOS']=df_cum['Block - iOS'].astype(int)\n",
    "\n",
    "df_cum['Total TC - Android']=df_cum['Total TC - Android'].astype(int)\n",
    "df_cum['Total TC - iOS']=df_cum['Total TC - iOS'].astype(int)\n",
    "\n",
    "df_cum['Pass Percentage - Android']=(df_cum['Pass - Android']/df_cum['Total TC - Android'])\n",
    "df_cum['Fail Percentage - Android']=(df_cum['Fail - Android']/df_cum['Total TC - Android'])\n",
    "df_cum['Block Percentage - Android']=(df_cum['Block - Android']/df_cum['Total TC - Android'])\n",
    "df_cum['Pass Percentage - iOS']=(df_cum['Pass - iOS']/df_cum['Total TC - iOS'])\n",
    "df_cum['Fail Percentage - iOS']=(df_cum['Fail - iOS']/df_cum['Total TC - iOS'])\n",
    "df_cum['Block Percentage - iOS']=(df_cum['Block - iOS']/df_cum['Total TC - iOS'])\n",
    "\n",
    "df_cum=df_cum.fillna(0)\n",
    "\n",
    "def add_percent(x):\n",
    "    return \"{:.2%}\".format(x)\n",
    "\n",
    "df_cum['Pass Percentage - Android'] = df_cum['Pass Percentage - Android'].apply(add_percent)\n",
    "df_cum['Fail Percentage - Android']=df_cum['Fail Percentage - Android'].apply(add_percent)\n",
    "df_cum['Block Percentage - Android']=df_cum['Block Percentage - Android'].apply(add_percent)\n",
    "df_cum['Pass Percentage - iOS'] = df_cum['Pass Percentage - iOS'].apply(add_percent)\n",
    "df_cum['Fail Percentage - iOS']=df_cum['Fail Percentage - iOS'].apply(add_percent)\n",
    "df_cum['Block Percentage - iOS']=df_cum['Block Percentage - iOS'].apply(add_percent)\n",
    "\n",
    "df_cum['Notes/Callouts']=df_cum['Notes/Callouts'].str.replace('0','')\n",
    "\n",
    "\n",
    "# getting test cycle links into urls\n",
    "\n",
    "def create_clickable_pipeline4(id_str):\n",
    "    ids = id_str.split(',')  # split the comma-separated IDs\n",
    "    clickable_ids = []\n",
    "    for id in ids:\n",
    "        id = id.strip()  # remove whitespace around the ID\n",
    "        if id not in ['0', 'NA']:\n",
    "            url_template = '''<a href=\"https://t3.uberinternal.com/secure/Tests.jspa#/testPlayer/{id}\" target=\"_blank\">{id}</a>'''.format(id=str(id))\n",
    "            clickable_ids.append(url_template)\n",
    "        else:\n",
    "            clickable_ids.append(id)\n",
    "    return ', '.join(clickable_ids) or None\n",
    "\n",
    "\n",
    "df_cum['Test Cycles link - Android'] = df_cum['Test Cycles - Android'].apply(lambda x: create_clickable_pipeline4(x) if ',' in str(x) else create_clickable_pipeline4(str(x)))\n",
    "df_cum['Test Cycles link - iOS'] = df_cum['Test Cycles - iOS'].apply(lambda x: create_clickable_pipeline4(x) if ',' in str(x) else create_clickable_pipeline4(str(x)))\n",
    "\n",
    "df_cum.drop(['Test Cycles - Android','Test Cycles - iOS'],axis=1,inplace=True)\n",
    "\n",
    "\n",
    "# calculating TAT = current time - time of filling form\n",
    "\n",
    "current_time = datetime.now()\n",
    "\n",
    "df_cum['Timestamp'] = pd.to_datetime(df_cum['Timestamp'])\n",
    "df_cum['Timestamp_GMT'] = df_cum['Timestamp'] - pd.Timedelta(hours=5, minutes=30)\n",
    "df_cum['TAT'] = round(df_cum['Timestamp_GMT'].apply(lambda x: (current_time - x).total_seconds() / 3600),2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 140,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Converting MASTER table into required format\n",
    "\n",
    "table_main=df_cum.copy()\n",
    "table_main=table_main.drop('index',axis=1)\n",
    "\n",
    "table_main['OS Platform']=np.where(table_main['Build_OS'].str.contains('Android'),\"Android\",\"\")\n",
    "table_main['OS Platform']=np.where(table_main['Build_OS'].str.contains('iOS'),\"iOS\",table_main['OS Platform'])\n",
    "\n",
    "table_main = table_main.groupby(['Feature Name','Date','Status','App','OS Platform','OS','Project / JIRA BOARD','Jira Board','MasterFile','Notes/Callouts','Tickets filed on JIRA','TAT','OS Version - Android','Test Cycles link - Android','Total TC - Android','Pass - Android','Pass Percentage - Android','Fail - Android','Fail Percentage - Android','Block - Android','Block Percentage - Android','OS Version - iOS','Test Cycles link - iOS','Total TC - iOS','Pass - iOS','Pass Percentage - iOS','Fail - iOS','Fail Percentage - iOS','Block - iOS','Block Percentage - iOS'])['Build Name'].agg(' , '.join).reset_index()\n",
    "table_main.index+=1\n",
    "table_main=table_main.rename(columns={'Date':'Test Execution Date'})\n",
    "table_main['OS']=np.where(table_main['OS']=='Both','Android & iOS',table_main['OS'])\n",
    "table_main = table_main.pivot(index=['Feature Name','Test Execution Date','Status','App','OS','Project / JIRA BOARD','Jira Board','MasterFile','Notes/Callouts','Tickets filed on JIRA','TAT','OS Version - Android','Test Cycles link - Android','Total TC - Android','Pass - Android','Pass Percentage - Android','Fail - Android','Fail Percentage - Android','Block - Android','Block Percentage - Android','OS Version - iOS','Test Cycles link - iOS','Total TC - iOS','Pass - iOS','Pass Percentage - iOS','Fail - iOS','Fail Percentage - iOS','Block - iOS','Block Percentage - iOS'], columns=['OS Platform'], values='Build Name').reset_index()\n",
    "table_main=table_main.fillna('-')\n",
    "table_main.index+=1\n",
    "table_main['TAT']=table_main['TAT'].astype(str)\n",
    "table_main=table_main.rename(columns={'Jira Board':'Dashboard'})\n",
    "\n",
    "table_main['Test Cycles link - iOS']=table_main['Test Cycles link - iOS'].replace('0',\"-\")\n",
    "table_main['Test Cycles link - Android']=table_main['Test Cycles link - Android'].replace('0',\"-\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 142,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>New/Existing</th>\n",
       "      <th>Feature Name</th>\n",
       "      <th>Test Execution Date</th>\n",
       "      <th>Platform</th>\n",
       "      <th>App</th>\n",
       "      <th># Blocked cases</th>\n",
       "      <th>Bug/Task Title</th>\n",
       "      <th>Type of Tracking</th>\n",
       "      <th>Ticket ID</th>\n",
       "      <th>Ticket Type</th>\n",
       "      <th>Status</th>\n",
       "      <th>Priority</th>\n",
       "      <th>Assignee</th>\n",
       "      <th>Regression</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Existing</td>\n",
       "      <td>Restaurants on Trip Map</td>\n",
       "      <td>2023-06-21</td>\n",
       "      <td>Android &amp; iOS</td>\n",
       "      <td>Eats</td>\n",
       "      <td>13</td>\n",
       "      <td>Android &amp; iOS : Restaurants on Trip Map : Zoom...</td>\n",
       "      <td>Bug</td>\n",
       "      <td>&lt;a href=\"https://t3.uberinternal.com/browse/GT...</td>\n",
       "      <td>Block</td>\n",
       "      <td>Ready</td>\n",
       "      <td>P2</td>\n",
       "      <td>Carla Aguiar</td>\n",
       "      <td>NA</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "0 New/Existing             Feature Name Test Execution Date       Platform  \\\n",
       "2     Existing  Restaurants on Trip Map          2023-06-21  Android & iOS   \n",
       "\n",
       "0   App # Blocked cases                                     Bug/Task Title  \\\n",
       "2  Eats              13  Android & iOS : Restaurants on Trip Map : Zoom...   \n",
       "\n",
       "0 Type of Tracking                                          Ticket ID  \\\n",
       "2              Bug  <a href=\"https://t3.uberinternal.com/browse/GT...   \n",
       "\n",
       "0 Ticket Type Status Priority       Assignee Regression  \n",
       "2       Block  Ready       P2   Carla Aguiar         NA  "
      ]
     },
     "execution_count": 142,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Converting Bugs Summary Table into required format\n",
    "\n",
    "table_defects=df_Defects[['New/Existing','Feature Name','Date','Platform','App','Bug/Task Title','# Blocked cases','Type of Tracking','Ticket ID','Ticket Type','Status','Priority','Assignee','Regression']]\n",
    "table_defects['Platform']=np.where(table_defects['Platform']=='Both','Android & iOS',table_defects['Platform'])\n",
    "table_defects=table_defects[['New/Existing','Feature Name','Date','Platform','App','# Blocked cases','Bug/Task Title','Type of Tracking','Ticket ID','Ticket Type','Status','Priority','Assignee','Regression']]\n",
    "table_defects=table_defects.rename(columns={'Date':'Test Execution Date'})\n",
    "table_defects.index+=1"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Creating Body for Mail"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 152,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Comment out from and to addresses in the beginning to test\n",
    "\n",
    "def send_mail(df1,df2):\n",
    "    from_addr = 'bdua1@ext.uber.com'\n",
    "    to_addr = 'bdua1@ext.uber.com'\n",
    "    cc=[]\n",
    "    # from_addr = 'gss-app-testing@uber.com'\n",
    "    # to_addr =table_main2['TO'][i+1]\n",
    "    # cc=list(table_main2['CC'][i:i+1])[0]\n",
    "    # cc.append('bdua1@ext.uber.com')\n",
    "    # cc.append('gss-app-testing@uber.com')\n",
    "    \n",
    "    date = datetime.today().strftime('%Y-%m-%d')\n",
    "    subject = \"GSS - Eats - Sanity || {Feature} || {Dashboard} || {Date} || {OS}\".format(Feature=df1['Feature Name'][i+1], Dashboard=df1['Project / JIRA BOARD'][i+1], Date=df1['Test Execution Date'][i+1], OS=df1['OS'][i+1])\n",
    "\n",
    "    df12 =  df1.iloc[0:1][['Test Execution Date','Dashboard','Tickets filed on JIRA','TAT']].T\n",
    "    df12 = df12.reset_index()\n",
    "    df12.index = df12.index + 1\n",
    "    df12.columns = ['', '']\n",
    "    # df12.columns =  pd.MultiIndex.from_product([[\"{Feature}\".format(Feature=df1['Feature Name'][i+1])], df12.columns])\n",
    "\n",
    "    table1 = (df12.style.set_table_styles([{\n",
    "           'selector': 'th',\n",
    "           'props': [\n",
    "               ('background-color', 'white'),\n",
    "               ('color', 'white'),\n",
    "               ('border-color', 'white'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','0px'),\n",
    "               ('width', '160px'),\n",
    "           ('text-align', 'center')]},\n",
    "        {\n",
    "           'selector': 'td',\n",
    "           'props': [\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]\n",
    "        },\n",
    "        {'selector': '.row_heading',\n",
    "              'props': [('display', 'none'), ('text-align', 'center')]}\n",
    "        ]).hide_index().render())\n",
    "    \n",
    "    table2 = (df1[['App','Android','iOS']].style.set_table_styles([{\n",
    "           'selector': 'th',\n",
    "           'props': [\n",
    "               ('background-color', 'mediumblue'),\n",
    "               ('color', 'white'),\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]},\n",
    "        {\n",
    "           'selector': 'td',\n",
    "           'props': [\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "               ('width', '180px'),\n",
    "           ('text-align', 'center')]\n",
    "        },\n",
    "        {'selector': '.row_heading',\n",
    "              'props': [('display', 'none'), ('text-align', 'center')]}\n",
    "        ]).hide_index().render())\n",
    "    \n",
    "    table3 = (df1[['App','Android']].style.set_table_styles([{\n",
    "           'selector': 'th',\n",
    "           'props': [\n",
    "               ('background-color', 'mediumblue'),\n",
    "               ('color', 'white'),\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]},\n",
    "        {\n",
    "           'selector': 'td',\n",
    "           'props': [\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]\n",
    "        },\n",
    "        {'selector': '.row_heading',\n",
    "              'props': [('display', 'none'), ('text-align', 'center')]}\n",
    "        ]).hide_index().render())\n",
    "    \n",
    "    table4 = (df1[['App','iOS']].style.set_table_styles([{\n",
    "           'selector': 'th',\n",
    "           'props': [\n",
    "               ('background-color', 'mediumblue'),\n",
    "               ('color', 'white'),\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]},\n",
    "        {\n",
    "           'selector': 'td',\n",
    "           'props': [\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]\n",
    "        },\n",
    "        {'selector': '.row_heading',\n",
    "              'props': [('display', 'none'), ('text-align', 'center')]}\n",
    "        ]).hide_index().render())\n",
    "    \n",
    "    table5 = df1[['OS Version - Android','Test Cycles link - Android','Total TC - Android','Pass - Android','Pass Percentage - Android',\n",
    "                   'Fail - Android','Fail Percentage - Android','Block - Android','Block Percentage - Android']]\n",
    "    table5=(table5.rename(columns={'OS Version - Android':'OS Version','Test Cycles link - Android':'Test Cycles','Total TC - Android':'Total TC','Pass - Android':'Pass','Pass Percentage - Android':'Pass Percentage','Fail - Android':'Fail','Fail Percentage - Android':'Fail Percentage'\n",
    "                                                                                                                                 ,'Block - Android':'Block','Block Percentage - Android':'Block Percentage'}).style.set_table_styles([{\n",
    "           'selector': 'th',\n",
    "           'props': [\n",
    "               ('background-color', 'mediumblue'),\n",
    "               ('color', 'white'),\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "               ('width', '75px'),\n",
    "           ('text-align', 'center')]},\n",
    "        {\n",
    "           'selector': 'td',\n",
    "           'props': [\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]\n",
    "        },\n",
    "        {'selector': '.row_heading',\n",
    "              'props': [('display', 'none'), ('text-align', 'center')]}\n",
    "        ]).hide_index().render())\n",
    "    \n",
    "    table6 = df1[['OS Version - iOS','Test Cycles link - iOS','Total TC - iOS','Pass - iOS','Pass Percentage - iOS','Fail - iOS','Fail Percentage - iOS',\n",
    "                   'Block - iOS','Block Percentage - iOS']]\n",
    "    table6=(table6.rename(columns={'OS Version - iOS':'OS Version','Test Cycles link - iOS':'Test Cycles','Total TC - iOS':'Total TC','Pass - iOS':'Pass','Pass Percentage - iOS':'Pass Percentage','Fail - iOS':'Fail','Fail Percentage - iOS':'Fail Percentage'\n",
    "                                                                            ,'Block - iOS':'Block','Block Percentage - iOS':'Block Percentage'}).style.set_table_styles([{\n",
    "           'selector': 'th',\n",
    "           'props': [\n",
    "               ('background-color', 'mediumblue'),\n",
    "               ('color', 'white'),\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "               ('width', '75px'),\n",
    "           ('text-align', 'center')]},\n",
    "        {\n",
    "           'selector': 'td',\n",
    "           'props': [\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]\n",
    "        },\n",
    "        {'selector': '.row_heading',\n",
    "              'props': [('display', 'none'), ('text-align', 'center')]}\n",
    "        ]).hide_index().render())\n",
    "    \n",
    "    table7 = (df2[['New/Existing','Platform','App','Type of Tracking','Bug/Task Title','Ticket ID','Ticket Type','# Blocked cases','Status','Priority','Assignee','Regression']].style.set_table_styles([{\n",
    "           'selector': 'th',\n",
    "           'props': [\n",
    "               ('background-color', 'mediumblue'),\n",
    "               ('color', 'white'),\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]},\n",
    "        {\n",
    "           'selector': 'td',\n",
    "           'props': [\n",
    "               ('border-color', 'black'),\n",
    "               ('border-style ', 'solid'),\n",
    "               ('border-width','1px'),\n",
    "           ('text-align', 'center')]\n",
    "        },\n",
    "        {'selector': '.row_heading',\n",
    "              'props': [('display', 'none'), ('text-align', 'center')]}\n",
    "        ]).hide_index().render())\n",
    "    \n",
    "\n",
    "    \n",
    "    \n",
    "    html1=   \"\"\"\n",
    "                <p style=\"margin : 0; padding-top:0;\">Hi Team, </p>\n",
    "\n",
    "                <p style=\"margin : 0; padding-top:0;\"> GSS has performed sanity testing for <b><u>{Feature}</u></b> on {Date}, find the test run details below.</p>\n",
    "                <p style=\"margin : 0; padding-top:0;\"> {Notes}</p>\n",
    "                <br>\n",
    "                <h3 style=\"margin : 0; padding-top:0;\"<u>{Feature} - {OS}: </u> </h3>\n",
    "                {table1}\n",
    "                <br>\n",
    "                \"\"\".format(Feature=df1['Feature Name'][i+1], Date=df1['Test Execution Date'][i+1],Notes=df1['Notes/Callouts'][i+1],OS=df1['OS'][i+1],\n",
    "                      table1=transform(table1))\n",
    "    if df1['OS'][i+1]=='Android & iOS':\n",
    "        html2=\"\"\"<h3 style=\"margin : 0; padding-top:0;\"<u>Build Info: </u></h3>\n",
    "                {table2}\n",
    "                <br>\n",
    "                <h3 style=\"margin : 0; padding-top:0;\">Execution Summary Android: </h3>\n",
    "                {table5}\n",
    "                <br>\n",
    "                <h3 style=\"margin : 0; padding-top:0;\">Execution Summary iOS: </h3>\n",
    "                {table6}\n",
    "                <br>\n",
    "\n",
    "\n",
    "             \"\"\".format(table2=transform(table2),table5=transform(table5),table6=transform(table6))\n",
    "\n",
    "    elif df1['OS'][i+1]=='Android':\n",
    "        html2=\"\"\"<h3 style=\"margin : 0; padding-top:0;\"<u>Build Info: </u></h3>\n",
    "                {table3}\n",
    "                <br>\n",
    "                <h3 style=\"margin : 0; padding-top:0;\">Execution Summary Android: </h3>\n",
    "                {table5}\n",
    "                <br>\n",
    "\n",
    "\n",
    "             \"\"\".format(table3=transform(table3),table5=transform(table5))\n",
    "\n",
    "    else:\n",
    "        html2=\"\"\"<h3 style=\"margin : 0; padding-top:0;\"<u>Build Info: </u></h3>\n",
    "                {table4}\n",
    "                <br>\n",
    "                <h3 style=\"margin : 0; padding-top:0;\">Execution Summary iOS: </h3>\n",
    "                {table6}\n",
    "                <br>\n",
    "\n",
    "\n",
    "             \"\"\".format(table4=transform(table4),table6=transform(table6))\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "    conditions = (table_defects['Feature Name'].isin(table_main2['Feature Name'][i:i+1])) & (table_defects['Test Execution Date'].isin(table_main2['Test Execution Date'][i:i+1]))\n",
    "    if len( df2.loc[conditions])>0:\n",
    "        html3=\"\"\"\n",
    "                <h3 style=\"margin : 0; padding-top:0;\">Bug/Task Summary:  </h3>\n",
    "                {table7}\n",
    "                <br><br>\n",
    "                \n",
    "                \"\"\".format(table7=transform(table7))\n",
    "    else:\n",
    "        html3=''\n",
    "\n",
    "\n",
    "    html4=\"\"\"<p style=\"margin : 0; padding-top:0;\"><b>Note: </p>\n",
    "    <p style=\"margin : 0; padding-top:0;\">{MasterFile} </p>\n",
    "    <p style=\"margin : 0; padding-top:0;\">For any requests, suggestions or feedback please write to apoorvg@uber.com. </p>\n",
    "     <br>\n",
    "                <p style=\"margin : 0; padding-top:0;\">Thanks &amp; Regards,</p>\n",
    "                <p style=\"margin : 0; padding-top:0;\">GSS Testing Team</p>\n",
    "                </body>\n",
    "                </html>\n",
    "               \"\"\".format(MasterFile=df1['MasterFile'][i+1])\n",
    "\n",
    "\n",
    "# body stores the text contents of the email\n",
    "    body=html1+html2+html3+html4\n",
    "\n",
    "\n",
    "    \n",
    "# send the email \n",
    "\n",
    "    # print(to_addr)\n",
    "    # print(cc)\n",
    "    # display(HTML(body))\n",
    "    # print(from_addr, to_addr, df1['Feature Name'][i+1])\n",
    "    \n",
    "    \n",
    "    \n",
    "# to view the email format\n",
    "    \n",
    "    helper = pypostmaster.MailHelper()\n",
    "    print(helper.sendmail(from_addr, to_addr, subject, body,cc))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 186,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "COMPLETE: Data copied\n"
     ]
    }
   ],
   "source": [
    "# Importing Recipient List and merging with MASTER table\n",
    "\n",
    "Recipient = pull_sheet_data(SCOPES,SPREADSHEET_ID,\"Recipient List!A:C\")\n",
    "\n",
    "df_Recipient=pd.DataFrame(Recipient)\n",
    "df_Recipient.columns = df_Recipient.iloc[0]\n",
    "df_Recipient = df_Recipient[1:]\n",
    "df_Recipient = df_Recipient.reset_index(drop=True)\n",
    "\n",
    "df_Recipient['CC'] = df_Recipient['CC'].str.replace('\\n', '')\n",
    "df_Recipient['CC'] = df_Recipient['CC'].str.replace('\\r', '')\n",
    "df_Recipient['CC'] = df_Recipient['CC'].str.replace(' ', '')\n",
    "\n",
    "\n",
    "df_Recipient['TO'] = df_Recipient['TO'].str.replace('\\n', '')\n",
    "df_Recipient['TO'] = df_Recipient['TO'].str.replace('\\r', '')\n",
    "df_Recipient['TO'] = df_Recipient['TO'].str.replace(' ', '')\n",
    "\n",
    "df_Recipient['CC']=df_Recipient['CC'].str.split(',')\n",
    "\n",
    "\n",
    "# merging with MASTER table\n",
    "\n",
    "table_final=pd.merge(table_main,df_Recipient, on=['Feature Name'])\n",
    "table_final.index+=1\n",
    "\n",
    "table_main2=table_final.copy().reset_index(drop=True)\n",
    "table_main2.index+=1\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 154,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "21"
      ]
     },
     "execution_count": 154,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# checking length of MASTER table\n",
    "\n",
    "# len(table_main2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 156,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# sending emails for each row in MASTER table\n",
    "\n",
    "for i in range(0, table_main2.shape[0]):\n",
    "    conditions = (table_defects['Feature Name'].isin(table_main2['Feature Name'][i:i+1])) & (table_defects['Test Execution Date'].isin(table_main2['Test Execution Date'][i:i+1]))\n",
    "    send_mail(table_main2.iloc[i:i+1], table_defects.loc[conditions])\n",
    "    Counter += 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 157,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "160"
      ]
     },
     "execution_count": 157,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Counter"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 158,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[[160]]\n",
      "1 cells updated.\n"
     ]
    }
   ],
   "source": [
    "# # Updating Counter value in the sheet\n",
    "\n",
    "# def update_sheet_data(spreadsheet_id,sheet_name,data):\n",
    "#     service = build('sheets', 'v4', credentials=creds)\n",
    "#     values = [[data]]\n",
    "#     print(values)\n",
    "#     data = [\n",
    "#         {\n",
    "#             'range': sheet_name,\n",
    "#             'values': values\n",
    "#         },\n",
    "#     ]\n",
    "    \n",
    "#     body = {\n",
    "#         'valueInputOption': 'USER_ENTERED',\n",
    "#         'data': data\n",
    "#     }\n",
    "#     result = service.spreadsheets().values().batchUpdate(\n",
    "#         spreadsheetId=spreadsheet_id, body=body).execute()\n",
    "#     print('{0} cells updated.'.format(result.get('totalUpdatedCells')))\n",
    "\n",
    "\n",
    "# update_sheet_data(SPREADSHEET_ID, sheet_name='Counter!A2', data=Counter)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 159,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "160"
      ]
     },
     "execution_count": 159,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Counter"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "02. Python 3.7 (General DS)",
   "language": "python",
   "name": "python37"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
