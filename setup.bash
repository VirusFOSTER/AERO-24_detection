apt install software-properties-common

apt update && sudo apt install curl -y

curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu bookworm main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

apt update && sudo apt install -y \
  python3-flake8-blind-except \
  python3-flake8-class-newline \
  python3-flake8-deprecated \
  python3-mypy \
  python3-pip \
  python3-pytest \
  python3-pytest-cov \
  python3-pytest-mock \
  python3-pytest-repeat \
  python3-pytest-rerunfailures \
  python3-pytest-runner \
  python3-pytest-timeout \
  ros-dev-tools \
  python3-vcstools
  
mkdir -p ~/ros2/src
cd ~/ros2_jazzy

vcs import --input https://raw.githubusercontent.com/ros2/ros2/jazzy/ros2.repos src

apt update && apt upgrade

rosdep init
rosdep update

rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers"

cd ~/ros2/
colcon build --symlink-install --continue-on-error
