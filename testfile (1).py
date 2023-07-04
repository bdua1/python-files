{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# #Importing Libraries\n",
    "\n",
    "# from queryrunner_client import Client\n",
    "# from warnings import filterwarnings\n",
    "# filterwarnings(\"ignore\")\n",
    "# import os\n",
    "# from google_auth_oauthlib.flow import InstalledAppFlow\n",
    "# from google.auth.transport.requests import Request\n",
    "# import pickle\n",
    "# from googleapiclient.discovery import build\n",
    "# import pandas as pd\n",
    "# import numpy as np\n",
    "# import pygsheets\n",
    "# from datetime import datetime\n",
    "# import pypostmaster\n",
    "\n",
    "# from IPython.display import HTML\n",
    "# from premailer import transform\n",
    "# from urllib.parse import urlparse, urlencode\n",
    "\n",
    "# pd.set_option('display.max_columns', None)\n",
    "\n",
    "# from datetime import datetime\n",
    "# import pytz\n",
    "\n",
    "# from IPython.core.display import display,HTML"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'spreadsheetId': '1N6LOtg4Ip9yaW9xOGpxGYMXcOpx8t7kNeDCiK46Cw_w',\n",
       " 'updatedRange': \"'bhavya-test'!A2\",\n",
       " 'updatedRows': 1,\n",
       " 'updatedColumns': 1,\n",
       " 'updatedCells': 1}"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import gspread\n",
    "import pandas as pd\n",
    "\n",
    "SHEET_ID = '1N6LOtg4Ip9yaW9xOGpxGYMXcOpx8t7kNeDCiK46Cw_w'\n",
    "SHEET_NAME = 'bhavya-test'\n",
    "gc = gspread.service_account('credentials.json')\n",
    "spreadsheet = gc.open_by_key(SHEET_ID)\n",
    "worksheet = spreadsheet.worksheet(SHEET_NAME)\n",
    "rows = worksheet.get_all_records()\n",
    "\n",
    "sheet_data = pd.DataFrame(rows)\n",
    "\n",
    "# gc = gspread.authorize(credentials)\n",
    "# sheet = gc.open('Your Google Sheet Name').sheet1\n",
    "\n",
    "# Read data from cell A1\n",
    "data = worksheet.acell('A1').value\n",
    "\n",
    "# Paste the data into cell A2\n",
    "worksheet.update('A2', data)"
   ]
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
