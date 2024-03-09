# 💎 Etimo Diamonds Greedy Bot

Bot untuk permainan Etimo Diamonds yang menggunakan strategi greedy. Greedy yang di implementasikan ada 2 yaitu greedy by closest distance dan greedy by biggest point / distance. Sangat disarankan untuk menggunakan point / distance dikarenakan lebih efisien dan bisa mendapatkan lebih banyak poin dibandingkan greedy by distance.

## Installing Dependencies 🔨

1. Clone this repository and move to the root of this project's directory

    ```
    git clone https://github.com/Rapa285/Tubes1_gatau_hehe
    cd ./Tubes1_gatau_hehe
    ```

2. Install dependencies

    ```
    pip install -r requirements.txt
    ```

## How to Run 💻

1. To run one bot

    ```
    python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```

2. To run multiple bots simultaneously

    For Windows

    ```
    ./run-bots.bat
    ```

    For Linux / (possibly) macOS

    ```
    ./run-bots.sh
    ```

    <b>Before executing the script, make sure to change the permission of the shell script to enable executing the script (for linux/macOS)</b>

    ```
    chmod +x run-bots.sh
    ```

#### Note:

-   If you run multiple bots, make sure each emails and names are unique
-   The email could be anything as long as it follows a correct email syntax
-   The name, and password could be anything without any space

## Credits 🪙

This repository is adapted from https://github.com/Etimo/diamonds2

Some code in this repository is adjusted to fix some issues in the original repository and to adapt to the requirements of Algorithm Strategies course (IF2211), Informatics Undergraduate Program, ITB.

©️ All rights and credits reserved to [Etimo](https://github.com/Etimo)

## Contributor

- [Muhammad Dzaki Arta (13522149)](https://github.com/TuanOnta)
- [Muhammad Fauzan Azhim (13522153)](https://github.com/fauzanazz)
- [Pradipta Rafa Mahesa (13522162)](https://github.com/Rapa285)