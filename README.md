# Strava Dashboard

## Overview

The **Strava Dashboard** is a web application that leverages the Strava API to visualize activity metrics. Built with Plotly Dash and Apache Airflow, this project provides insights into your running activities, including metrics like distance, time, elevation gain, and heart rate zones.

## Features

- **Interactive Dashboard:** Displays graphs for running distance and time with Year-to-Date (YTD) progression.
- **Geographical Heat Map:** Visualizes running locations on a map.
- **Additional Visualizations:** Includes bar charts for elevation gain and pie charts for heart rate zones.
- **Scheduled Data Fetching:** Uses Apache Airflow to periodically fetch and update data from the Strava API.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Safety and Publishing](#safety-and-publishing)

## Installation

### Prerequisites

- **Python 3.x**: Ensure Python 3 is installed.
- **WSL**: Windows Subsystem for Linux if running on Windows.

### Clone the Repository

```bash
git clone https://github.com/chrismatthews939/strava_dashboard.git
