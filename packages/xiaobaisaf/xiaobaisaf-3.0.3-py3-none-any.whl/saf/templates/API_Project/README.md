## 接口自动化项目


## 目录结构
```text
--------project
| 
|----api_project
|   |
|   |----apis（接口封装）
|   |   |
|   |   |----Client.py
|   |
|   |----case_scripts（测试用例脚本）
|   |   |
|   |   |----test_*.py
|   |   |----test_*.py
|   |
|   |----case_data_files（测试用例数据）
|   |   |
|   |   |----*_CASE_DATA.csv
|   |
|   |----common（公共方法）
|   |   |
|   |   |----ENV.py
|   |   |----csvUtils.py
|   |   |----jsonUtils.py
|   |   |----yamlUtils.py
|   |   |----emailService.py
|   |
|   |----config（配置数据）
|   |   |
|   |   |----case_config.py（测试用例配置文件）
|   |   |----config.py
|   |   |----email_config.py（邮件配置文件）
|   |   |----host_config.py（主机域名配置文件）
|   |   |----log_config.py（日志配置文件）
|   |
|   |----data（测试数据）
|   |   |
|   |   |----*
|   |   
|   |----db（数据库文件）
|   |   |
|   |   |----*
|   |
|   |----log（日志文件）
|   |   |
|   |   |----*.log
|   |
|   |----report（pytest测试报告）
|   |   |
|   |   |----（默认为空，执行前清空文件等内容）
|   |
|   |----allure_report（allure测试报告）
|   |   |
|   |   |----index.html
|   |   |----*
|   |
|----run_main.py
```
----
## 使用建议
Python>=3.9.*

-----

## 使用模板步骤

- 1、环境准备
  - 1.1 命令行，创建并激活虚拟环境 ，防止环境污染（库版本的错乱）
  ```cmd
  cd API_Project
  python -m venv venv
  venv\Scripts\activate       备注：Windows系统命令
  或者
  . venv/bin/activate         备注：非Windows系统命令
  ```
  - 1.2 安装依赖库
  ```cmd
  pip install -r requirements.txt 
  ```
  - 1.3 Allure
  
  [allure-commandline](https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/ "Allure下载地址") 
  下载完，解压，Allure的bin路径添加到环境变量Path中即可

- 2、一键生成/手动编写（代码）
  - 2.1 一键生成代码（一键将curl命令转为python代码）
  ```cmd
  convert_ui.bat
  或者
  convert_ui.sh
  或者
  python convert_ui.py
  ```
  - 2.2 手动编写代码（模仿一键生成方法即可，测试用例脚本、测试用例数据文件、用例配置文件）
- 3、执行
  - 3.1 HOST的赋值（需要指定HOST，不然默认会报错）HOST的值为所有接口Url的前缀部分（都一样的部分）
  ```cmd
  方式一：修改host_config.py中的TEST_HOST的值即可
  方式二：修改run_apis.py中HOST.CURRENT_HOST的值即可  
  ```