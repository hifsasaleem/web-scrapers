{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNpJThaxyOYiyjljBiqU7wB"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "import requests\n",
        "import pandas as pd\n",
        "import sys\n",
        "import time\n",
        "from bs4 import BeautifulSoup\n",
        "\n",
        "headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}\n",
        "\n",
        "start = 0\n",
        "end = 80\n",
        "for n in range(start,end):\n",
        "  newrow_list = []\n",
        "  url = f\"https://experts.webflow.com/browse?fe088fc9_page={n}\"\n",
        "  response = requests.get(url)\n",
        "  soup = BeautifulSoup(response.content, \"html.parser\")\n",
        "  divs = soup.find_all(\"div\", {\"class\": \"experts-item w-dyn-item\"})\n",
        "  for div in divs:\n",
        "    try:\n",
        "       p = div.find(\"p\",{\"class\":\"line-clamp-3\"}).text\n",
        "       a = div.find(\"a\",{\"class\":\"experts-item_link w-inline-block\"})[\"href\"]\n",
        "       name = div.find(\"h2\",{\"class\":\"experts-item_name\"}).text\n",
        "       info = div.find(\"div\",{\"class\":\"experts-item-info_wrapper\"}).text\n",
        "       img = div.find(\"img\",{\"class\":\"experts-item_profile-image\"})[\"src\"]\n",
        "       res = requests.get(a)\n",
        "       soup2 = BeautifulSoup(res.content, \"html.parser\")\n",
        "       weblink = soup2.find(\"a\",{\"class\":\"--styled-dbGEqI wf-1ecmo1\"})[\"href\"]\n",
        "       starting = soup2.find(\"span\",{\"class\":\"--styled-cfxuxD --pick-dBJKbx wf-dq4t4e\"}).text\n",
        "       about = soup2.find(\"p\",{\"class\":\"--styled-gqIQop --pick-dBJKbx wf-1oigpre\"}).text\n",
        "       new_row = [name,a,img,info,p,about,weblink,starting]\n",
        "       newrow_list.append(new_row)\n",
        "    except:\n",
        "      pass\n",
        "\n",
        "\n",
        "  df = pd.DataFrame.from_dict(newrow_list)\n",
        "  df.to_csv('webflow_data.csv', mode='a', index=False, header=False)\n",
        "  sys.stdout.write(\"\\r %d of %d Pages Successfully Scraped\"%(n,end))\n",
        "  sys.stdout.flush()\n",
        "\n",
        "columns=[\"Company\",\"Profile\",\"img_link\",\"Location\",\"description\",\"About\",\"Website Link\",\"Strating At\"]\n",
        "csv_data = pd.read_csv(\"webflow_data.csv\",names=columns)\n",
        "df = pd.DataFrame(csv_data,columns=columns)\n",
        "df.to_csv('webflow_data.csv')\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "EdjloSbmqLwn",
        "outputId": "e9f5a731-4e2e-41e5-e37a-5810144ed52d"
      },
      "execution_count": 64,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            " 79 of 80 Pages Successfully Scraped"
          ]
        }
      ]
    }
  ]
}