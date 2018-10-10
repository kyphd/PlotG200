# PlotG200

You can get various plots of "Nanoindenter G200" data, immediately.

![PlotG200](https://github.com/kyphd/PlotG200/blob/master/images/plotg200.png)

## Table of Contents

* [What is PlotG200?](#what-is-plotg200)
* [Requirements](#requirements)
* [Quick Start](#quick-start)
* [How to Use](#how-to-use)
* [Contributing](#contributing)
* [Authors](#authors)
* [License](#license)

## What is PlotG200?

PlotG200 is a python program to generate some plots of data of "Nanoindenter G200". You can generate the following plots immediately.

* load - depth
* harmonic - depth (harmonic contact stiffness)
* hardness - depth
* modulus - depth
* H^2 - 1/h (Nix-Gao)

As for Nix-Gao plot, see https://www.sciencedirect.com/science/article/pii/S0022509697000860?via%3Dihub  
You can generate fitting curves and can find H0 (the hardness in the limit of infinite depth) easily.

## Requirements

PlotG200 requires python 3.7 (I didn't check older versions.) 

Python 3 is available at [https://www.python.org/downloads/](https://www.python.org/downloads/)

PlotG200 requires the following modules.

* numpy
* matplotlib
* pandas
* xlrd

## Quick Start

### 0. install python 3.7 and modules

**If you already installed python and the modules, skip this.**

1. Get python 3.7 at [https://www.python.org/downloads/](https://www.python.org/downloads/) and install.

1. Check installation.

    ~~~
    $ python -V
    Python 3.7.0
    ~~~
    
1. Install modules.

    ~~~
    $ pip install numpy
    $ pip install matplotlib
    $ pip install pandas
    $ pip install xlrd 
    ~~~
    
    If you failed to install the modules, upgrade pip and setuptools and try again.
    
    ~~~
    $ pip install --upgrade pip setuptools
    ~~~
    

### 1. git clone or Download zip 

~~~
$ git clone https://github.com/kyphd/PlotG200.git
~~~

or download [zip](https://github.com/kyphd/plotg200/archive/master.zip) and unzip.

### 2. move to the PlotG200 dir and run PlotG200

~~~
$ cd PlotG200
$ python plotg200.py
~~~

That's it! You can find the PlotG200 window.

## How to Use

1. Open Excel file of G200 with "open file" button.
1. Choose plot type in "plot type" form:
    * load - depth
    * harmonic - depth (harmonic contact stiffness)
    * hardness - depth
    * modulus - depth
    * H^2 - 1/h (Nix-Gao)
1. Select "Test" in Plot Test List. Tick the Test No. you want to plot.
1. Set parameters: xrange, yrange, color, alpha, line plot, and legend.  
For Nix-Gao plot, you can plot fitting curve if "show fitting curve" is ticked.
1. For Nix-Gao plot, you can change xrange (min_x and max_x) parameter for fitting curve in "Fitting Parameter for Nix-Gao Plot" form. Press "Enter" key to update the values.
1. You can save images with "Save Figure" button.
1. You can save csv file of fitting parameters for Nix-Gao plot with "Save CSV" button.

## Contributing

1. Fork this
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

## Authors

* **K. Yabuuchi** 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
