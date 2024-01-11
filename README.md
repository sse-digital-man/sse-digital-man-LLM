# API key的设置
在`system.example.conf`文件中填写API key，并将文件名改为`system.conf`

# 运行方式
在项目**根目录**下用cmd运行`python main.py`即可。可以自动进行初始化（创建collection和embeddings）
## 输入方式
### 文本输入
1. 输入`in + 问题`进行提问，如`in 连州菜心好吃吗？`
输入`exit`退出程序
### 麦克风输入
1. 输入`mic`进入麦克风输入模式
2. 分别输入`start`和`stop`以开始、结束录音

### 退出程序
输入`exit`退出程序

## utils文件夹中函数的使用
`reload_database.py`: 重新创建collection和embeddings
