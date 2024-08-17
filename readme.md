# 项目名称：自动注册网站账号

## 安装

安装所需的依赖库，可以使用以下命令：

\`\`\`shell
pip install requests
pip install pandas
pip install selenium
pip install bs5
\`\`\`

下载 Chrome 浏览器对应版本的 ChromeDriver，并将其路径更新到代码中的 `chrome_driver_path` 变量。

## 运行代码文件

运行代码文件 `批量注册网站.py`。

ChromeDriver下载方法：[https://www.toutiao.com/article/7252388157394518586/](https://www.toutiao.com/article/7252388157394518586/)

## 使用示例

略

## 特性
`
- 自动注册ASF网站账号
- 有规律生成用户名和邮箱，并使用共同的密码
- 将注册的用户名、密码及邮箱保存到CSV文件
- 在注册界面需人工验证
- 用户名格式为 用户名称+序号(5位)
- 邮箱使用snapmail.cc进行注册
- 邮箱名格式为 邮箱前缀+序号+snapmail.cc
- 用户名，密码及邮箱的更改在setting.py中进行

## 测试

要运行项目的测试，请执行以下步骤：

1. 确保已经按照上述步骤设置了开发环境。
2. 执行项目代码文件 `batch_register.py`。

## 作者

本项目由 jiangk77 编写和维护。

## 授权许可

本项目基于 许可证名称 进行许可。请查阅许可证文件以获取更多信息。

请注意，此处的许可证链接应替换为适用于你的项目的实际许可证链接。

如有其他问题或疑问，请随时联系我。谢谢！
