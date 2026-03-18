{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyO+ZvOqSeF7609eubPdvQ87",
      "include_colab_link": true
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
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Mrrichards76/mip-dashboard/blob/main/scrapers/github_scraper.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "dTN0HHcQ0dxF",
        "outputId": "9ca9673e-fa57-4777-ec9b-ce347d24591d"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Signals table is ready!\n"
          ]
        }
      ],
      "source": [
        "import sqlite3\n",
        "\n",
        "# Connect to your database\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "c = conn.cursor()\n",
        "\n",
        "# Create signals table if it doesn't exist\n",
        "c.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS signals (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    company TEXT,\n",
        "    signal_type TEXT,\n",
        "    source TEXT,\n",
        "    timestamp TEXT,\n",
        "    strength REAL,\n",
        "    details TEXT\n",
        ")\n",
        "\"\"\")\n",
        "conn.commit()\n",
        "conn.close()\n",
        "\n",
        "print(\"Signals table is ready!\")"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install PyGitHub"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "oaxNIaqI1usa",
        "outputId": "c19c652b-2e93-4a16-c45d-7abed3cf717a"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting PyGitHub\n",
            "  Downloading pygithub-2.8.1-py3-none-any.whl.metadata (3.9 kB)\n",
            "Collecting pynacl>=1.4.0 (from PyGitHub)\n",
            "  Downloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl.metadata (10.0 kB)\n",
            "Requirement already satisfied: requests>=2.14.0 in /usr/local/lib/python3.12/dist-packages (from PyGitHub) (2.32.4)\n",
            "Requirement already satisfied: pyjwt>=2.4.0 in /usr/local/lib/python3.12/dist-packages (from pyjwt[crypto]>=2.4.0->PyGitHub) (2.11.0)\n",
            "Requirement already satisfied: typing-extensions>=4.5.0 in /usr/local/lib/python3.12/dist-packages (from PyGitHub) (4.15.0)\n",
            "Requirement already satisfied: urllib3>=1.26.0 in /usr/local/lib/python3.12/dist-packages (from PyGitHub) (2.5.0)\n",
            "Requirement already satisfied: cryptography>=3.4.0 in /usr/local/lib/python3.12/dist-packages (from pyjwt[crypto]>=2.4.0->PyGitHub) (43.0.3)\n",
            "Requirement already satisfied: cffi>=2.0.0 in /usr/local/lib/python3.12/dist-packages (from pynacl>=1.4.0->PyGitHub) (2.0.0)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests>=2.14.0->PyGitHub) (3.4.5)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests>=2.14.0->PyGitHub) (3.11)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests>=2.14.0->PyGitHub) (2026.2.25)\n",
            "Requirement already satisfied: pycparser in /usr/local/lib/python3.12/dist-packages (from cffi>=2.0.0->pynacl>=1.4.0->PyGitHub) (3.0)\n",
            "Downloading pygithub-2.8.1-py3-none-any.whl (432 kB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m432.7/432.7 kB\u001b[0m \u001b[31m11.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading pynacl-1.6.2-cp38-abi3-manylinux_2_34_x86_64.whl (1.4 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m1.4/1.4 MB\u001b[0m \u001b[31m37.2 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: pynacl, PyGitHub\n",
            "Successfully installed PyGitHub-2.8.1 pynacl-1.6.2\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from github import Github\n",
        "import sqlite3\n",
        "import datetime\n",
        "\n",
        "# 1️⃣ Connect to SQLite\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "c = conn.cursor()\n",
        "\n",
        "# 2️⃣ GitHub API - replace with your token if needed\n",
        "g = Github()  # No token needed for public repos, optional for higher rate limits\n",
        "\n",
        "# 3️⃣ Companies to track (use GitHub usernames/repos)\n",
        "companies_to_watch = [\"openai\", \"tensorflow\", \"pytorch\"]  # example\n",
        "\n",
        "for company in companies_to_watch:\n",
        "    try:\n",
        "        repo = g.get_user(company).get_repos()[0]  # first repo of user/org\n",
        "        commits_last_week = repo.get_commits(since=datetime.datetime.now() - datetime.timedelta(days=7)).totalCount\n",
        "        stars = repo.stargazers_count\n",
        "\n",
        "        # Calculate normalized strength (0-1 scale)\n",
        "        strength = min(commits_last_week / 50 + stars / 100, 1)\n",
        "\n",
        "        # Insert signal into database\n",
        "        c.execute(\"\"\"\n",
        "        INSERT INTO signals (company, signal_type, source, timestamp, strength, details)\n",
        "        VALUES (?, ?, ?, ?, ?, ?)\n",
        "        \"\"\", (\n",
        "            company,\n",
        "            \"github_spike\",\n",
        "            \"GitHub\",\n",
        "            datetime.datetime.now().isoformat(),\n",
        "            strength,\n",
        "            f\"Commits last week: {commits_last_week}, Stars: {stars}\"\n",
        "        ))\n",
        "        conn.commit()\n",
        "\n",
        "        print(f\"Signal added for {company} | Strength: {strength}\")\n",
        "\n",
        "    except Exception as e:\n",
        "        print(f\"Error for {company}: {e}\")\n",
        "\n",
        "conn.close()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CMfGUcwi2NgV",
        "outputId": "a2280257-6644-493f-cf01-37d41004ab27"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Signal added for openai | Strength: 0.58\n",
            "Signal added for tensorflow | Strength: 0.03\n",
            "Signal added for pytorch | Strength: 1\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "import datetime\n",
        "\n",
        "# 1️⃣ Connect to the database\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "\n",
        "# 2️⃣ Pull all signals\n",
        "df_signals = pd.read_sql_query(\"SELECT * FROM signals\", conn)\n",
        "\n",
        "# 3️⃣ Prepare momentum calculation\n",
        "momentum_data = []\n",
        "\n",
        "for company in df_signals[\"company\"].unique():\n",
        "    company_signals = df_signals[df_signals[\"company\"] == company].sort_values(\"timestamp\")\n",
        "\n",
        "    # Cumulative sum of strengths → trajectory\n",
        "    trajectory = company_signals[\"strength\"].cumsum().tolist()\n",
        "\n",
        "    current_score = trajectory[-1]  # last value\n",
        "    change = trajectory[-1] - trajectory[0] if len(trajectory) > 1 else trajectory[0]\n",
        "\n",
        "    momentum_data.append({\n",
        "        \"company\": company,\n",
        "        \"trajectory\": trajectory,\n",
        "        \"current_score\": current_score,\n",
        "        \"change\": change\n",
        "    })\n",
        "\n",
        "# 4️⃣ Create a DataFrame for momentum\n",
        "df_momentum = pd.DataFrame(momentum_data)\n",
        "conn.close()\n",
        "\n",
        "# 5️⃣ Check the results\n",
        "df_momentum"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 163
        },
        "id": "pNYVgc7Z3qw3",
        "outputId": "518ee8d2-f17b-4060-ed5b-469ba8435af3"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "      company trajectory  current_score  change\n",
              "0      openai     [0.58]           0.58    0.58\n",
              "1  tensorflow     [0.03]           0.03    0.03\n",
              "2     pytorch      [1.0]           1.00    1.00"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-6aaf3d3c-b5b3-4eca-af25-34e501cee0b3\" class=\"colab-df-container\">\n",
              "    <div>\n",
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
              "      <th>company</th>\n",
              "      <th>trajectory</th>\n",
              "      <th>current_score</th>\n",
              "      <th>change</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>openai</td>\n",
              "      <td>[0.58]</td>\n",
              "      <td>0.58</td>\n",
              "      <td>0.58</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>tensorflow</td>\n",
              "      <td>[0.03]</td>\n",
              "      <td>0.03</td>\n",
              "      <td>0.03</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>pytorch</td>\n",
              "      <td>[1.0]</td>\n",
              "      <td>1.00</td>\n",
              "      <td>1.00</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "    <div class=\"colab-df-buttons\">\n",
              "\n",
              "  <div class=\"colab-df-container\">\n",
              "    <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-6aaf3d3c-b5b3-4eca-af25-34e501cee0b3')\"\n",
              "            title=\"Convert this dataframe to an interactive table.\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\">\n",
              "    <path d=\"M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z\"/>\n",
              "  </svg>\n",
              "    </button>\n",
              "\n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    .colab-df-buttons div {\n",
              "      margin-bottom: 4px;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "    <script>\n",
              "      const buttonEl =\n",
              "        document.querySelector('#df-6aaf3d3c-b5b3-4eca-af25-34e501cee0b3 button.colab-df-convert');\n",
              "      buttonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "      async function convertToInteractive(key) {\n",
              "        const element = document.querySelector('#df-6aaf3d3c-b5b3-4eca-af25-34e501cee0b3');\n",
              "        const dataTable =\n",
              "          await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                    [key], {});\n",
              "        if (!dataTable) return;\n",
              "\n",
              "        const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "          '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "          + ' to learn more about interactive tables.';\n",
              "        element.innerHTML = '';\n",
              "        dataTable['output_type'] = 'display_data';\n",
              "        await google.colab.output.renderOutput(dataTable, element);\n",
              "        const docLink = document.createElement('div');\n",
              "        docLink.innerHTML = docLinkHtml;\n",
              "        element.appendChild(docLink);\n",
              "      }\n",
              "    </script>\n",
              "  </div>\n",
              "\n",
              "\n",
              "  <div id=\"id_43cd054f-e964-4e8d-a88d-e1cdc8d291d9\">\n",
              "    <style>\n",
              "      .colab-df-generate {\n",
              "        background-color: #E8F0FE;\n",
              "        border: none;\n",
              "        border-radius: 50%;\n",
              "        cursor: pointer;\n",
              "        display: none;\n",
              "        fill: #1967D2;\n",
              "        height: 32px;\n",
              "        padding: 0 0 0 0;\n",
              "        width: 32px;\n",
              "      }\n",
              "\n",
              "      .colab-df-generate:hover {\n",
              "        background-color: #E2EBFA;\n",
              "        box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "        fill: #174EA6;\n",
              "      }\n",
              "\n",
              "      [theme=dark] .colab-df-generate {\n",
              "        background-color: #3B4455;\n",
              "        fill: #D2E3FC;\n",
              "      }\n",
              "\n",
              "      [theme=dark] .colab-df-generate:hover {\n",
              "        background-color: #434B5C;\n",
              "        box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "        filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "        fill: #FFFFFF;\n",
              "      }\n",
              "    </style>\n",
              "    <button class=\"colab-df-generate\" onclick=\"generateWithVariable('df_momentum')\"\n",
              "            title=\"Generate code using this dataframe.\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M7,19H8.4L18.45,9,17,7.55,7,17.6ZM5,21V16.75L18.45,3.32a2,2,0,0,1,2.83,0l1.4,1.43a1.91,1.91,0,0,1,.58,1.4,1.91,1.91,0,0,1-.58,1.4L9.25,21ZM18.45,9,17,7.55Zm-12,3A5.31,5.31,0,0,0,4.9,8.1,5.31,5.31,0,0,0,1,6.5,5.31,5.31,0,0,0,4.9,4.9,5.31,5.31,0,0,0,6.5,1,5.31,5.31,0,0,0,8.1,4.9,5.31,5.31,0,0,0,12,6.5,5.46,5.46,0,0,0,6.5,12Z\"/>\n",
              "  </svg>\n",
              "    </button>\n",
              "    <script>\n",
              "      (() => {\n",
              "      const buttonEl =\n",
              "        document.querySelector('#id_43cd054f-e964-4e8d-a88d-e1cdc8d291d9 button.colab-df-generate');\n",
              "      buttonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "      buttonEl.onclick = () => {\n",
              "        google.colab.notebook.generateWithVariable('df_momentum');\n",
              "      }\n",
              "      })();\n",
              "    </script>\n",
              "  </div>\n",
              "\n",
              "    </div>\n",
              "  </div>\n"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "dataframe",
              "variable_name": "df_momentum",
              "summary": "{\n  \"name\": \"df_momentum\",\n  \"rows\": 3,\n  \"fields\": [\n    {\n      \"column\": \"company\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 3,\n        \"samples\": [\n          \"openai\",\n          \"tensorflow\",\n          \"pytorch\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"trajectory\",\n      \"properties\": {\n        \"dtype\": \"object\",\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"current_score\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 0.48644972333565295,\n        \"min\": 0.03,\n        \"max\": 1.0,\n        \"num_unique_values\": 3,\n        \"samples\": [\n          0.58,\n          0.03,\n          1.0\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"change\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 0.48644972333565295,\n        \"min\": 0.03,\n        \"max\": 1.0,\n        \"num_unique_values\": 3,\n        \"samples\": [\n          0.58,\n          0.03,\n          1.0\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    }\n  ]\n}"
            }
          },
          "metadata": {},
          "execution_count": 4
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JU92rj2-5eJJ",
        "outputId": "d183e970-3fed-4b06-c086-1e405551538a"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting streamlit\n",
            "  Downloading streamlit-1.55.0-py3-none-any.whl.metadata (9.8 kB)\n",
            "Requirement already satisfied: altair!=5.4.0,!=5.4.1,<7,>=4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.5.0)\n",
            "Requirement already satisfied: blinker<2,>=1.5.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (1.9.0)\n",
            "Requirement already satisfied: cachetools<8,>=5.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.2.6)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (8.3.1)\n",
            "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.12/dist-packages (from streamlit) (3.1.46)\n",
            "Requirement already satisfied: numpy<3,>=1.23 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.0.2)\n",
            "Requirement already satisfied: packaging>=20 in /usr/local/lib/python3.12/dist-packages (from streamlit) (26.0)\n",
            "Requirement already satisfied: pandas<3,>=1.4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.2.2)\n",
            "Requirement already satisfied: pillow<13,>=7.1.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (11.3.0)\n",
            "Collecting pydeck<1,>=0.8.0b4 (from streamlit)\n",
            "  Downloading pydeck-0.9.1-py2.py3-none-any.whl.metadata (4.1 kB)\n",
            "Requirement already satisfied: protobuf<7,>=3.20 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.29.6)\n",
            "Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (18.1.0)\n",
            "Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.32.4)\n",
            "Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (9.1.4)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.5.1)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.10.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (4.15.0)\n",
            "Requirement already satisfied: watchdog<7,>=2.1.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.0.0)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.1.6)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (4.26.0)\n",
            "Requirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2.17.0)\n",
            "Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.12/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.12/dist-packages (from pandas<3,>=1.4.0->streamlit) (2.9.0.post0)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.12/dist-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.12/dist-packages (from pandas<3,>=1.4.0->streamlit) (2025.3)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (3.4.5)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (3.11)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (2026.2.25)\n",
            "Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.12/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.3)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from jinja2->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.0.3)\n",
            "Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (25.4.0)\n",
            "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2025.9.1)\n",
            "Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.37.0)\n",
            "Requirement already satisfied: rpds-py>=0.25.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.30.0)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.17.0)\n",
            "Downloading streamlit-1.55.0-py3-none-any.whl (9.1 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m9.1/9.1 MB\u001b[0m \u001b[31m46.5 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading pydeck-0.9.1-py2.py3-none-any.whl (6.9 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m6.9/6.9 MB\u001b[0m \u001b[31m71.8 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: pydeck, streamlit\n",
            "Successfully installed pydeck-0.9.1 streamlit-1.55.0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import streamlit as st\n",
        "import plotly.graph_objects as go\n",
        "import pandas as pd\n",
        "\n",
        "# -------------------------\n",
        "# Example: df_momentum from previous step\n",
        "# Replace this with your actual momentum calculation DataFrame\n",
        "# df_momentum should have columns: company, trajectory, current_score, change\n",
        "# -------------------------\n",
        "# For testing, you can uncomment below mock:\n",
        "# df_momentum = pd.DataFrame({\n",
        "#     \"company\": [\"openai\", \"tensorflow\", \"pytorch\"],\n",
        "#     \"trajectory\": [[0.2,0.5,0.8],[0.03,0.06,0.1],[0.5,0.8,1]],\n",
        "#     \"current_score\": [0.8, 0.1, 1],\n",
        "#     \"change\": [0.6,0.07,0.5]\n",
        "# })\n",
        "\n",
        "# -------------------------\n",
        "# 1️⃣ Plot the jagged line chart\n",
        "# -------------------------\n",
        "fig = go.Figure()\n",
        "\n",
        "for idx, row in df_momentum.iterrows():\n",
        "    x_values = list(range(len(row[\"trajectory\"])))  # Q1, Q2, Q3, Q4\n",
        "    y_values = row[\"trajectory\"]\n",
        "\n",
        "    fig.add_trace(go.Scatter(\n",
        "        x=x_values,\n",
        "        y=y_values,\n",
        "        mode=\"lines+markers\",\n",
        "        name=row[\"company\"],\n",
        "        line=dict(width=3),\n",
        "        hovertemplate=f\"<b>{row['company']}</b><br>Momentum: %{{y}}<extra></extra>\"\n",
        "    ))\n",
        "\n",
        "fig.update_xaxes(tickvals=[0,1,2,3], ticktext=[\"Q1\",\"Q2\",\"Q3\",\"Q4\"])\n",
        "fig.update_layout(\n",
        "    title=\"Startup Momentum Field\",\n",
        "    height=600,\n",
        "    template=\"plotly_dark\"\n",
        ")\n",
        "\n",
        "st.plotly_chart(fig, use_container_width=True)\n",
        "\n",
        "# -------------------------\n",
        "# 2️⃣ Top Momentum Startups Table\n",
        "# -------------------------\n",
        "st.subheader(\"Top Momentum Startups\")\n",
        "\n",
        "df_top = df_momentum.sort_values(\"current_score\", ascending=False).head(10)\n",
        "st.table(df_top[[\"company\",\"current_score\",\"change\"]])\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KhmFo9-T7OtT",
        "outputId": "8bfdd512-2d2f-487f-de34-c467ce737708"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2026-03-15 00:37:16.056 Please replace `use_container_width` with `width`.\n",
            "\n",
            "`use_container_width` will be removed after 2025-12-31.\n",
            "\n",
            "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.\n",
            "2026-03-15 00:37:16.077 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.079 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.080 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.666 \n",
            "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
            "  command:\n",
            "\n",
            "    streamlit run /usr/local/lib/python3.12/dist-packages/colab_kernel_launcher.py [ARGUMENTS]\n",
            "2026-03-15 00:37:16.667 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.668 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.669 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.670 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.671 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.686 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.754 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.756 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-15 00:37:16.758 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "DeltaGenerator()"
            ]
          },
          "metadata": {},
          "execution_count": 8
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "\n",
        "cursor = conn.cursor()\n",
        "\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS signals (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    company TEXT,\n",
        "    signal_type TEXT,\n",
        "    source TEXT,\n",
        "    timestamp TEXT,\n",
        "    strength REAL,\n",
        "    details TEXT\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "conn.commit()\n",
        "conn.close()\n",
        "\n",
        "print(\"Signals table created successfully\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "7NSOQ2tYGtLl",
        "outputId": "98cfa51c-0a2b-48b1-8aec-fa397d689ac9"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Signals table created successfully\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install requests"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "yrjdOrPXErni",
        "outputId": "1df431b0-4601-4dfa-c69c-0cf64dab3b8a"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: requests in /usr/local/lib/python3.12/dist-packages (2.32.4)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests) (3.4.5)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests) (3.11)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests) (2026.2.25)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python scrapers/github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "vK_dZB5lE1Jw",
        "outputId": "b6b77db4-690e-4a75-967d-34f25b039878"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "python3: can't open file '/content/scrapers/github_scraper.py': [Errno 2] No such file or directory\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install requests\n",
        "!python scrapers/github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "WN6F3YCYGeX0",
        "outputId": "978a39ef-7869-4411-d9d3-35b56ced6405"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: requests in /usr/local/lib/python3.12/dist-packages (2.32.4)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests) (3.4.5)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests) (3.11)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests) (2026.2.25)\n",
            "python3: can't open file '/content/scrapers/github_scraper.py': [Errno 2] No such file or directory\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!ls /content"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "XdCCJwzqITH7",
        "outputId": "efa0ea16-7222-4c5c-f212-de63dfdad26e"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "mip_live.db  sample_data\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!mkdir -p /content/scrapers"
      ],
      "metadata": {
        "id": "86m9iBFfI6mc"
      },
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!ils /content"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "u-ioxu9hJFwm",
        "outputId": "cba448ab-fc4b-4870-a3f3-a529c6a9eeaf"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/bin/bash: line 1: ils: command not found\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!ls /content"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "I8kCvCm_JwIP",
        "outputId": "811070e6-fedf-4c9f-a11f-97a7a9bac7c5"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "mip_live.db  sample_data  scrapers\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!ls /content/scrapers"
      ],
      "metadata": {
        "id": "0TEqM7kjLDTn"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!ls /content/scrapers"
      ],
      "metadata": {
        "id": "WsnS2LnILtjw"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile /content/scrapers/github_scraper.py\n",
        "import requests\n",
        "import sqlite3\n",
        "from datetime import datetime\n",
        "\n",
        "# -------------------------\n",
        "# DATABASE CONNECTION\n",
        "# -------------------------\n",
        "conn = sqlite3.connect(\"/content/mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# -------------------------\n",
        "# FETCH TRENDING REPOS\n",
        "# -------------------------\n",
        "url = \"https://api.github.com/search/repositories?q=stars:%3E500&sort=stars&order=desc\"\n",
        "response = requests.get(url)\n",
        "data = response.json()\n",
        "\n",
        "repos = data.get(\"items\", [])[:10]\n",
        "\n",
        "# -------------------------\n",
        "# INSERT SIGNALS\n",
        "# -------------------------\n",
        "for repo in repos:\n",
        "    company = repo[\"name\"]\n",
        "    signal_type = \"GitHub Spike\"\n",
        "    source = \"GitHub\"\n",
        "    strength = repo[\"stargazers_count\"] / 10000\n",
        "    timestamp = datetime.utcnow().isoformat()\n",
        "    details = repo[\"html_url\"]\n",
        "\n",
        "    cursor.execute(\"\"\"\n",
        "        INSERT INTO signals\n",
        "        (company, signal_type, source, strength, timestamp, details)\n",
        "        VALUES (?, ?, ?, ?, ?, ?)\n",
        "    \"\"\", (company, signal_type, source, strength, timestamp, details))\n",
        "\n",
        "    print(f\"Signal added for {company}\")\n",
        "\n",
        "conn.commit()\n",
        "conn.close()\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KDjLxjfpO4zi",
        "outputId": "0728dbe8-7efc-4e22-911d-7fe0eec3ed0a"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing /content/scrapers/github_scraper.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!ls /content/scrapers"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ofdLm2U5PoWc",
        "outputId": "98485cf8-dd4e-4347-8fe4-39d5d8cea79f"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "ls: cannot access '/content/scrapers': No such file or directory\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install requests\n",
        "!python /content/scrapers/github_scraper.py\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CIw7VkhoQHIS",
        "outputId": "2816d39c-9088-4b97-fe69-3cb75b8d6088"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: requests in /usr/local/lib/python3.12/dist-packages (2.32.4)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests) (3.4.5)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests) (3.11)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests) (2026.2.25)\n",
            "python3: can't open file '/content/scrapers/github_scraper.py': [Errno 2] No such file or directory\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "\n",
        "conn = sqlite3.connect(\"/content/mip_live.db\")\n",
        "df = pd.read_sql_query(\"SELECT * FROM signals ORDER BY timestamp DESC LIMIT 10\", conn)\n",
        "conn.close()\n",
        "\n",
        "df"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 591
        },
        "id": "Tu2GGvrJSSga",
        "outputId": "289c0ab1-c330-4b8c-913b-8be363728401"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "   id                      company   signal_type  source  \\\n",
              "0  13               awesome-python  GitHub Spike  GitHub   \n",
              "1  12                     openclaw  GitHub Spike  GitHub   \n",
              "2  11  coding-interview-university  GitHub Spike  GitHub   \n",
              "3  10         system-design-primer  GitHub Spike  GitHub   \n",
              "4   9            developer-roadmap  GitHub Spike  GitHub   \n",
              "5   8       free-programming-books  GitHub Spike  GitHub   \n",
              "6   7                  public-apis  GitHub Spike  GitHub   \n",
              "7   6                 freeCodeCamp  GitHub Spike  GitHub   \n",
              "8   5                      awesome  GitHub Spike  GitHub   \n",
              "9   4             build-your-own-x  GitHub Spike  GitHub   \n",
              "\n",
              "                    timestamp  strength  \\\n",
              "0  2026-03-15T16:08:33.973966   28.7280   \n",
              "1  2026-03-15T16:08:33.973944   31.4522   \n",
              "2  2026-03-15T16:08:33.973921   33.7854   \n",
              "3  2026-03-15T16:08:33.973899   33.8928   \n",
              "4  2026-03-15T16:08:33.973876   35.0940   \n",
              "5  2026-03-15T16:08:33.973850   38.4040   \n",
              "6  2026-03-15T16:08:33.973825   41.0551   \n",
              "7  2026-03-15T16:08:33.973797   43.8207   \n",
              "8  2026-03-15T16:08:33.973753   44.5692   \n",
              "9  2026-03-15T16:08:33.973260   47.5340   \n",
              "\n",
              "                                             details  momentum_score  \\\n",
              "0            https://github.com/vinta/awesome-python               0   \n",
              "1               https://github.com/openclaw/openclaw               0   \n",
              "2  https://github.com/jwasham/coding-interview-un...               0   \n",
              "3  https://github.com/donnemartin/system-design-p...               0   \n",
              "4  https://github.com/kamranahmedse/developer-roa...               0   \n",
              "5  https://github.com/EbookFoundation/free-progra...               0   \n",
              "6         https://github.com/public-apis/public-apis               0   \n",
              "7       https://github.com/freeCodeCamp/freeCodeCamp               0   \n",
              "8            https://github.com/sindresorhus/awesome               0   \n",
              "9  https://github.com/codecrafters-io/build-your-...               0   \n",
              "\n",
              "   breakout_alert  \n",
              "0               0  \n",
              "1               0  \n",
              "2               0  \n",
              "3               0  \n",
              "4               0  \n",
              "5               0  \n",
              "6               0  \n",
              "7               0  \n",
              "8               0  \n",
              "9               0  "
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-3a745818-2e5c-4f48-8432-ab782e44e62d\" class=\"colab-df-container\">\n",
              "    <div>\n",
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
              "      <th>id</th>\n",
              "      <th>company</th>\n",
              "      <th>signal_type</th>\n",
              "      <th>source</th>\n",
              "      <th>timestamp</th>\n",
              "      <th>strength</th>\n",
              "      <th>details</th>\n",
              "      <th>momentum_score</th>\n",
              "      <th>breakout_alert</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>13</td>\n",
              "      <td>awesome-python</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973966</td>\n",
              "      <td>28.7280</td>\n",
              "      <td>https://github.com/vinta/awesome-python</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>12</td>\n",
              "      <td>openclaw</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973944</td>\n",
              "      <td>31.4522</td>\n",
              "      <td>https://github.com/openclaw/openclaw</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>11</td>\n",
              "      <td>coding-interview-university</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973921</td>\n",
              "      <td>33.7854</td>\n",
              "      <td>https://github.com/jwasham/coding-interview-un...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>10</td>\n",
              "      <td>system-design-primer</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973899</td>\n",
              "      <td>33.8928</td>\n",
              "      <td>https://github.com/donnemartin/system-design-p...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>9</td>\n",
              "      <td>developer-roadmap</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973876</td>\n",
              "      <td>35.0940</td>\n",
              "      <td>https://github.com/kamranahmedse/developer-roa...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>8</td>\n",
              "      <td>free-programming-books</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973850</td>\n",
              "      <td>38.4040</td>\n",
              "      <td>https://github.com/EbookFoundation/free-progra...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>7</td>\n",
              "      <td>public-apis</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973825</td>\n",
              "      <td>41.0551</td>\n",
              "      <td>https://github.com/public-apis/public-apis</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>6</td>\n",
              "      <td>freeCodeCamp</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973797</td>\n",
              "      <td>43.8207</td>\n",
              "      <td>https://github.com/freeCodeCamp/freeCodeCamp</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>5</td>\n",
              "      <td>awesome</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973753</td>\n",
              "      <td>44.5692</td>\n",
              "      <td>https://github.com/sindresorhus/awesome</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>4</td>\n",
              "      <td>build-your-own-x</td>\n",
              "      <td>GitHub Spike</td>\n",
              "      <td>GitHub</td>\n",
              "      <td>2026-03-15T16:08:33.973260</td>\n",
              "      <td>47.5340</td>\n",
              "      <td>https://github.com/codecrafters-io/build-your-...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "    <div class=\"colab-df-buttons\">\n",
              "\n",
              "  <div class=\"colab-df-container\">\n",
              "    <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-3a745818-2e5c-4f48-8432-ab782e44e62d')\"\n",
              "            title=\"Convert this dataframe to an interactive table.\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\">\n",
              "    <path d=\"M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z\"/>\n",
              "  </svg>\n",
              "    </button>\n",
              "\n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    .colab-df-buttons div {\n",
              "      margin-bottom: 4px;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "    <script>\n",
              "      const buttonEl =\n",
              "        document.querySelector('#df-3a745818-2e5c-4f48-8432-ab782e44e62d button.colab-df-convert');\n",
              "      buttonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "      async function convertToInteractive(key) {\n",
              "        const element = document.querySelector('#df-3a745818-2e5c-4f48-8432-ab782e44e62d');\n",
              "        const dataTable =\n",
              "          await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                    [key], {});\n",
              "        if (!dataTable) return;\n",
              "\n",
              "        const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "          '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "          + ' to learn more about interactive tables.';\n",
              "        element.innerHTML = '';\n",
              "        dataTable['output_type'] = 'display_data';\n",
              "        await google.colab.output.renderOutput(dataTable, element);\n",
              "        const docLink = document.createElement('div');\n",
              "        docLink.innerHTML = docLinkHtml;\n",
              "        element.appendChild(docLink);\n",
              "      }\n",
              "    </script>\n",
              "  </div>\n",
              "\n",
              "\n",
              "  <div id=\"id_dcdb35d9-4ee8-492a-8fa2-89a595c218f3\">\n",
              "    <style>\n",
              "      .colab-df-generate {\n",
              "        background-color: #E8F0FE;\n",
              "        border: none;\n",
              "        border-radius: 50%;\n",
              "        cursor: pointer;\n",
              "        display: none;\n",
              "        fill: #1967D2;\n",
              "        height: 32px;\n",
              "        padding: 0 0 0 0;\n",
              "        width: 32px;\n",
              "      }\n",
              "\n",
              "      .colab-df-generate:hover {\n",
              "        background-color: #E2EBFA;\n",
              "        box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "        fill: #174EA6;\n",
              "      }\n",
              "\n",
              "      [theme=dark] .colab-df-generate {\n",
              "        background-color: #3B4455;\n",
              "        fill: #D2E3FC;\n",
              "      }\n",
              "\n",
              "      [theme=dark] .colab-df-generate:hover {\n",
              "        background-color: #434B5C;\n",
              "        box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "        filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "        fill: #FFFFFF;\n",
              "      }\n",
              "    </style>\n",
              "    <button class=\"colab-df-generate\" onclick=\"generateWithVariable('df')\"\n",
              "            title=\"Generate code using this dataframe.\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M7,19H8.4L18.45,9,17,7.55,7,17.6ZM5,21V16.75L18.45,3.32a2,2,0,0,1,2.83,0l1.4,1.43a1.91,1.91,0,0,1,.58,1.4,1.91,1.91,0,0,1-.58,1.4L9.25,21ZM18.45,9,17,7.55Zm-12,3A5.31,5.31,0,0,0,4.9,8.1,5.31,5.31,0,0,0,1,6.5,5.31,5.31,0,0,0,4.9,4.9,5.31,5.31,0,0,0,6.5,1,5.31,5.31,0,0,0,8.1,4.9,5.31,5.31,0,0,0,12,6.5,5.46,5.46,0,0,0,6.5,12Z\"/>\n",
              "  </svg>\n",
              "    </button>\n",
              "    <script>\n",
              "      (() => {\n",
              "      const buttonEl =\n",
              "        document.querySelector('#id_dcdb35d9-4ee8-492a-8fa2-89a595c218f3 button.colab-df-generate');\n",
              "      buttonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "      buttonEl.onclick = () => {\n",
              "        google.colab.notebook.generateWithVariable('df');\n",
              "      }\n",
              "      })();\n",
              "    </script>\n",
              "  </div>\n",
              "\n",
              "    </div>\n",
              "  </div>\n"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "dataframe",
              "variable_name": "df",
              "summary": "{\n  \"name\": \"df\",\n  \"rows\": 10,\n  \"fields\": [\n    {\n      \"column\": \"id\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 3,\n        \"min\": 4,\n        \"max\": 13,\n        \"num_unique_values\": 10,\n        \"samples\": [\n          5,\n          12,\n          8\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"company\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 10,\n        \"samples\": [\n          \"awesome\",\n          \"openclaw\",\n          \"free-programming-books\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"signal_type\",\n      \"properties\": {\n        \"dtype\": \"category\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"GitHub Spike\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"source\",\n      \"properties\": {\n        \"dtype\": \"category\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"GitHub\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"timestamp\",\n      \"properties\": {\n        \"dtype\": \"object\",\n        \"num_unique_values\": 10,\n        \"samples\": [\n          \"2026-03-15T16:08:33.973753\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"strength\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 6.227825602924702,\n        \"min\": 28.728,\n        \"max\": 47.534,\n        \"num_unique_values\": 10,\n        \"samples\": [\n          44.5692\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"details\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 10,\n        \"samples\": [\n          \"https://github.com/sindresorhus/awesome\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"momentum_score\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 0,\n        \"min\": 0,\n        \"max\": 0,\n        \"num_unique_values\": 1,\n        \"samples\": [\n          0\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"breakout_alert\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 0,\n        \"min\": 0,\n        \"max\": 0,\n        \"num_unique_values\": 1,\n        \"samples\": [\n          0\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    }\n  ]\n}"
            }
          },
          "metadata": {},
          "execution_count": 11
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "\n",
        "# Connect to the database\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# Step 1: Add momentum_score column if it doesn't already exist\n",
        "cursor.execute(\"\"\"\n",
        "    ALTER TABLE signals\n",
        "    ADD COLUMN momentum_score INTEGER DEFAULT 0\n",
        "\"\"\")\n",
        "\n",
        "# Optional Step 2: Add breakout_alert column\n",
        "cursor.execute(\"\"\"\n",
        "    ALTER TABLE signals\n",
        "    ADD COLUMN breakout_alert INTEGER DEFAULT 0\n",
        "\"\"\")\n",
        "\n",
        "# Commit changes and close connection\n",
        "conn.commit()\n",
        "conn.close()\n",
        "\n",
        "print(\"✅ Columns added successfully. Layout unaffected.\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KHHaOZKbVfHo",
        "outputId": "f86d29f7-daf8-4b89-f6d0-88e61237cc0b"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "✅ Columns added successfully. Layout unaffected.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "\n",
        "# Connect to database\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "\n",
        "# Pull the first 10 rows to inspect\n",
        "df = pd.read_sql_query(\"SELECT company, momentum_score, breakout_alert FROM signals LIMIT 10\", conn)\n",
        "print(df)\n",
        "\n",
        "conn.close()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "j0GARvaHbGiW",
        "outputId": "5d0fd690-bc4a-4a89-e5ab-13ef66998260"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "                  company  momentum_score  breakout_alert\n",
            "0                  openai               0               0\n",
            "1              tensorflow               0               0\n",
            "2                 pytorch               0               0\n",
            "3        build-your-own-x               0               0\n",
            "4                 awesome               0               0\n",
            "5            freeCodeCamp               0               0\n",
            "6             public-apis               0               0\n",
            "7  free-programming-books               0               0\n",
            "8       developer-roadmap               0               0\n",
            "9    system-design-primer               0               0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python scraper/github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "OuL9EmitnFYn",
        "outputId": "c6c65d27-f098-4c24-e4fa-14f4e953818b"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "python3: can't open file '/content/scraper/github_scraper.py': [Errno 2] No such file or directory\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!ls /content"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "yDv8XuZNZN7W",
        "outputId": "3736c9a1-cc61-4a67-90f4-f01cb07eb408"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "github_scraper.py  mip_live.db\tsample_data\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install python-dateutil"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "M8H3IpMQaQmF",
        "outputId": "d59197d1-bf42-4d92-eb35-1b3e6f40447c"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: python-dateutil in /usr/local/lib/python3.12/dist-packages (2.9.0.post0)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil) (1.17.0)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install python-dateutil"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "vW9FpQVbck1n",
        "outputId": "0e3a8610-b858-4092-a1b9-d76d741d361c"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: python-dateutil in /usr/local/lib/python3.12/dist-packages (2.9.0.post0)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil) (1.17.0)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "FcQbRWt0cyi8",
        "outputId": "cd275640-e60a-418f-cdae-9c1338335d64"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/github_scraper.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "/content/github_scraper.py:39: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])).days\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 39, in <module>\n",
            "    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])).days\n",
            "                            ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
            "TypeError: can't subtract offset-naive and offset-aware datetimes\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3jfT-TfLGdBg",
        "outputId": "5166b7e5-b7eb-4adb-deb4-5ad766bd39a0"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/github_scraper.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 41, in <module>\n",
            "    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "                            ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
            "TypeError: can't subtract offset-naive and offset-aware datetimes\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "QeBt7CGoJLOo",
        "outputId": "53f0f989-f2a0-4018-df60-c73493995487"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/github_scraper.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 41, in <module>\n",
            "    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "                            ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
            "TypeError: can't subtract offset-naive and offset-aware datetimes\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!grep -n \"utcnow\" github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JwNMTdFWLuNv",
        "outputId": "8ca49b08-4704-4523-eabb-c9ac7521380f"
      },
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "33:    timestamp = datetime.utcnow().isoformat()\n",
            "41:    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "NblRB3LeRDjm",
        "outputId": "8151e018-69e2-4854-8978-1c598e9b42c3"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/github_scraper.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 48, in <module>\n",
            "    momentum_score = calculate_momentum_score(\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "NameError: name 'calculate_momentum_score' is not defined\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "id": "Lo-wVHUWXGE5"
      },
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "\n",
        "# Connect to the database\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "\n",
        "# Query top 10 signals with momentum and breakout info\n",
        "df = pd.read_sql_query(\"\"\"\n",
        "    SELECT company, momentum_score, breakout_alert\n",
        "    FROM signals\n",
        "    ORDER BY timestamp DESC\n",
        "    LIMIT 10\n",
        "\"\"\", conn)\n",
        "\n",
        "print(df)\n",
        "\n",
        "conn.close()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 755
        },
        "id": "zXIHx4_xXymK",
        "outputId": "fdd359eb-c714-41f3-e75f-b05d4b3bd15c"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "error",
          "ename": "DatabaseError",
          "evalue": "Execution failed on sql '\n    SELECT company, momentum_score, breakout_alert \n    FROM signals\n    ORDER BY timestamp DESC\n    LIMIT 10\n': no such column: momentum_score",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mOperationalError\u001b[0m                          Traceback (most recent call last)",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mexecute\u001b[0;34m(self, sql, params)\u001b[0m\n\u001b[1;32m   2673\u001b[0m         \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 2674\u001b[0;31m             \u001b[0mcur\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msql\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m*\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   2675\u001b[0m             \u001b[0;32mreturn\u001b[0m \u001b[0mcur\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mOperationalError\u001b[0m: no such column: momentum_score",
            "\nThe above exception was the direct cause of the following exception:\n",
            "\u001b[0;31mDatabaseError\u001b[0m                             Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_636/2040488389.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      6\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0;31m# Query top 10 signals with momentum and breakout info\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 8\u001b[0;31m df = pd.read_sql_query(\"\"\"\n\u001b[0m\u001b[1;32m      9\u001b[0m     \u001b[0mSELECT\u001b[0m \u001b[0mcompany\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mmomentum_score\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbreakout_alert\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     10\u001b[0m     \u001b[0mFROM\u001b[0m \u001b[0msignals\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mread_sql_query\u001b[0;34m(sql, con, index_col, coerce_float, params, parse_dates, chunksize, dtype, dtype_backend)\u001b[0m\n\u001b[1;32m    524\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    525\u001b[0m     \u001b[0;32mwith\u001b[0m \u001b[0mpandasSQL_builder\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcon\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpandas_sql\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 526\u001b[0;31m         return pandas_sql.read_query(\n\u001b[0m\u001b[1;32m    527\u001b[0m             \u001b[0msql\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    528\u001b[0m             \u001b[0mindex_col\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mindex_col\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mread_query\u001b[0;34m(self, sql, index_col, coerce_float, parse_dates, params, chunksize, dtype, dtype_backend)\u001b[0m\n\u001b[1;32m   2736\u001b[0m         \u001b[0mdtype_backend\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mDtypeBackend\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0mLiteral\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"numpy\"\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m\"numpy\"\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2737\u001b[0m     ) -> DataFrame | Iterator[DataFrame]:\n\u001b[0;32m-> 2738\u001b[0;31m         \u001b[0mcursor\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msql\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mparams\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   2739\u001b[0m         \u001b[0mcolumns\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0mcol_desc\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m0\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;32mfor\u001b[0m \u001b[0mcol_desc\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mcursor\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdescription\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2740\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mexecute\u001b[0;34m(self, sql, params)\u001b[0m\n\u001b[1;32m   2684\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2685\u001b[0m             \u001b[0mex\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mDatabaseError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mf\"Execution failed on sql '{sql}': {exc}\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 2686\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mex\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mexc\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   2687\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2688\u001b[0m     \u001b[0;34m@\u001b[0m\u001b[0mstaticmethod\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mDatabaseError\u001b[0m: Execution failed on sql '\n    SELECT company, momentum_score, breakout_alert \n    FROM signals\n    ORDER BY timestamp DESC\n    LIMIT 10\n': no such column: momentum_score"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# Add momentum_score column if it doesn't exist\n",
        "try:\n",
        "    cursor.execute(\"ALTER TABLE signals ADD COLUMN momentum_score INTEGER DEFAULT 0\")\n",
        "except:\n",
        "    pass  # ignore if it already exists\n",
        "\n",
        "# Add breakout_alert column if it doesn't exist\n",
        "try:\n",
        "    cursor.execute(\"ALTER TABLE signals ADD COLUMN breakout_alert INTEGER DEFAULT 0\")\n",
        "except:\n",
        "    pass\n",
        "\n",
        "conn.commit()\n",
        "conn.close()\n",
        "print(\"Columns added (or already exist).\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "SwkOJkCVYp8B",
        "outputId": "935a536e-3111-4eaa-97c0-e1c49b80bb87"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Columns added (or already exist).\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "2f28gqerZyd_",
        "outputId": "33e09d08-aedb-4da3-c751-58ab0b786eb4"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479681 45132\n",
            "/content/github_scraper.py:36: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "/content/github_scraper.py:44: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 44, in <module>\n",
            "    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "                            ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
            "TypeError: can't subtract offset-naive and offset-aware datetimes\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "\n",
        "# Connect to the database\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "\n",
        "# Query top 10 signals with momentum and breakout info\n",
        "df = pd.read_sql_query(\"\"\"\n",
        "    SELECT company, momentum_score, breakout_alert\n",
        "    FROM signals\n",
        "    ORDER BY timestamp DESC\n",
        "    LIMIT 10\n",
        "\"\"\", conn)\n",
        "\n",
        "print(df)\n",
        "\n",
        "conn.close()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 755
        },
        "id": "pHgmrtZQaLpS",
        "outputId": "fa3fd419-cf46-4b4c-cacd-e258d9bfbe20"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "error",
          "ename": "DatabaseError",
          "evalue": "Execution failed on sql '\n    SELECT company, momentum_score, breakout_alert \n    FROM signals\n    ORDER BY timestamp DESC\n    LIMIT 10\n': no such column: momentum_score",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mOperationalError\u001b[0m                          Traceback (most recent call last)",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mexecute\u001b[0;34m(self, sql, params)\u001b[0m\n\u001b[1;32m   2673\u001b[0m         \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 2674\u001b[0;31m             \u001b[0mcur\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msql\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m*\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   2675\u001b[0m             \u001b[0;32mreturn\u001b[0m \u001b[0mcur\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mOperationalError\u001b[0m: no such column: momentum_score",
            "\nThe above exception was the direct cause of the following exception:\n",
            "\u001b[0;31mDatabaseError\u001b[0m                             Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_13702/2040488389.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      6\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0;31m# Query top 10 signals with momentum and breakout info\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 8\u001b[0;31m df = pd.read_sql_query(\"\"\"\n\u001b[0m\u001b[1;32m      9\u001b[0m     \u001b[0mSELECT\u001b[0m \u001b[0mcompany\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mmomentum_score\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbreakout_alert\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     10\u001b[0m     \u001b[0mFROM\u001b[0m \u001b[0msignals\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mread_sql_query\u001b[0;34m(sql, con, index_col, coerce_float, params, parse_dates, chunksize, dtype, dtype_backend)\u001b[0m\n\u001b[1;32m    524\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    525\u001b[0m     \u001b[0;32mwith\u001b[0m \u001b[0mpandasSQL_builder\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcon\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpandas_sql\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 526\u001b[0;31m         return pandas_sql.read_query(\n\u001b[0m\u001b[1;32m    527\u001b[0m             \u001b[0msql\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    528\u001b[0m             \u001b[0mindex_col\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mindex_col\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mread_query\u001b[0;34m(self, sql, index_col, coerce_float, parse_dates, params, chunksize, dtype, dtype_backend)\u001b[0m\n\u001b[1;32m   2736\u001b[0m         \u001b[0mdtype_backend\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mDtypeBackend\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0mLiteral\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"numpy\"\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m\"numpy\"\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2737\u001b[0m     ) -> DataFrame | Iterator[DataFrame]:\n\u001b[0;32m-> 2738\u001b[0;31m         \u001b[0mcursor\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0msql\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mparams\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   2739\u001b[0m         \u001b[0mcolumns\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0mcol_desc\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m0\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;32mfor\u001b[0m \u001b[0mcol_desc\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mcursor\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdescription\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2740\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/sql.py\u001b[0m in \u001b[0;36mexecute\u001b[0;34m(self, sql, params)\u001b[0m\n\u001b[1;32m   2684\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2685\u001b[0m             \u001b[0mex\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mDatabaseError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mf\"Execution failed on sql '{sql}': {exc}\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 2686\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mex\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mexc\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   2687\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   2688\u001b[0m     \u001b[0;34m@\u001b[0m\u001b[0mstaticmethod\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mDatabaseError\u001b[0m: Execution failed on sql '\n    SELECT company, momentum_score, breakout_alert \n    FROM signals\n    ORDER BY timestamp DESC\n    LIMIT 10\n': no such column: momentum_score"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!grep -n \"utcnow\" github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Foyhm6T0AHy-",
        "outputId": "d1292717-377d-43d4-b6b2-fe57ed0007da"
      },
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "36:    timestamp = datetime.utcnow().isoformat()\n",
            "44:    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "86br3rcvB-8D",
        "outputId": "23d5f037-c982-4ad8-b19c-2fc59b1f828d"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479687 45133\n",
            "/content/github_scraper.py:36: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "/content/github_scraper.py:44: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 44, in <module>\n",
            "    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "                            ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
            "TypeError: can't subtract offset-naive and offset-aware datetimes\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!grep -n \"parser.parse\" github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KF4Tpp2BDE31",
        "outputId": "8fdd6b04-cdc2-4b6e-b3d2-07232468ca62"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "44:    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "H_3axW_DE2Q2",
        "outputId": "2c596459-887c-48f6-dd38-4895e36817bc"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479695 45134\n",
            "/content/github_scraper.py:36: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 49, in <module>\n",
            "    momentum_score = calculate_momentum_score(\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "NameError: name 'calculate_momentum_score' is not defined\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "j86KzsfwGYDr",
        "outputId": "6c57fd2f-295e-4337-c1a4-6159b3fdb05f"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479701 45134\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 54, in <module>\n",
            "    momentum_score = calculate_momentum_score(\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_momentum_score() takes 1 positional argument but 6 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JTtFQQF2J5GY",
        "outputId": "6d807627-cc9a-42f2-91d2-d94f1c91bbd7"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479708 45135\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 60, in <module>\n",
            "    \"\"\", (company_name,))\n",
            "          ^^^^^^^^^^^^\n",
            "NameError: name 'company_name' is not defined\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "nA1VCjR-Kr2Q",
        "outputId": "f01cf203-7634-401e-b11c-1fd0bb36098d"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479714 45135\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 55, in <module>\n",
            "    cursor.execute(\"\"\"\n",
            "sqlite3.OperationalError: no such column: momentum_score\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "cursor.execute(\"PRAGMA table_info(signals)\")\n",
        "columns = cursor.fetchall()\n",
        "for col in columns:\n",
        "    print(col)\n",
        "\n",
        "conn.close()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "6uABKXEcMB24",
        "outputId": "20efa7fe-e1c3-4a86-8620-b2ba15331733"
      },
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "(0, 'id', 'INTEGER', 0, None, 1)\n",
            "(1, 'company', 'TEXT', 0, None, 0)\n",
            "(2, 'signal_type', 'TEXT', 0, None, 0)\n",
            "(3, 'source', 'TEXT', 0, None, 0)\n",
            "(4, 'timestamp', 'TEXT', 0, None, 0)\n",
            "(5, 'strength', 'REAL', 0, None, 0)\n",
            "(6, 'details', 'TEXT', 0, None, 0)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# Add momentum_score column\n",
        "cursor.execute(\"ALTER TABLE signals ADD COLUMN momentum_score INTEGER DEFAULT 0\")\n",
        "\n",
        "# Add breakout_alert column\n",
        "cursor.execute(\"ALTER TABLE signals ADD COLUMN breakout_alert INTEGER DEFAULT 0\")\n",
        "\n",
        "conn.commit()\n",
        "conn.close()\n",
        "print(\"Columns momentum_score and breakout_alert added successfully.\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "XQZ3YKtyORFx",
        "outputId": "3d55365f-bd8f-4ecc-8874-c70c7b1c8fe0"
      },
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Columns momentum_score and breakout_alert added successfully.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "jTby0FqbOu0P",
        "outputId": "8547fef6-cc13-4ec8-aab6-5a4fa258f92a"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479720 45135\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 55, in <module>\n",
            "    cursor.execute(\"\"\"\n",
            "sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 16 supplied.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LaHpLCRsSCEf",
        "outputId": "ae6c5256-7400-4829-99a8-9f2ffaf7d0e8"
      },
      "execution_count": 15,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479730 45137\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 55, in <module>\n",
            "    cursor.execute(\"\"\"\n",
            "sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 16 supplied.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bd0wNKoOTpBY",
        "outputId": "36a353d6-8af0-4877-f610-ddcd06537ab7"
      },
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "build-your-own-x 479738 45139\n",
            "/content/github_scraper.py:41: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 55, in <module>\n",
            "    cursor.execute(\"\"\"\n",
            "sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 16 supplied.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "\n",
        "# 2️⃣ Database setup — creates table if it doesn't exist\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS signals (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    company TEXT,\n",
        "    signal_type TEXT,\n",
        "    source TEXT,\n",
        "    strength REAL,\n",
        "    timestamp TEXT,\n",
        "    details TEXT,\n",
        "    momentum_score INTEGER DEFAULT 0,\n",
        "    breakout_alert INTEGER DEFAULT 0\n",
        ")\n",
        "\"\"\")\n",
        "conn.commit()\n",
        "\n",
        "# 3️⃣ Momentum Score function\n",
        "def calculate_momentum_score(repo):\n",
        "    \"\"\"\n",
        "    Returns a simple momentum score based on stars and forks.\n",
        "    Can be refined later with additional signals.\n",
        "    \"\"\"\n",
        "    stars = repo.get(\"stargazers_count\", 0)\n",
        "    forks = repo.get(\"forks_count\", 0)\n",
        "    return stars + forks\n",
        "\n",
        "# 4️⃣ Placeholder Breakout Alert function\n",
        "def calculate_breakout_alert(repo):\n",
        "    # For now, always return 0; refine logic later\n",
        "    return 0\n",
        "\n",
        "# 5️⃣ GitHub scraping logic\n",
        "# Example: fetch trending repos from GitHub API (can be replaced with real query)\n",
        "url = \"https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=10\"\n",
        "response = requests.get(url)\n",
        "data = response.json()\n",
        "repos = data.get(\"items\", [])\n",
        "\n",
        "# 6️⃣ Loop through repos and insert into DB\n",
        "for repo in repos:\n",
        "    company = repo.get(\"name\")\n",
        "    signal_type = \"GitHub Spike\"\n",
        "    source = \"GitHub\"\n",
        "    strength = repo.get(\"stargazers_count\", 0) / 1000  # example\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "    details = repo.get(\"html_url\")\n",
        "\n",
        "    # Compute scores\n",
        "    momentum_score = calculate_momentum_score(repo)\n",
        "    breakout_alert = calculate_breakout_alert(repo)\n",
        "\n",
        "    # Insert into DB (correct 1-tuple)\n",
        "    cursor.execute(\"\"\"\n",
        "        INSERT INTO signals (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert)\n",
        "        VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n",
        "    \"\"\", (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert))\n",
        "\n",
        "conn.commit()\n",
        "conn.close()\n",
        "print(\"GCM — Scraper completed successfully!\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BdiVvnc8ZIJa",
        "outputId": "43d870f1-e6f8-4cf7-e776-9bb0afb44a89"
      },
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "GCM — Scraper completed successfully!\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "df = pd.read_sql_query(\"SELECT company, momentum_score, breakout_alert FROM signals ORDER BY timestamp DESC LIMIT 10\", conn)\n",
        "print(df)\n",
        "conn.close()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "aTfr1dObaWiT",
        "outputId": "4d39a297-151f-4651-a240-762cda6ddec2"
      },
      "execution_count": 18,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "                  company  momentum_score  breakout_alert\n",
            "0             HelloGitHub          157725               0\n",
            "1                  yt-dlp          164053               0\n",
            "2            transformers          190486               0\n",
            "3  stable-diffusion-webui          192002               0\n",
            "4                 AutoGPT          228773               0\n",
            "5                  Python          268990               0\n",
            "6          awesome-python          315066               0\n",
            "7    system-design-primer          394134               0\n",
            "8  free-programming-books          450172               0\n",
            "9             public-apis          456027               0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# angel_scraper_clean.py\n",
        "\n",
        "import sqlite3\n",
        "from datetime import datetime, timezone\n",
        "\n",
        "# 1️⃣ Database setup — connect to existing DB\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# 2️⃣ Placeholder for startup data\n",
        "# In real usage, replace with API calls or scraping logic\n",
        "startups = [\n",
        "    {\"name\": \"StartupA\", \"followers\": 1500, \"funding_rounds\": 2, \"url\": \"https://angel.co/startupA\"},\n",
        "    {\"name\": \"StartupB\", \"followers\": 800, \"funding_rounds\": 1, \"url\": \"https://angel.co/startupB\"},\n",
        "    {\"name\": \"StartupC\", \"followers\": 3000, \"funding_rounds\": 3, \"url\": \"https://angel.co/startupC\"},\n",
        "]\n",
        "\n",
        "# 3️⃣ Momentum score function\n",
        "def calculate_momentum_score(startup):\n",
        "    # Example: followers + 500 * funding_rounds\n",
        "    followers = startup.get(\"followers\", 0)\n",
        "    funding_rounds = startup.get(\"funding_rounds\", 0)\n",
        "    return followers + (500 * funding_rounds)\n",
        "\n",
        "# 4️⃣ Breakout alert placeholder\n",
        "def calculate_breakout_alert(startup):\n",
        "    # Example: mark breakout if momentum_score > 2000\n",
        "    return 1 if calculate_momentum_score(startup) > 2000 else 0\n",
        "\n",
        "# 5️⃣ Insert startups into DB\n",
        "for s in startups:\n",
        "    company = s.get(\"name\")\n",
        "    signal_type = \"AngelList Signal\"\n",
        "    source = \"AngelList\"\n",
        "    strength = s.get(\"followers\", 0) / 1000  # simple scaling\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "    details = s.get(\"url\")\n",
        "\n",
        "    momentum_score = calculate_momentum_score(s)\n",
        "    breakout_alert = calculate_breakout_alert(s)\n",
        "\n",
        "    cursor.execute(\"\"\"\n",
        "        INSERT INTO signals (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert)\n",
        "        VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n",
        "    \"\"\", (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert))\n",
        "\n",
        "conn.commit()\n",
        "conn.close()\n",
        "print(\"GCM — AngelList scraper completed successfully!\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "hhNUmX3Kechz",
        "outputId": "6f675696-5637-4bc2-8d10-aa24fa9c4dca"
      },
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "GCM — AngelList scraper completed successfully!\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "tgF-i5JPpi7W",
        "outputId": "1aef355b-24bc-46d5-fbb6-548afc19ed8f"
      },
      "execution_count": 21,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "GCM — Scraper completed successfully!\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python angel_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "iDDwpi7JpztJ",
        "outputId": "e943aa1a-77ed-4a83-d76b-75ea9ff7aabf"
      },
      "execution_count": 22,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "GCM — AngelList scraper completed successfully!\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "df = pd.read_sql_query(\"\"\"\n",
        "    SELECT company, source, momentum_score, breakout_alert\n",
        "    FROM signals\n",
        "    ORDER BY timestamp DESC\n",
        "    LIMIT 20\n",
        "\"\"\", conn)\n",
        "print(df)\n",
        "conn.close()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "0gSPBfibqZvZ",
        "outputId": "aadad772-33c0-4cc9-c177-031f001f6b01"
      },
      "execution_count": 23,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "                        company     source  momentum_score  breakout_alert\n",
            "0                      StartupC  AngelList            4500               1\n",
            "1                      StartupB  AngelList            1300               0\n",
            "2                      StartupA  AngelList            2500               1\n",
            "3                      StartupC  AngelList            4500               1\n",
            "4                      StartupB  AngelList            1300               0\n",
            "5                      StartupA  AngelList            2500               1\n",
            "6                   HelloGitHub     GitHub          157725               0\n",
            "7                        yt-dlp     GitHub          164053               0\n",
            "8                  transformers     GitHub          190486               0\n",
            "9        stable-diffusion-webui     GitHub          192002               0\n",
            "10                      AutoGPT     GitHub          228773               0\n",
            "11                       Python     GitHub          268990               0\n",
            "12               awesome-python     GitHub          315066               0\n",
            "13         system-design-primer     GitHub          394134               0\n",
            "14       free-programming-books     GitHub          450172               0\n",
            "15                  public-apis     GitHub          456027               0\n",
            "16               awesome-python     GitHub               0               0\n",
            "17                     openclaw     GitHub               0               0\n",
            "18  coding-interview-university     GitHub               0               0\n",
            "19         system-design-primer     GitHub               0               0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile breakout_engine.py\n",
        "# breakout_engine.py\n",
        "\n",
        "def calculate_breakout_alert(repo, source):\n",
        "    if source == \"GitHub\":\n",
        "        stars = repo.get(\"stargazers_count\", 0)\n",
        "        forks = repo.get(\"forks_count\", 0)\n",
        "        recent_activity = repo.get(\"recent_activity_days\", 0)\n",
        "        return 1 if stars > 1000 and recent_activity < 14 else 0\n",
        "    elif source == \"AngelList\":\n",
        "        followers = repo.get(\"followers\", 0)\n",
        "        funding_rounds = repo.get(\"funding_rounds\", 0)\n",
        "        return 1 if followers + 500*funding_rounds > 2000 else 0\n",
        "    else:\n",
        "        return 0"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "FztI9pqn3HTS",
        "outputId": "79f5f51c-5421-4e8d-85d9-5212748060d1"
      },
      "execution_count": 24,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting breakout_engine.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "UiO8wCua6Iwe",
        "outputId": "93e39544-9561-44d5-df70-297df94d05fc"
      },
      "execution_count": 25,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 7, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                                              ^^^^\n",
            "NameError: name 'repo' is not defined. Did you mean: 'repr'?\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "lTHl6iQd57D_",
        "outputId": "3729f744-3fd0-4631-ccda-22adf535c7e4"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 30, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"Github\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "NameError: name 'calculate_breakout_alert' is not defined\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "PmIeN8br7AZZ",
        "outputId": "22fd8027-0e22-44e7-be2f-2d43747276ec"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/github_scraper.py:35: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  timestamp = datetime.utcnow().isoformat()\n",
            "/content/github_scraper.py:43: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
            "  recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 43, in <module>\n",
            "    recent_activity_days = (datetime.utcnow() - parser.parse(repo[\"pushed_at\"])\n",
            "                            ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
            "TypeError: can't subtract offset-naive and offset-aware datetimes\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "UHYUE96qASdL",
        "outputId": "453f22ac-fdff-4654-db60-c7ce051899d6"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 62, in <module>\n",
            "    cursor.execute(\"\"\"\n",
            "sqlite3.OperationalError: table signals has no column named momentum_score\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Xop0MU6KAvis",
        "outputId": "64311ea8-912a-490f-87c8-664aed12abd6"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 63, in <module>\n",
            "    cursor.execute(\"\"\"\n",
            "sqlite3.OperationalError: table signals has no column named momentum_score\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "oWr_cDySBX2C",
        "outputId": "f750ec00-9c85-44da-aed6-2d3446d55c85"
      },
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "  File \"/content/github_scraper.py\", line 51\n",
            "    company = repo.get(\"name\") breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                               ^^^^^^^^^^^^^^\n",
            "SyntaxError: invalid syntax\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "QbNAyhM3BrDj",
        "outputId": "7cffce57-1ea4-4763-871f-2b330a695c3e"
      },
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "  File \"/content/github_scraper.py\", line 51\n",
            "    company = repo.get(\"name\")breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                              ^^^^^^^^^^^^^^\n",
            "SyntaxError: invalid syntax\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KWaC-_s6B6y2",
        "outputId": "a17704d6-d122-47aa-df6b-512a52e75dbe"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 52, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "NJ1POxbqD7bj",
        "outputId": "dfa37c15-faaf-4af8-897a-bea5468a4760"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 52, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "IMJtuKi7Eh9l",
        "outputId": "71865e4f-58d1-44df-c276-45624859ea33"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 52, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"github\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!ls"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "2lwn5LpIEozK",
        "outputId": "7a2ad618-053a-4171-d257-74410312c5b2"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "angel_scraper.py    github_scraper.py  __pycache__\n",
            "breakout_engine.py  mip_live.db        sample_data\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "QZfYoe89Gk9W",
        "outputId": "de991a3b-a7e4-43e7-d8d0-0f9e4695918e"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 52, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "vW1Cbtv8IQya",
        "outputId": "76b957f2-14a6-47ac-e055-8f933b082908"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/breakout_engine.py\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 54, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Cell 1: Verify breakout engine\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "import breakout_engine\n",
        "print(breakout_engine.__file__)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "NBDSTHAmKHbe",
        "outputId": "14fb57b9-a189-4d58-acb1-09c692b08d18"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/breakout_engine.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "buOSHjy0KKtv",
        "outputId": "194d1c1a-d555-46a6-bca8-72035b25e834"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/breakout_engine.py\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 54, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import importlib\n",
        "import breakout_engine\n",
        "importlib.reload(breakout_engine)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CDy8JvZhLI8e",
        "outputId": "d0dfaf6a-a1ea-46f1-85ba-43cae6132dd6"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<module 'breakout_engine' from '/content/breakout_engine.py'>"
            ]
          },
          "metadata": {},
          "execution_count": 4
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from breakout_engine import calculate_breakout_alert\n",
        "\n",
        "# quick test\n",
        "print(calculate_breakout_alert({\"stargazers_count\":1000,\"forks_count\":200,\"recent_activity_days\":5}, \"GitHub\"))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "stHPcxKuLxO7",
        "outputId": "347d5826-2eb3-41c2-98d8-09deb8547817"
      },
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "1\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "5zeQa41ZMqQW",
        "outputId": "a93b0862-5407-4a21-9e2d-bf993462b5c2"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/breakout_engine.py\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 54, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Zj-IyMyXPyrS",
        "outputId": "37fa5af4-4894-408a-89d8-946ec42c171b"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/breakout_engine.py\n",
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 54, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ORSSkIFBQ46f",
        "outputId": "6aeb1997-5171-47ef-e749-f78635ac6dc2"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 53, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Force Colab to reload the breakout engine module\n",
        "import importlib\n",
        "import breakout_engine\n",
        "importlib.reload(breakout_engine)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "SnP_5UI9Rn9m",
        "outputId": "f4a6d77a-aee4-4e86-cab0-bbab4f752ee1"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<module 'breakout_engine' from '/content/breakout_engine.py'>"
            ]
          },
          "metadata": {},
          "execution_count": 9
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!python github_scraper.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "P3BgXoNyR0jI",
        "outputId": "02de3d88-2131-4b6b-8178-faf0414e5b99"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Traceback (most recent call last):\n",
            "  File \"/content/github_scraper.py\", line 53, in <module>\n",
            "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
            "                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "TypeError: calculate_breakout_alert() takes 1 positional argument but 2 were given\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile github_scraper.py\n",
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "W9PTpFaMYTAR",
        "outputId": "ed9c7810-d01b-48ff-dabb-b4d59e24a173"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing github_scraper.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "\n",
        "# 2️⃣ Database connection\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# 3️⃣ Placeholder for repos (replace with actual API call later)\n",
        "repos = [\n",
        "    {\"name\": \"CompanyA\", \"stargazers_count\": 1000, \"forks_count\": 200, \"pushed_at\": \"2026-03-17T12:00:00Z\"},\n",
        "    {\"name\": \"CompanyB\", \"stargazers_count\": 400, \"forks_count\": 50, \"pushed_at\": \"2026-03-15T15:30:00Z\"}\n",
        "]\n",
        "\n",
        "# 4️⃣ Loop through repos\n",
        "for repo in repos:\n",
        "    company = repo.get(\"name\")\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "\n",
        "    # Placeholder for momentum score (to be calculated in next step)\n",
        "    momentum_score = 0\n",
        "\n",
        "    # Call breakout engine\n",
        "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
        "\n",
        "    # Print to test\n",
        "    print(company, momentum_score, breakout_alert)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "O0e64jG1awzw",
        "outputId": "d463e3c2-759d-4608-fc4f-ad5614323e12"
      },
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "CompanyA 0 1\n",
            "CompanyB 0 0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "\n",
        "# 2️⃣ Database connection\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# 3️⃣ Placeholder for repos (replace with actual API call later)\n",
        "repos = [\n",
        "    {\"name\": \"CompanyA\", \"stargazers_count\": 1000, \"forks_count\": 200, \"pushed_at\": \"2026-03-17T12:00:00Z\"},\n",
        "    {\"name\": \"CompanyB\", \"stargazers_count\": 400, \"forks_count\": 50, \"pushed_at\": \"2026-03-15T15:30:00Z\"}\n",
        "]\n",
        "\n",
        "# 4️⃣ Loop through repos\n",
        "for repo in repos:\n",
        "    company = repo.get(\"name\")\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "\n",
        "    # Placeholder for momentum score (to be calculated in next step)\n",
        "    momentum_score = 0\n",
        "\n",
        "    # Call breakout engine\n",
        "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
        "\n",
        "    # Print to test\n",
        "    print(company, momentum_score, breakout_alert)\n",
        "\n",
        "    # Calculate momentum score (replace with actual function if available)\n",
        "# For now, using placeholder\n",
        "def calculate_momentum_score(repo):\n",
        "    stars = repo.get(\"stargazers_count\", 0)\n",
        "    forks = repo.get(\"forks_count\", 0)\n",
        "    return stars * 0.5 + forks * 0.5  # example calculation\n",
        "\n",
        "momentum_score = calculate_momentum_score(repo)\n",
        "\n",
        "# Insert into database\n",
        "cursor.execute(\"\"\"\n",
        "    INSERT INTO mip_live (company, momentum_score, breakout_alert, timestamp)\n",
        "    VALUES (?, ?, ?, ?)\n",
        "\"\"\", (company, momentum_score, breakout_alert, timestamp))\n",
        "\n",
        "# Commit changes\n",
        "conn.commit()\n",
        "\n",
        "# Optional: print inserted values\n",
        "print(f\"Inserted: {company}, {momentum_score}, {breakout_alert}\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 367
        },
        "id": "rgTtYfvTbhH3",
        "outputId": "7b5899d7-0ea7-4fd6-ef0c-16e92e43877f"
      },
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "CompanyA 0 1\n",
            "CompanyB 0 0\n"
          ]
        },
        {
          "output_type": "error",
          "ename": "OperationalError",
          "evalue": "no such table: mip_live",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mOperationalError\u001b[0m                          Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_31290/1453681946.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     40\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     41\u001b[0m \u001b[0;31m# Insert into database\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 42\u001b[0;31m cursor.execute(\"\"\"\n\u001b[0m\u001b[1;32m     43\u001b[0m     \u001b[0mINSERT\u001b[0m \u001b[0mINTO\u001b[0m \u001b[0mmip_live\u001b[0m \u001b[0;34m(\u001b[0m\u001b[0mcompany\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mmomentum_score\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbreakout_alert\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mtimestamp\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     44\u001b[0m     \u001b[0mVALUES\u001b[0m \u001b[0;34m(\u001b[0m\u001b[0;31m?\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;31m \u001b[0m\u001b[0;31m?\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;31m \u001b[0m\u001b[0;31m?\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;31m \u001b[0m\u001b[0;31m?\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mOperationalError\u001b[0m: no such table: mip_live"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "\n",
        "# 2️⃣ Database connection\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "# 2️⃣ Create table if it doesn't exist\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS mip_live (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    company TEXT,\n",
        "    momentum_score REAL,\n",
        "    breakout_alert INTEGER,\n",
        "    timestamp TEXT\n",
        ")\n",
        "\"\"\")\n",
        "conn.commit()\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# 3️⃣ Placeholder for repos (replace with actual API call later)\n",
        "repos = [\n",
        "    {\"name\": \"CompanyA\", \"stargazers_count\": 1000, \"forks_count\": 200, \"pushed_at\": \"2026-03-17T12:00:00Z\"},\n",
        "    {\"name\": \"CompanyB\", \"stargazers_count\": 400, \"forks_count\": 50, \"pushed_at\": \"2026-03-15T15:30:00Z\"}\n",
        "]\n",
        "\n",
        "# 4️⃣ Loop through repos\n",
        "for repo in repos:\n",
        "    company = repo.get(\"name\")\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "\n",
        "    # Placeholder for momentum score (to be calculated in next step)\n",
        "    momentum_score = 0\n",
        "\n",
        "    # Call breakout engine\n",
        "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
        "\n",
        "    # Print to test\n",
        "    print(company, momentum_score, breakout_alert)\n",
        "\n",
        "    # Calculate momentum score (replace with actual function if available)\n",
        "# For now, using placeholder\n",
        "def calculate_momentum_score(repo):\n",
        "    stars = repo.get(\"stargazers_count\", 0)\n",
        "    forks = repo.get(\"forks_count\", 0)\n",
        "    return stars * 0.5 + forks * 0.5  # example calculation\n",
        "\n",
        "momentum_score = calculate_momentum_score(repo)\n",
        "\n",
        "# Insert into database\n",
        "cursor.execute(\"\"\"\n",
        "    INSERT INTO mip_live (company, momentum_score, breakout_alert, timestamp)\n",
        "    VALUES (?, ?, ?, ?)\n",
        "\"\"\", (company, momentum_score, breakout_alert, timestamp))\n",
        "\n",
        "# Commit changes\n",
        "conn.commit()\n",
        "\n",
        "# Optional: print inserted values\n",
        "print(f\"Inserted: {company}, {momentum_score}, {breakout_alert}\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4f6Tg8oLdO0y",
        "outputId": "3c06cc27-a3d5-4ba9-a05c-19508e90c7d6"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "CompanyA 0 1\n",
            "CompanyB 0 0\n",
            "Inserted: CompanyB, 225.0, 0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Imports for scrapers\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert"
      ],
      "metadata": {
        "id": "VxoGxNd9gwtE"
      },
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile angel_scraper.py\n",
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KlbeETzvhhpI",
        "outputId": "76887210-8b63-4a2d-8005-95780c2cbda8"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing angel_scraper.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "\n",
        "# 2️⃣ Database connection\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# 2️⃣ Create table if it doesn't exist\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS mip_live (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    company TEXT,\n",
        "    momentum_score REAL,\n",
        "    breakout_alert INTEGER,\n",
        "    timestamp TEXT\n",
        ")\n",
        "\"\"\")\n",
        "conn.commit()\n",
        "\n",
        "# 3️⃣ Placeholder AngelList companies (replace with actual API later)\n",
        "companies = [\n",
        "    {\"name\": \"AngelCoA\", \"stargazers_count\": 800, \"forks_count\": 150, \"pushed_at\": \"2026-03-16T10:00:00Z\"},\n",
        "    {\"name\": \"AngelCoB\", \"stargazers_count\": 300, \"forks_count\": 40, \"pushed_at\": \"2026-03-15T08:30:00Z\"}\n",
        "]\n",
        "\n",
        "# 4️⃣ Loop through companies\n",
        "for company in companies:\n",
        "    name = company.get(\"name\")\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "\n",
        "    # Placeholder momentum score\n",
        "    momentum_score = 0\n",
        "\n",
        "    # Call breakout engine\n",
        "    breakout_alert = calculate_breakout_alert(company, \"AngelList\")\n",
        "\n",
        "    # Print to test\n",
        "    print(name, momentum_score, breakout_alert)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "hEYR-95oitWR",
        "outputId": "ead55028-d632-42e7-9fa7-184bef5ab019"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "AngelCoA 0 1\n",
            "AngelCoB 0 0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 1️⃣ Imports\n",
        "import requests\n",
        "from datetime import datetime, timezone\n",
        "import sqlite3\n",
        "from dateutil import parser\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "\n",
        "# 2️⃣ Database connection\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# 2️⃣ Create table if it doesn't exist\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS mip_live (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    company TEXT,\n",
        "    momentum_score REAL,\n",
        "    breakout_alert INTEGER,\n",
        "    timestamp TEXT\n",
        ")\n",
        "\"\"\")\n",
        "conn.commit()\n",
        "\n",
        "# 3️⃣ Placeholder AngelList companies (replace with actual API later)\n",
        "companies = [\n",
        "    {\"name\": \"AngelCoA\", \"stargazers_count\": 800, \"forks_count\": 150, \"pushed_at\": \"2026-03-16T10:00:00Z\"},\n",
        "    {\"name\": \"AngelCoB\", \"stargazers_count\": 300, \"forks_count\": 40, \"pushed_at\": \"2026-03-15T08:30:00Z\"}\n",
        "]\n",
        "\n",
        "# 4️⃣ Loop through companies\n",
        "for company in companies:\n",
        "    name = company.get(\"name\")\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "\n",
        "    # Placeholder momentum score\n",
        "    momentum_score = 0\n",
        "\n",
        "    # Call breakout engine\n",
        "    breakout_alert = calculate_breakout_alert(company, \"AngelList\")\n",
        "\n",
        "    # Print to test\n",
        "    print(name, momentum_score, breakout_alert)\n",
        "    # Calculate momentum score (replace with actual function if available)\n",
        "def calculate_momentum_score(company):\n",
        "    stars = company.get(\"stargazers_count\", 0)\n",
        "    forks = company.get(\"forks_count\", 0)\n",
        "    return stars * 0.5 + forks * 0.5  # example calculation\n",
        "\n",
        "momentum_score = calculate_momentum_score(company)\n",
        "\n",
        "# Insert into database\n",
        "cursor.execute(\"\"\"\n",
        "    INSERT INTO mip_live (company, momentum_score, breakout_alert, timestamp)\n",
        "    VALUES (?, ?, ?, ?)\n",
        "\"\"\", (name, momentum_score, breakout_alert, timestamp))\n",
        "\n",
        "# Commit changes\n",
        "conn.commit()\n",
        "\n",
        "# Optional: print inserted values\n",
        "print(f\"Inserted: {name}, {momentum_score}, {breakout_alert}\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "s3YJ8DYejmm0",
        "outputId": "bb226253-90af-42bf-9b6d-69700e9b0524"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "AngelCoA 0 1\n",
            "AngelCoB 0 0\n",
            "Inserted: AngelCoB, 170.0, 0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import importlib\n",
        "import breakout_engine\n",
        "importlib.reload(breakout_engine)\n",
        "\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "\n",
        "# Quick test for both sources\n",
        "print(calculate_breakout_alert({\"stargazers_count\":1000,\"forks_count\":200}, \"GitHub\"))   # Should print 1\n",
        "print(calculate_breakout_alert({\"followers_count\":600,\"jobs_count\":15}, \"AngelList\"))    # Should print 1"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "VFzRp7KRl0v1",
        "outputId": "52a6afbb-f6ca-47b3-c13a-c5ebcd90ec91"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "1\n",
            "1\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile breakout_engine.py\n",
        "def calculate_breakout_alert(entity, source):\n",
        "    try:\n",
        "        if source == \"GitHub\":\n",
        "            stars = entity.get(\"stargazers_count\", 0)\n",
        "            forks = entity.get(\"forks_count\", 0)\n",
        "            return 1 if stars > 500 and forks > 100 else 0\n",
        "\n",
        "        elif source == \"AngelList\":\n",
        "            followers = entity.get(\"followers_count\", 0)\n",
        "            jobs_posted = entity.get(\"jobs_count\", 0)\n",
        "            return 1 if followers > 500 and jobs_posted > 10 else 0\n",
        "\n",
        "        else:\n",
        "            return 0\n",
        "\n",
        "    except Exception as e:\n",
        "        print(f\"Breakout engine error ({source}): {e}\")\n",
        "        return 0"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "kdmUH__YrGy9",
        "outputId": "7e36d456-ee6a-49ca-bab7-a72faa75fd49"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting breakout_engine.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import importlib\n",
        "import breakout_engine\n",
        "importlib.reload(breakout_engine)\n",
        "from breakout_engine import calculate_breakout_alert"
      ],
      "metadata": {
        "id": "ApVqP61gsrcE"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "print(calculate_breakout_alert({\"stargazers_count\":1000,\"forks_count\":200}, \"GitHub\"))   # Should print 1\n",
        "print(calculate_breakout_alert({\"followers_count\":600,\"jobs_count\":15}, \"AngelList\"))    # Should print 1"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Xvvm3J72s7Ha",
        "outputId": "7356bd41-94e3-422a-9e45-10fd8a3df74b"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "1\n",
            "1\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "from breakout_engine import calculate_breakout_alert\n",
        "from datetime import datetime, timezone\n",
        "\n",
        "# Connect to the database\n",
        "conn = sqlite3.connect(\"mip_live.db\")\n",
        "cursor = conn.cursor()\n",
        "\n",
        "# Create table if not exists\n",
        "cursor.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS mip_live (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    company TEXT,\n",
        "    momentum_score REAL,\n",
        "    breakout_alert INTEGER,\n",
        "    timestamp TEXT\n",
        ")\n",
        "\"\"\")\n",
        "conn.commit()\n",
        "\n",
        "# Sample GitHub repos\n",
        "github_repos = [\n",
        "    {\"name\": \"GitHubCo1\", \"stargazers_count\": 1000, \"forks_count\": 200, \"pushed_at\": \"2026-03-17T12:00:00Z\"},\n",
        "    {\"name\": \"GitHubCo2\", \"stargazers_count\": 400, \"forks_count\": 50, \"pushed_at\": \"2026-03-15T15:30:00Z\"}\n",
        "]\n",
        "\n",
        "# Sample AngelList companies\n",
        "angel_companies = [\n",
        "    {\"name\": \"AngelCo1\", \"followers_count\": 600, \"jobs_count\": 15, \"pushed_at\": \"2026-03-16T10:00:00Z\"},\n",
        "    {\"name\": \"AngelCo2\", \"followers_count\": 300, \"jobs_count\": 5, \"pushed_at\": \"2026-03-15T08:30:00Z\"}\n",
        "]\n",
        "\n",
        "def calculate_momentum_score(entity, source):\n",
        "    if source == \"GitHub\":\n",
        "        return entity.get(\"stargazers_count\", 0)*0.5 + entity.get(\"forks_count\",0)*0.5\n",
        "    elif source == \"AngelList\":\n",
        "        return entity.get(\"followers_count\",0)*0.5 + entity.get(\"jobs_count\",0)*0.5\n",
        "    else:\n",
        "        return 0\n",
        "\n",
        "# Insert GitHub test data\n",
        "for repo in github_repos:\n",
        "    name = repo[\"name\"]\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "    momentum_score = calculate_momentum_score(repo, \"GitHub\")\n",
        "    breakout_alert = calculate_breakout_alert(repo, \"GitHub\")\n",
        "    cursor.execute(\"INSERT INTO mip_live (company, momentum_score, breakout_alert, timestamp) VALUES (?, ?, ?, ?)\",\n",
        "                   (name, momentum_score, breakout_alert, timestamp))\n",
        "    print(f\"GitHub inserted: {name}, {momentum_score}, {breakout_alert}\")\n",
        "\n",
        "# Insert AngelList test data\n",
        "for company in angel_companies:\n",
        "    name = company[\"name\"]\n",
        "    timestamp = datetime.now(timezone.utc).isoformat()\n",
        "    momentum_score = calculate_momentum_score(company, \"AngelList\")\n",
        "    breakout_alert = calculate_breakout_alert(company, \"AngelList\")\n",
        "    cursor.execute(\"INSERT INTO mip_live (company, momentum_score, breakout_alert, timestamp) VALUES (?, ?, ?, ?)\",\n",
        "                   (name, momentum_score, breakout_alert, timestamp))\n",
        "    print(f\"AngelList inserted: {name}, {momentum_score}, {breakout_alert}\")\n",
        "\n",
        "conn.commit()\n",
        "conn.close()\n",
        "print(\"Integration test complete ✅\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Hh0PRPNavwrT",
        "outputId": "6aed7301-329e-4d85-9147-b46a931d6647"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "GitHub inserted: GitHubCo1, 600.0, 1\n",
            "GitHub inserted: GitHubCo2, 225.0, 0\n",
            "AngelList inserted: AngelCo1, 307.5, 1\n",
            "AngelList inserted: AngelCo2, 152.5, 0\n",
            "Integration test complete ✅\n"
          ]
        }
      ]
    }
  ]
}