# YihanResultSaver Library

当我们做数值计算时，会面临代码修改次数多，数值结果保存得太多，最后分不清哪个是哪个的问题，不要担心，在你的main函数前加上`YihanResultSaver`修饰器，他会自动帮你用`numpy.save`保存计算结果、源代码和日志，方便后面查阅

---

## 特性

- **运行日志记录**：自动记录函数运行的时间、参数和描述信息。
- **返回值保存**：将函数的返回值保存为 `.npy` 文件，便于后续加载和分析。
- **代码备份**：将目标函数的源代码及其依赖的非公共模块的文件保存到指定目录。
- **输出日志重定向**：将函数的标准输出保存到文件，同时保留在终端输出。

---

## 安装

你可以直接将项目克隆到本地使用：

```bash
git clone https://github.com/YihanYu115/YihanResultSaver.git
cd YihanResultSaver
```

并将库添加到你的项目中。

```bash
pip install dist\YihanResultSaver-0.1.0-py3-none-any.whl
```
或者直接
```bash
pip install YihanResultSaver
```

## 使用方法 

### 示例代码 


```python
import numpy as np
from YihanResultSaver import YihanResultSaver

# 为函数添加装饰器
@YihanResultSaver(description="This is a sample function for demo purposes.")
def sample_function(x, y):
    print("This is a sample function.")
    return np.array([x + y, x - y, x * y])

# 调用函数
result = sample_function(10, 5)
print("Function Result:", result)
```

### 执行后的结果 

执行上面的代码后，将生成以下文件和目录结构：


```bash
Results/
├── run_log.txt  # 日志文件，记录函数的运行时间、参数等
├── sample_function_20240101_123456/
│   ├── source_code/
│   │   ├── sample_function.py  # 函数及依赖模块的源代码
│   ├── result.npy  # 函数返回值
│   ├── stdout.txt  # 函数的标准输出日志
```
 
- `run_log.txt`：记录每次函数运行的信息，包括时间、函数名、参数和描述。
 
- `source_code/`：包含目标函数及其所有依赖模块的备份代码。
 
- `result.npy`：函数返回值保存为 `.npy` 文件。
 
- `stdout.txt`：标准输出日志文件。

效果截图
![alt text](image.png)


---


## 函数装饰器参数 
`@YihanResultSaver(description="Your description here")` 
- `description`：用于描述目标函数，记录在日志中，方便追溯。


---


## API 文档 
`YihanResultSaver(description)`
#### 参数 
 
- `description` *(str)*: 对目标函数的描述信息。

#### 功能 

- 自动创建运行日志。

- 保存目标函数的返回值到文件。

- 保存目标函数和依赖模块的源代码。

- 捕获目标函数的标准输出。


---


## 系统需求 
 
- **Python 版本** ：>= 3.6
 
- **依赖库** ： 
  - `numpy>=1.21.0`（用于保存返回值）


---


## 开发者 
 
- **Author** : Yihan Yu
 
- **Email** : [yihan.yu@iphy.ac.cn]()


---


## 许可证 
本项目基于 [MIT License](https://chatgpt.com/c/LICENSE)  进行分发和开源。详情请参阅 `LICENSE` 文件。

---


## 贡献指南 

欢迎对该项目进行贡献！如果您有新的想法或发现了问题，请通过以下方式参与：

1. Fork 本项目。
 
2. 创建您的功能分支：`git checkout -b feature/AmazingFeature`
 
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
 
4. 推送到分支：`git push origin feature/AmazingFeature`

5. 提交 Pull Request。


---


## 致谢 

感谢所有使用和贡献该库的开发者！