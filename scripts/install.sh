python -m ensurepip --upgrade
pip install pyqtgraph


sudo apt-get install build-essential cmake libusb-1.0-0-dev pkg-config libfftw3-dev
pip install sympy
wget https://github.com/greatscottgadgets/hackrf/releases/download/v2021.03.1/hackrf-2021.03.1.tar.xz
tar -xvf hackrf-2021.03.1.tar.xz
cd hackrf-2021.03.1
mkdir host/build
cd host/build
cmake ..
make
sudo make install
sudo ldconfig
hackrf_info
