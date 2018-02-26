# Script
some useful Script

## Dr.com Logib Script

>  Dr.com 登录脚本（适用于SZU）

- 只在Linux环境中测试过。

- 由于编码问题只适用于python3

- 使用方法：

  ```shell
  usage: drcom.py [-h] [--daemon] --username USERNAME --passwd PASSWORD
                  [--gap GAP]

  a script for login dr.com in SZU

  optional arguments:
    -h, --help            show this help message and exit
    --daemon, -d          whether become daemon
    --username USERNAME, -u USERNAME
                          username
    --passwd PASSWORD, -p PASSWORD
                          password
    --gap GAP, -g GAP     check gap(second)
  ```

  注意事项：

  1. `gap <= 0`时，表示不循环执行，只进行一次登录，例如`./drcom.py -u USERNAME -p PASSWD -g 0`
  2. `-d` 选项设置后，会使得程序变成守护进程，这时会生成一个`kill_daemon.sh` 脚本来kill掉守护进程。

  ​

  ​

